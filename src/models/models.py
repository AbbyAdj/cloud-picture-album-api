from pydantic import BaseModel
from fastapi import Form


class PostPictureModel(BaseModel):
    """Only use hyphens for the picture name and album name in place of spaces"""

    picture_name: str
    picture_description: str | None

    @classmethod
    def as_form(
        cls, picture_name: str = Form(...), picture_description: str | None = Form(...)
    ):
        return cls(picture_name=picture_name, picture_description=picture_description)


class AddNewUserModel(BaseModel):
    first_name: str
    last_name: str
