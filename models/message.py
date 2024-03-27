from sqlmodel import SQLModel, Field, Column, JSON
from typing import List

class Message(SQLModel, table=True):
  create_user: str
  uuid: str = Field(primary_key=True, index=True)
  message: List[str] = Field(sa_column=Column(JSON))
  user_list: List[str] = Field(sa_column=Column(JSON))
  my_msg: List[int] = Field(sa_column=Column(JSON))
  user_msg: List[int] = Field(sa_column=Column(JSON))
  