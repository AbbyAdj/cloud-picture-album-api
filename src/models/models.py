from pydantic import BaseModel


class PostPictureModel(BaseModel):
    picture_name: str
    picture_description: str
    album_name: str

class AddNewUserModel(BaseModel):
    first_name: str
    last_name: str