from pydantic import BaseModel

class IMessage_send(BaseModel):
  message: str
  chatuuid: str
  myuuid: str