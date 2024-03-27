from pydantic import BaseModel

class IUsersearch(BaseModel):
  name: str

class IUseradd(BaseModel):
  my_name: str
  user_name: str