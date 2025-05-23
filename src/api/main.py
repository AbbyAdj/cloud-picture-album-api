from pprint import pprint
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from pg8000.dbapi import DatabaseError
import boto3
from botocore.exceptions import ClientError
from src.utils.db_operations import util_funcs
from src.models.models import PostPictureModel, AddNewUserModel

# from src.api.exception_handler import database_error_handler
from src.utils.aws_utils import insert_into_bucket,delete_object_from_bucket,delete_album_from_bucket,


app = FastAPI()

s3_client = boto3.client("s3")

###########################
# GET REQUESTS
###########################


@app.get("/healthcheck")
def healthcheck():
    return {"message": "Server is running", "status_code": 200}


@app.get("/users")
def get_all_users():
    response = util_funcs["all_users"]()
    return response


@app.get("/albums")
def get_all_albums():
    response = util_funcs["all_albums"]()
    return response


@app.get("/pictures")
def get_all_pictures():
    response = util_funcs["all_pictures"]()
    return response


@app.get("/users/{user_id}/user-details")
def get_user_details(user_id: int):
    response = util_funcs["user_details"](user_id=user_id)
    return response


@app.get("/users/{user_id}/albums")
def get_user_albums(user_id: int):
    response = util_funcs["user_albums"](user_id=user_id)
    return response


@app.get("/users/{user_id}/albums/{album_id}")
def get_user_album(user_id: int, album_id: int):
    response = util_funcs["user_album_details"](user_id=user_id, album_id=album_id)
    return response


@app.get("/users/{user_id}/pictures")
def get_all_user_pictures(user_id: int):
    response = util_funcs["all_user_pictures"](user_id=user_id)
    return response


###########################
# POST REQUESTS
###########################


@app.post("/users/add", status_code=201)
def add_new_user(new_user: AddNewUserModel):

    new_user_response = util_funcs["add_new_user"](user_details=new_user)

    return new_user_response


@app.post("/users/{user_id}/albums/{album_id}/pictures", status_code=201)
def post_new_picture(
    user_id: int,
    album_id: int,
    picture_metadata: PostPictureModel,
    new_file: UploadFile = File(...),
):

    if new_file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        return {"error": "Invalid file type"}
    user_album_response = util_funcs["user_album_details"](
        user_id=user_id, album_id=album_id
    )["album"]
    user_album_name = user_album_response.get("album_name", default="")
    # If i receive an album id that is not valid, I will put it in the default user album
    album_name = "" if user_album_name == "default" else user_album_name

    s3_upload_response = insert_into_bucket(
        s3_client,
        file=new_file,
        user_given_metadata=picture_metadata,
        album_name=f"user-{user_id}/{album_name}",
    )

    response = util_funcs["insert_new_picture"](
        user_id=user_id, album_id=album_id, metadata=s3_upload_response
    )
    return response


###########################
# PATCH REQUESTS
###########################

# TODO TO BE IMPLEMENTED LATER


###########################
# DELETE REQUESTS
###########################


@app.delete("/users/{user_id}/pictures/{picture_id}")
def delete_user_picture(user_id: int, picture_id: int):

    picture_key = util_funcs["one_picture"]["picture"]["s3_key_name"]

    s3_delete_response = delete_object_from_bucket(s3_client, file_key=picture_key)

    response = util_funcs["delete_user_picture"](
        user_id=user_id, picture_id=picture_id, delete_confirmation=s3_delete_response
    )
    return response


@app.delete("/users/{user_id}/albums/{album_id}")
def delete_user_album(user_id: int, album_id: int):

    album_key = util_funcs["user_album_details"]["album"]["album_s3_path"]

    s3_delete_response = delete_album_from_bucket(s3_client, album_key=album_key)

    response = util_funcs["delete_user_album"](
        user_id=user_id, album_id=album_id, delete_confirmation=s3_delete_response
    )
    return response


# TODO DELETE USER IS A RECURSIVE ACTION. DELETES EVERYTHING!
