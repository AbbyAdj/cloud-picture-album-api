from pprint import pprint
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pg8000.dbapi import DatabaseError
import boto3
from botocore.exceptions import ClientError
from src.api.exception_handler import (
    database_error_handler,
    return_404_error,
    aws_client_error,
)
from src.utils.db_operations import util_funcs
from src.models.models import PostPictureModel, AddNewUserModel

# from src.api.exception_handler import database_error_handler
from src.utils.aws_utils import (
    insert_into_bucket,
    delete_object_from_bucket,
    delete_album_from_bucket,
)


app = FastAPI()
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(HTTPException, return_404_error)
app.add_exception_handler(ClientError, aws_client_error)

s3_client = boto3.client("s3")

###########################
# GET REQUESTS
###########################

# TODO put all get exception raising in a wrapper


@app.get("/healthcheck")
def healthcheck():
    return {"message": "Server is running", "status_code": 200}


@app.get("/users")
def get_all_users():
    response = util_funcs["all_users"]()
    if not response["users"]:
        raise HTTPException(404, "No users found")
    elif "message" in response:
        raise DatabaseError()
    return response


@app.get("/albums")
def get_all_albums():
    response = util_funcs["all_albums"]()
    if not response["albums"]:
        raise HTTPException(404, "No albums found")
    elif "message" in response:
        raise DatabaseError()
    return response


@app.get("/pictures")
def get_all_pictures():
    response = util_funcs["all_pictures"]()
    if not response["pictures"]:
        raise HTTPException(404, "No pictures found")
    elif "message" in response:
        raise DatabaseError()
    return response


@app.get("/users/{user_id}/user-details")
def get_user_details(user_id: int):
    response = util_funcs["user_details"](user_id=user_id)
    if not response["user"]:
        raise HTTPException(404, f"User with id {user_id} not found")
    elif "message" in response:
        raise DatabaseError()
    return response


@app.get("/users/{user_id}/albums")
def get_user_albums(user_id: int):
    response = util_funcs["user_albums"](user_id=user_id)
    if not response["albums"]:
        raise HTTPException(404, f"No albums found for user with id {user_id}")
    elif "message" in response:
        raise DatabaseError()
    return response


@app.get("/users/{user_id}/albums/{album_id}")
def get_user_album(user_id: int, album_id: int):
    response = util_funcs["user_album_details"](user_id=user_id, album_id=album_id)
    if not response["album"]:
        raise HTTPException(
            404,
            f"Album with album id {album_id} not found for user with user id {user_id}",
        )
    elif "message" in response:
        raise DatabaseError()
    return response


@app.get("/users/{user_id}/pictures")
def get_all_user_pictures(user_id: int):
    response = util_funcs["all_user_pictures"](user_id=user_id)
    if not response["pictures"]:
        raise HTTPException(404, f"No pictures found for user with id {user_id}")
    elif "message" in response:
        raise DatabaseError()
    return response


###########################
# POST REQUESTS
###########################


@app.post("/users/add", status_code=201)
def add_new_user(new_user: AddNewUserModel):

    new_user_response = util_funcs["add_new_user"](user_details=new_user)

    if not new_user_response:
        raise HTTPException(404, "No pictures found")
    elif "message" in new_user_response:
        raise DatabaseError()
    return new_user_response


@app.post("/users/{user_id}/albums/{album_id}/pictures", status_code=201)
def post_new_picture(
    user_id: int,
    album_id: int,
    picture_metadata: PostPictureModel = Depends(PostPictureModel.as_form),
    new_file: UploadFile = File(...),
):

    if new_file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            404, "Invalid File Type. Allowed types are jpeg, png and webp"
        )

    user_album_response = util_funcs["user_album_details"](
        user_id=user_id, album_id=album_id
    )["album"][0]

    user_album_name = user_album_response.get("album_name", "")
    # If i receive an album id that is not valid, I will put it in the default user album
    album_name = "" if user_album_name == "default" else user_album_name

    s3_upload_response = insert_into_bucket(
        s3_client,
        file=new_file,
        user_given_metadata=picture_metadata,
        user_album_name=f"user-{user_id}/{album_name}",
    )

    response = util_funcs["insert_new_picture"](
        user_id=user_id, album_id=album_id, metadata=s3_upload_response
    )

    if "message" in response:
        raise DatabaseError()
    elif "error" in response:
        raise ClientError()
    elif not response["picture"][0]:
        raise HTTPException(404, "Unable to add new picture")

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
    try:
        picture_key = util_funcs["one_picture"](picture_id)["picture"][0]["s3_key_name"]

        s3_delete_response = delete_object_from_bucket(s3_client, file_key=picture_key)

        response = util_funcs["delete_user_picture"](
            user_id=user_id,
            picture_id=picture_id,
            delete_confirmation=s3_delete_response,
        )

        if "message" in response:
            raise DatabaseError()
        elif "error" in response:
            raise HTTPException(404, "Unable to delete picture")

        return response
    except IndexError as e:
        raise HTTPException(404, "Unable to delete picture")


@app.delete("/users/{user_id}/albums/{album_id}")
def delete_user_album(user_id: int, album_id: int):
    try:
        album_key = util_funcs["user_album_details"](user_id, album_id)["album"][0][
            "album_s3_path"
        ]

        s3_delete_response = delete_album_from_bucket(s3_client, album_key=album_key)

        response = util_funcs["delete_user_album"](
            user_id=user_id, album_id=album_id, delete_confirmation=s3_delete_response
        )

        if "message" in response:
            raise DatabaseError()
        elif "error" in response:
            raise HTTPException(404, "Unable to delete album")

        return response
    except IndexError as e:
        raise HTTPException(404, "Unable to delete album")


# TODO DELETE USER IS A RECURSIVE ACTION. DELETES EVERYTHING!


def random_func(picture_metadata: PostPictureModel):
    user_id, album_name = 1, 2
    s3_upload_response = insert_into_bucket(
        s3_client,
        file="random.txt",
        user_given_metadata=picture_metadata,
        user_album_name=f"user-{user_id}/{album_name}",
    )
    return s3_upload_response
