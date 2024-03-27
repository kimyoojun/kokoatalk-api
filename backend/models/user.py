from sqlmodel import SQLModel, Field, Column, JSON
from typing import List

class User(SQLModel, table=True):
  uuid: str = Field(primary_key=True, index=True)
  name: str = Field(index=True)
  email: str = Field(unique=True)
  id: str = Field(unique=True, index=True)
  pw: str
  token: str
  friends: List[str] = Field(sa_column=Column(JSON))
  chats: List[str] = Field(sa_column=Column(JSON))