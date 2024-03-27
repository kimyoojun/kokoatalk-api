from fastapi import APIRouter
from sqlmodel import Session, select, update
from starlette.responses import JSONResponse as JSON
import uuid

from db.database import engine
from models.message import Message
from models.user import User
from schemas.message_create import IMessage_create
from schemas.message_goin import IMessage_goin
from schemas.message_send import IMessage_send

router = APIRouter(prefix="/message", tags=["message"])

@router.post("/")
async def chatting(req:IMessage_create):
  with Session(engine) as session:
    useruuid = select(User).where(User.name == req.user_name)
    user_uuid_infrom = session.exec(useruuid)
    user = user_uuid_infrom.first()


    is_user = select(Message).where(Message.user_list == [req.my_uuid, user.uuid])
    is_uesrlist = session.exec(is_user)
    userlist = is_uesrlist.first()


    is_users = select(Message).where(Message.user_list == [user.uuid, req.my_uuid])
    is_uesrslist = session.exec(is_users)
    userslist = is_uesrslist.first()
    
    if userlist:
      chatuuid = userlist.uuid

    if userslist:
      chatuuid = userslist.uuid

  if userlist or userslist:
    return "존재함", user, chatuuid
  else:
    chat_uuid = uuid.uuid1()

    participation = []
    participation.append(req.my_uuid)
    participation.append(user.uuid)

    message = Message(
      create_user=req.my_uuid,
      uuid=str(chat_uuid),
      user_list=participation
    )

    my_chats_add = update(User).where(User.uuid == req.my_uuid).values(chats=str(chat_uuid))
    user_chats_add = update(User).where(User.uuid == user.uuid).values(chats=str(chat_uuid))

    session.add(message)
    session.exec(my_chats_add)
    session.exec(user_chats_add)
    session.commit()
    return "채팅창 생성", chat_uuid
    



@router.post("/send")
async def my_message(req: IMessage_send):
  with Session(engine) as session:
    select_chatting = select(Message).where(Message.uuid == req.chatuuid)
    chatting_inform = session.exec(select_chatting).first()

    if chatting_inform.message is None:
      newChat = []
    else:
      newChat = chatting_inform.message
    newChat.append(req.message)

    chat_len = len(newChat) - 1
    
    if chatting_inform.create_user == req.myuuid:
      if chatting_inform.my_msg is None:
        my_msgindex = []
      else:
        my_msgindex = chatting_inform.my_msg
      my_msgindex.append(chat_len)
      user_msgindex = chatting_inform.user_msg
    else:
      if chatting_inform.user_msg is None:
        user_msgindex = []
      else:
        user_msgindex = chatting_inform.user_msg
      user_msgindex.append(chat_len)
      my_msgindex = chatting_inform.my_msg

      
  try:
      update_chat = update(Message).where(Message.uuid == req.chatuuid).values(message = newChat, my_msg = my_msgindex, user_msg = user_msgindex)
      session.exec(update_chat)
      session.commit()
  except Exception as e:
    print(e)
    return JSON({"msg": "메세지 전송에 실패하였습니다."}, 500)
  finally:
    return JSON({"msg": "메세지전송에 성공하였습니다"}, 200)
  



@router.post("/window")
async def message_window(req: IMessage_goin):
  with Session(engine) as session:
    user_select = select(User).where(User.uuid == req.useruuid)
    user_infrom = session.exec(user_select).first()

    chatuuid = select(Message).where(Message.uuid == req.chatuuid)
    chat_record = session.exec(chatuuid).first()

  return user_infrom.name, chat_record
