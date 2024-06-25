import glob
import re
from geopy.point import Point
import exifread
from config import photo_title_lenght
import zipfile
import io


def zip_files(list_of_photos_to_send):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for photo_object in list_of_photos_to_send:
            zf.write(photo_object.path)
    return zip_buffer


def delete_bad_symbols_and_shorten(received_object_name):
    received_object_name = received_object_name.replace('\n', '')
    received_object_name = re.sub(r'[<>:"/\\|?*]', '', received_object_name)
    received_object_name = received_object_name[:photo_title_lenght]
    if received_object_name[-1] == ' ':
        received_object_name = received_object_name[:-1]
    return received_object_name


def check_the_photo(photo_id, name, number_to_check):
    if len(glob.glob(f'dokapp_temp/{photo_id} {name} {number_to_check} *')) != 0:
        number_to_check += 1
    else:
        number_to_check = 1
    return number_to_check


def convert_coord(uni_coordinates):
    point_coord = Point.from_string(uni_coordinates)
    deci_coord = point_coord.format_decimal()
    x = round(float(deci_coord.split(', ')[0]), 6)
    y = round(float(deci_coord.split(', ')[1]), 6)
    rounded_deci_coordinates = '(' + str(x) + ', ' + str(y) + ')'
    return rounded_deci_coordinates


def get_gps_coords(temp_filename):
    with open(f"dokapp_temp/{temp_filename}", 'rb') as image_file:
        meta_data = exifread.process_file(image_file)
        if "GPS GPSLatitude" in meta_data.keys():
            latitude = meta_data['GPS GPSLatitude'].values
            longitude = meta_data['GPS GPSLongitude'].values
            creation_date = meta_data['EXIF DateTimeOriginal'].values.split(' ')[1].replace(':', "_")[:5]
            if str(latitude[2]) == '0/0' or str(longitude[2]) == '0/0':
                pass
            elif int(latitude[0]) == 0 or int(longitude[0]) == 0:
                pass
            else:
                uni_coordinates = (f'{latitude[0]} {latitude[1]}m {float(latitude[2])}s N 'f'{longitude[0]} '
                                   f'{longitude[1]}m {float(longitude[2])}s E')
                rounded_deci_coordinates = convert_coord(uni_coordinates)
        return rounded_deci_coordinates, creation_date
