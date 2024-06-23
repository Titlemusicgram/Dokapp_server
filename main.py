import shutil
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Создаем папку, где будут храниться фото
app.mount('/dokap_temp', StaticFiles(directory='dokapp_temp'), name='dokapp_temp')

# Создаем список, где будут храниться фотографии, которые на данный момент не забрал с сервера Dockapp_desktop
list_of_photos_to_send = []


class ReceivedMsg(BaseModel):
    text: str | None = None


class Photo:
    global_id: int
    name: str
    path: str

    def __init__(self, global_id):
        self.global_id = global_id
        self.name = "name"
        self.path = f"dokapp_temp/{global_id} {self.name}.jpg"


@app.get('/')
async def get_root():
    return 'Started in web mode'


@app.get('/get_all_photos')
async def get_all_photos():
    return 'In process...'


@app.post('/')
async def post_root(msg: ReceivedMsg):
    print(msg.text)
    return 'Got a text!'


@app.post('/post_photo')
async def post_photo(file: UploadFile):
    photo_global_id = file.filename.split("%", maxsplit=1)[0]
    photo_obj = Photo(photo_global_id)
    list_of_photos_to_send.append(photo_obj)
    with open(f"{photo_obj.path}", "wb+") as image:
        shutil.copyfileobj(file.file, image)
    print(list_of_photos_to_send)
    print('Just got a photo')
    return 'got a photo!'
