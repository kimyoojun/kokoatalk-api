from fastapi import APIRouter
from sqlmodel import Session, select, update
from starlette.responses import JSONResponse as JSON

from models.user import User
from schemas.friend_add import IUsersearch, IUseradd
from db.database import engine
from models.message import Message

router = APIRouter(prefix="/user", tags=["add"])

@router.post("/select/")
async def friend_add(req:IUsersearch):
  with Session(engine) as session:
    select_friend = select(User).where(User.name == req.name)
    friend_information = session.exec(select_friend).first()
  return friend_information

@router.post("/add/")
async def friend_add_btn(req:IUseradd):
  with Session(engine) as session:
    select_my = select(User).where(User.name == req.my_name)
    my_inform = session.exec(select_my)
    my = my_inform.one()

    if my.friends is None:
      friendlist = []
    else:
      friendlist = my.friends
    friendlist.append(req.user_name)



    select_useer = select(User).where(User.name == req.user_name)
    user_infrom = session.exec(select_useer)
    user = user_infrom.one()

    if user.friends is None:
      ufriendlist = []
    else:
      ufriendlist = user.friends
    ufriendlist.append(req.my_name)


  try:
      update_my = update(User).where(User.name == req.my_name).values(friends = friendlist)
      update_user = update(User).where(User.name == req.user_name).values(friends = ufriendlist)
      session.exec(update_my)
      session.exec(update_user)
      session.commit()
  except Exception as e:
    print(e)
    return JSON({"msg": "친구추가에 실패하였습니다."}, 500)
  finally:
    return JSON({"msg": "친구추가에 성공하였습니다."}, 200)