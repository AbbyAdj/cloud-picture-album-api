from dotenv import load_dotenv
import os
from datetime import datetime
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, ParamValidationError
from src.models.models import PostPictureModel

load_dotenv()


###########################
# S3 CLIENT
###########################

# This assumes that the bucket for storing user files has already been created.
# This should be provided in the .env as S3_USER_STORAGE_BUCKET

USERS_BUCKET_NAME = os.getenv("S3_USER_STORAGE_BUCKET")


# bucket name
# album name (user-1 is the default album/bucket and remains as is if specified)
# file name
# object key = bucket name/user-id/album name/file name

# file/image


def insert_into_bucket(
    s3_client, file, user_given_metadata: PostPictureModel, user_album_name=""
) -> dict:

    key = f"{user_album_name}{user_given_metadata.picture_name}"

    try:
        put_object_response = s3_client.put_object(
            Body=file, Bucket=USERS_BUCKET_NAME, Key=key
        )

        date_created = datetime.now().strftime("%Y-%m-%d")

        object_metadata = {
            "picture_name": user_given_metadata.picture_name,
            "s3_key_name": key,
            "date_created": date_created,
            "picture_description": user_given_metadata.picture_description,
            "album_name": user_album_name,
        }
    except ClientError as error:
        return {"error": "Upload unsuccessful. Try again later", "details": error}
    except ParamValidationError as error:
        return {"error": "Upload unsuccessful. Try again later", "details": error}

    else:
        return object_metadata


def delete_object_from_bucket(s3_client, file_key: str):

    # object_exists = True
    try:
        s3_client.get_object(Bucket=USERS_BUCKET_NAME, Key=file_key)
    except ClientError as error:
        return {"error": "Deletion unsuccessful. Try again later", "details": error}
    else:
        s3_client.delete_object(
            Bucket=USERS_BUCKET_NAME,
            Key=file_key,
        )
        return {"Success": "Object deleted successfully"}


def delete_album_from_bucket(s3_client, album_key: str):

    try:
        get_all_files_in_album = s3_client.list_objects_v2(
            Bucket=USERS_BUCKET_NAME, Prefix=album_key
        )

        if "Contents" in get_all_files_in_album.keys():
            all_files = [
                file_record["Key"] for file_record in get_all_files_in_album["Contents"]
            ]
            for file_key in all_files:
                delete_object_from_bucket(s3_client, file_key)
            return {"Success": "Object deleted successfully"}
        else:
            # print(get_all_files_in_album.keys())
            return {
                "error": "Deletion unsuccessful. Try again later",
                "details": "Key does not exist",
            }

    except ClientError as error:
        return {"error": "Deletion unsuccessful. Try again later", "details": error}


# The function below should only be triggered when the user is deleting their account
def delete_main_user_album_from_bucket(s3_client, user_id: int):
    album_key = f"user-{user_id}"
    try:
        response = delete_album_from_bucket(s3_client, album_key=album_key)
        return response
    except ClientError as error:
        return {"error": "Deletion unsuccessful. Try again later", "details": error}
