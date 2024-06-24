import os
import shutil
import re
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from config import photo_title_lenght

app = FastAPI()

# Создаем папку, где будут храниться фото
app.mount('/dokap_temp', StaticFiles(directory='dokapp_temp'), name='dokapp_temp')

# Создаем список, где будут храниться фотографии, которые на данный момент не забрал с сервера Dockapp_desktop
list_of_photos_to_send = []

object_name = 'qwerty'


def delete_bad_symbols_and_shorten(received_object_name):
    received_object_name = received_object_name.replace('\n', '')
    received_object_name = re.sub(r'[<>:"/\\|?*]', '', received_object_name)
    received_object_name = received_object_name[:photo_title_lenght]
    if received_object_name[-1] == ' ':
        received_object_name = received_object_name[:-1]
    return received_object_name


def check_the_photo(photo_id, name, number_to_check, gps):
    path_to_check = f'dokapp_temp/{photo_id} {name} {number_to_check} {gps}.jpg'
    if os.path.isfile(path_to_check):
        number_to_check += 1
    else:
        number_to_check = 1
    return number_to_check


class ReceivedMsg(BaseModel):
    text: str | None = None


class Photo:
    global_id: int
    name: str
    gps: str = '(None)'
    number_of_photo: int = 1
    path: str

    def __init__(self, photo_name):
        self.global_id = photo_name.split(' ', maxsplit=1)[0]
        self.name = photo_name.split(' ', maxsplit=1)[1]
        Photo.number_of_photo = check_the_photo(self.global_id, self.name, Photo.number_of_photo, self.gps)
        self.number_of_photo = Photo.number_of_photo
        self.path = f"dokapp_temp/{self.global_id} {self.name} {self.number_of_photo} {self.gps}.jpg"


@app.get('/')
async def get_root():
    return 'Started in web mode'


@app.get('/get_all_photos')
async def get_all_photos():
    return 'In process...'


@app.post('/')
async def post_root(msg: ReceivedMsg):
    global object_name
    object_name = delete_bad_symbols_and_shorten(msg.text)
    print(object_name)
    return 'Got a text!'


@app.post('/post_photo')
async def post_photo(file: UploadFile):
    global object_name
    photo_obj = Photo(object_name)
    list_of_photos_to_send.append(photo_obj)
    with open(f"{photo_obj.path}", "wb+") as image:
        shutil.copyfileobj(file.file, image)
    print(list_of_photos_to_send)
    print('Just got a photo')
    return 'got a photo!'
