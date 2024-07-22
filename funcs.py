# import glob
import os
import re
from geopy.point import Point
import exifread
from config import photo_title_lenght, dokapp_temp
import zipfile
import io


# Создаем список, где будут храниться все полученные фото
list_of_all_received_photos = []


def create_temp_folder():
    if not os.path.isdir(dokapp_temp):
        os.mkdir(dokapp_temp)


def zip_files(list_of_photos: list):
    zip_buffer = io.BytesIO()
    os.chdir(dokapp_temp)
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for photo_object in list_of_photos:
            zf.write(photo_object.image_name)
            os.remove(photo_object.image_name)
    os.chdir('..')
    return zip_buffer


def delete_bad_symbols_and_shorten(received_object_name):
    received_object_name = received_object_name.replace('\n', '')
    received_object_name = re.sub(r'[<>:"/\\|?*]', '', received_object_name)
    received_object_name = received_object_name[:photo_title_lenght]
    if received_object_name[-1] == ' ':
        received_object_name = received_object_name[:-1]
    return received_object_name


# def check_the_photo(photo_id, name, number_to_check):
#     if len(glob.glob(f'{dokapp_temp}/{photo_id} {name} {number_to_check} *')) != 0:
#         number_to_check += 1
#     else:
#         number_to_check = 1
#     return number_to_check


def check_the_photo(photo_id, name):
    global list_of_all_received_photos
    count_of_existing_names = 0
    for image_name in list_of_all_received_photos:
        if f'{photo_id} {name}' == image_name:
            count_of_existing_names += 1
    correct_number = count_of_existing_names + 1
    return correct_number


def convert_coord(uni_coordinates):
    point_coord = Point.from_string(uni_coordinates)
    deci_coord = point_coord.format_decimal()
    x = round(float(deci_coord.split(', ')[0]), 6)
    y = round(float(deci_coord.split(', ')[1]), 6)
    rounded_deci_coordinates = '(' + str(x) + ', ' + str(y) + ')'
    return rounded_deci_coordinates


def get_gps_coords_and_creation_data(temp_filename):
    with open(f"{dokapp_temp}/{temp_filename}", 'rb') as image_file:
        meta_data = exifread.process_file(image_file)
        if "EXIF DateTimeOriginal" in meta_data.keys():
            image_creation_date = meta_data['EXIF DateTimeOriginal'].values.split(' ')[1].replace(':', "_")[:5]
        else:
            image_creation_date = ''
        if "GPS GPSLatitude" in meta_data.keys():
            latitude = meta_data['GPS GPSLatitude'].values
            longitude = meta_data['GPS GPSLongitude'].values
            if str(latitude[2]) == '0/0' or str(longitude[2]) == '0/0':
                pass
            elif int(latitude[0]) == 0 or int(longitude[0]) == 0:
                pass
            else:
                uni_coordinates = (f'{latitude[0]} {latitude[1]}m {float(latitude[2])}s N 'f'{longitude[0]} '
                                   f'{longitude[1]}m {float(longitude[2])}s E')
                rounded_deci_coordinates = convert_coord(uni_coordinates)
        else:
            rounded_deci_coordinates = ''
        return rounded_deci_coordinates, image_creation_date
