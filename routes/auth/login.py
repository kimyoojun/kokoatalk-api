from starlette.responses import JSONResponse as JSON
from sqlmodel import Session, select
from fastapi import APIRouter

from schemas.auth import ILogin
from models.user import User
from db.database import engine

router = APIRouter(prefix="/auth/login", tags=["auth"])

@router.post("/")
async def login_user(req:ILogin):
  if not req.id:
    return JSON({"msg": "아이디를 입력하세요"}, 400)
  
  if req.id in ["admin"]:
    return JSON({"msg": "사용할 수 없는 아이디입니다."}, 400)
  
  if not req.pw:
    return JSON({"msg": "비밀번호를 입력하세요"}, 400)
  
  with Session(engine) as session:
    select_information = select(User).filter(User.id == req.id)
    row = session.exec(select_information)
    db_information = row.first()

  if db_information.id == req.id and db_information.pw == req.pw + 'a':
    return JSON({"msg": "로그인에 성공하였습니다."}, 200), db_information
  else:
    return JSON({"msg": "로그인에 실패하였습니다. 다시 시도해주세요."}, 500)