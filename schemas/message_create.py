from pydantic import BaseModel

class IMessage_create(BaseModel):
  my_uuid: str
  user_name: str
