import os
import shutil
from fastapi import FastAPI, UploadFile, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from funcs import delete_bad_symbols_and_shorten, get_gps_coords, zip_files
from Photo_class import Photo

app = FastAPI()

# Создаем папку, где будут храниться фото
app.mount('/dokap_temp', StaticFiles(directory='dokapp_temp'), name='dokapp_temp')

# Создаем список, где будут храниться фотографии, которые на данный момент не забрал с сервера Dockapp_desktop
list_of_photos_to_send = []

object_name = '123 qwerty'


class ReceivedMsg(BaseModel):
    text: str | None = None


@app.get('/')
async def get_root():
    return 'Started in web mode'


@app.get('/get_all_photos')
async def get_all_photos():
    zip_buffer = zip_files(list_of_photos_to_send)

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(zip_buffer.getvalue(), media_type="application/x-zip-compressed",
                    headers={'Content-Disposition': f'attachment;filename=archive.zip'})
    return resp


@app.post('/')
async def post_root(msg: ReceivedMsg):
    global object_name
    object_name = delete_bad_symbols_and_shorten(msg.text)
    print(object_name)
    return 'Got a text!'


@app.post('/post_photo')
async def post_photo(file: UploadFile):
    temp_filename = file.filename[:10]
    with open(f"dokapp_temp/{temp_filename}", "wb+") as image:
        shutil.copyfileobj(file.file, image)
    gps_coords, creation_date = get_gps_coords(temp_filename)
    global object_name
    photo_obj = Photo(object_name, creation_date, gps_coords)
    list_of_photos_to_send.append(photo_obj)
    os.replace(f"dokapp_temp/{temp_filename}", photo_obj.path)
    print('Just got a photo')
    return 'got a photo!'
