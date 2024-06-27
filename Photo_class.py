from funcs import check_the_photo


class Photo:
    global_id: int
    object_name: str
    gps: str
    image_creation_date: str
    number_of_photo: int = 1
    image_name: str
    path: str

    def __init__(self, photo_name, image_creation_date, gps_coords):
        self.global_id = photo_name.split(' ', maxsplit=1)[0]
        self.object_name = photo_name.split(' ', maxsplit=1)[1]
        self.gps = gps_coords
        self.image_creation_date = image_creation_date
        Photo.number_of_photo = check_the_photo(self.global_id, self.object_name, Photo.number_of_photo)
        self.number_of_photo = Photo.number_of_photo
        self.image_name = (f"{self.global_id} {self.object_name} {self.number_of_photo} {self.image_creation_date} "
                           f"{self.gps}.jpg")
        self.path = f"dokapp_temp/{self.image_name}"
