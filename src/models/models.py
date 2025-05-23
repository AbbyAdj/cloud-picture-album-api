from pydantic import BaseModel


class PostPictureModel(BaseModel):
    """Only use hyphens for the picture name and album name in place of spaces"""
    picture_name: str
    picture_description: str | None

class AddNewUserModel(BaseModel):
    first_name: str
    last_name: str




