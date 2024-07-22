from fastapi import APIRouter
from pydantic import BaseModel
import os
import shutil
from fastapi import UploadFile, Response
from Photo_class import Photo
from funcs import delete_bad_symbols_and_shorten, get_gps_coords_and_creation_data, zip_files
from config import dokapp_temp
from funcs import list_of_all_received_photos


router = APIRouter()

# Создаем список, где будут храниться фотографии, которые на данный момент не забрал с сервера Dockapp_desktop
list_of_photos_to_send = []

# Имя объекта по умолчанию
object_name = '123 qwerty'


class ReceivedMsg(BaseModel):
    text: str | None = None


@router.get('/')
async def get_root():
    return 'Started in web mode'


@router.get('/get_all_photos')
async def get_all_photos():
    global list_of_photos_to_send
    if list_of_photos_to_send:
        file_to_send = [list_of_photos_to_send.pop(0)]
    else:
        file_to_send = []
    zip_buffer = zip_files(file_to_send)

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(zip_buffer.getvalue(), media_type="application/x-zip-compressed",
                    headers={'Content-Disposition': f'attachment;filename=archive.zip'})
    return resp


@router.post('/')
async def post_root(msg: ReceivedMsg):
    global object_name
    try:
        if type(msg.text.split(' ', maxsplit=1)[1]) == str and msg.text.split(' ', maxsplit=1)[0].isdigit():
            object_name = delete_bad_symbols_and_shorten(msg.text)
    except IndexError:
        print("Неверный формат названия объекта")
    print(object_name)
    return 'Got a text!'


@router.post('/post_photo')
async def post_photo(file: UploadFile):
    global list_of_photos_to_send
    temp_filename = file.filename[:10]
    with open(f"{dokapp_temp}/{temp_filename}", "wb+") as image:
        shutil.copyfileobj(file.file, image)
    gps_coords, image_creation_date = get_gps_coords_and_creation_data(temp_filename)
    global object_name
    photo_obj = Photo(object_name, image_creation_date, gps_coords)
    list_of_photos_to_send.append(photo_obj)
    list_of_all_received_photos.append(f'{photo_obj.global_id} {photo_obj.object_name}')
    os.replace(f"{dokapp_temp}/{temp_filename}", photo_obj.path)
    print('Just got a photo')
    print(list_of_photos_to_send)
    print(list_of_all_received_photos)
    return 'got a photo!'
