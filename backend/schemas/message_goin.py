from pydantic import BaseModel

class IMessage_goin(BaseModel):
  useruuid: str
  chatuuid: str
