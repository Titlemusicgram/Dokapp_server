import os
import shutil
from fastapi import FastAPI, UploadFile, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from funcs import delete_bad_symbols_and_shorten, get_gps_coords, zip_files, clean_temp_dir, create_temp_folder
from Photo_class import Photo
from config import dokapp_temp


# Создаем временную папку, если ее нет
create_temp_folder()

# Запускаем сервер
app = FastAPI()

# Создаем папку, где будут храниться фото
app.mount(f'/{dokapp_temp}', StaticFiles(directory=f'{dokapp_temp}'), name=f'{dokapp_temp}')

# Удаляем все временные фото в dokapp_temp при запуске
clean_temp_dir(dokapp_temp)

# Создаем список, где будут храниться фотографии, которые на данный момент не забрал с сервера Dockapp_desktop
list_of_photos_to_send = []

# Имя объекта по умолчанию
object_name = '123 qwerty'


class ReceivedMsg(BaseModel):
    text: str | None = None


@app.get('/')
async def get_root():
    return 'Started in web mode'


@app.get('/get_all_photos')
async def get_all_photos():
    global list_of_photos_to_send
    zip_buffer = zip_files(list_of_photos_to_send)
    list_of_photos_to_send = []

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
    global list_of_photos_to_send
    temp_filename = file.filename[:10]
    with open(f"{dokapp_temp}/{temp_filename}", "wb+") as image:
        shutil.copyfileobj(file.file, image)
    gps_coords, image_creation_date = get_gps_coords(temp_filename)
    global object_name
    photo_obj = Photo(object_name, image_creation_date, gps_coords)
    list_of_photos_to_send.append(photo_obj)
    os.replace(f"{dokapp_temp}/{temp_filename}", photo_obj.path)
    print('Just got a photo')
    print(list_of_photos_to_send)
    return 'got a photo!'
