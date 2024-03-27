from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///database.db")

async def init_db():
  SQLModel.metadata.create_all(engine)



