from fastapi import FastAPI, WebSocket, UploadFile
from pydantic import BaseModel

app = FastAPI()


class ReceivedMsg(BaseModel):
    text: str | None = None


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Message was: {data}")


@app.get('/')
async def get_root():
    return 'Started in web mode'


@app.post('/')
async def post_root(msg: ReceivedMsg):
    print(msg.text)
    return 'Got a text!'


@app.post('/post_photo')
async def post_photo(file: UploadFile):
    print(file.filename)
    print('Just got a photo')
    return 'got a photo!'
