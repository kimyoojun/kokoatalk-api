from fastapi import APIRouter
from sqlmodel import Session, select
from starlette.responses import JSONResponse as JSON

from schemas.friend_list import IFriendlist
from db.database import engine
from models.user import User

router = APIRouter(prefix="/friendlist", tags=["friend"])

@router.post("/")
async def friend_list(req:IFriendlist):
  with Session(engine) as session:
    select_token = select(User).where(User.token == req.my_token)
    token_inform = session.exec(select_token).first()
    friendlist = []
    for friends in token_inform.friends:
      friendlist.append(friends)
  return friendlist