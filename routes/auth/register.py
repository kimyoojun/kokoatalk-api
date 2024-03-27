from starlette.responses import JSONResponse as JSON
from sqlmodel import Session
from fastapi import APIRouter
import uuid

from schemas.auth import IRegister
from models.user import User
from db.database import engine

router = APIRouter(prefix="/auth/register", tags=["auth"])

@router.post("/")
async def register_user(req:IRegister):
  if not req.name:
    return JSON({"msg": "이름을 입력하세요"}, 400)
  
  if not req.email:
    return JSON({"msg": "이메일을 입력하세요"}, 400)
  
  if not req.id:
    return JSON({"msg": "아이디를 입력하세요"}, 400)
  
  if req.id in ["admin"]:
    return JSON({"msg": "사용할 수 없는 아이디입니다."}, 400)
  
  if not req.pw:
    return JSON({"msg": "비밀번호를 입력하세요"}, 400)
  
  HASH_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
  user_uuid = uuid.uuid1()
  
  user = User(
    uuid=str(user_uuid),
    name=req.name,
    email=req.email,
    id=req.id,
    pw=req.pw + 'a',
    token = (req.id + req.name + req.email).upper() + HASH_KEY
  )



  try:
    with Session(engine) as session:
      session.add(user)
      session.commit()
  except Exception as e:
    print(e)
    return JSON({"msg": "회원가입에 실패하였습니다. 다시 시도해주세요."}, 500)
  finally:
    return JSON({"msg": "회원가입에 성공하였습니다."}, 200)