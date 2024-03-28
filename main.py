from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os

from routes.message_box import message_box
from routes.auth import register
from routes.auth import login
from db.database import init_db
from routes.friend_add import friend_add
from routes import friend_list

@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("API starting up")
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://localhost:5173/*",
    os.environ.get["KOKOATALK_HOST"],
    os.environ.get["KOKOATALK_HOST"] + '/*',
]

app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_box.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(friend_add.router)
app.include_router(friend_list.router)

@app.get("/")
def read_root():
    return {"연결상태": "코코아톡"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text({data})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)

