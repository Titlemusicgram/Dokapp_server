from funcs import check_the_photo


class Photo:
    global_id: int
    name: str
    gps: str
    creation_date: str
    number_of_photo: int = 1
    path: str

    def __init__(self, photo_name, creation_date, gps_coords):
        self.global_id = photo_name.split(' ', maxsplit=1)[0]
        self.name = photo_name.split(' ', maxsplit=1)[1]
        self.gps = gps_coords
        self.creation_date = creation_date
        Photo.number_of_photo = check_the_photo(self.global_id, self.name, Photo.number_of_photo)
        self.number_of_photo = Photo.number_of_photo
        self.path = (f"dokapp_temp/{self.global_id} {self.name} {self.number_of_photo} "
                     f"{self.creation_date} {self.gps}.jpg")
