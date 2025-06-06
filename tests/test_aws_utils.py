import json
from botocore.exceptions import ClientError, ParamValidationError
from moto import mock_aws
import pytest
from src.utils.aws_utils import (
    insert_into_bucket,
    delete_object_from_bucket,
    delete_album_from_bucket,
    delete_main_user_album_from_bucket,
    USERS_BUCKET_NAME,
)
from src.models.models import PostPictureModel


# @pytest.mark.skip
@mock_aws
class TestInsertIntoBucket:
    data = PostPictureModel(
        picture_name="new-pic.json", picture_description="random description"
    )

    file = {"type": "object"}

    def test_inserts_object_into_bucket(self, s3_client, s3_client_with_bucket):

        new_record = insert_into_bucket(
            s3_client=s3_client,
            file=json.dumps(self.file),
            user_given_metadata=self.data,
            user_album_name="new",
        )

        check_response = s3_client.get_object(
            Bucket=USERS_BUCKET_NAME, Key=new_record["s3_key_name"]
        )

        data = check_response["Body"].read().decode("utf-8")

        assert json.loads(data) == self.file


    def test_handles_exceptions(self, s3_client):
        new_record = insert_into_bucket(
            s3_client=s3_client,
            file=self.file,
            user_given_metadata=self.data,
            user_album_name="new",
        )

        assert new_record["error"] == "Upload unsuccessful. Try again later"


# @pytest.mark.skip
@mock_aws
class TestDeleteObjectFromBucket:

    def test_deletes_existing_object(self, s3_client, s3_client_with_object):
        response = delete_object_from_bucket(s3_client, file_key="new-file")

        assert response == {"Success": "Object deleted successfully"}


    def test_handles_error_for_incorrect_key_name(self, s3_client, s3_client_with_object):
        response = delete_object_from_bucket(
            s3_client, file_key="does-not-exist.txt"
        )

        assert response["error"] == "Deletion unsuccessful. Try again later"


# @pytest.mark.skip
@mock_aws
class TestDeleteAlbumFromBucket:

    def test_deletes_folder_from_bucket(self, s3_client, s3_client_with_objects):
        response = delete_album_from_bucket(s3_client, album_key="store")

        assert response == {"Success": "Object deleted successfully"}

    def test_deletes_all_files_from_folder(self, s3_client, s3_client_with_objects):
        delete_album_from_bucket(s3_client, album_key="store")

        with pytest.raises(ParamValidationError):
            s3_client.get_object(
                Bcket=USERS_BUCKET_NAME, Key="store/newer-file"
            )

    def test_handles_error_for_wrong_album_name(s3, s3_client, s3_client_with_objects):
        response = delete_album_from_bucket(s3_client, album_key="wrong")

        assert response["error"] == "Deletion unsuccessful. Try again later"


# @pytest.mark.skip
# @mock_aws
class TestDeleteMainUserAlbumFromBucket:

    def test_deletes_all_objects_and_folders_for_user_folder(
        self, s3_client, s3_client_with_user_objects
    ):
        user_id = 1
        response = delete_main_user_album_from_bucket(
            s3_client, user_id=user_id
        )

        assert response == {"Success": "Object deleted successfully"}

        check_objects = s3_client.list_objects_v2(
            Bucket=USERS_BUCKET_NAME, Prefix=f"user-{user_id}"
        )        
        check_all_objects = s3_client.list_objects_v2(
            Bucket=USERS_BUCKET_NAME
        )

        assert check_objects["KeyCount"] == 0
        assert check_all_objects["KeyCount"] == 1


    def test_handles_error_for_incorrect_or_nonexistent_user_id(s3, s3_client, s3_client_with_user_objects):
        response = delete_main_user_album_from_bucket(s3_client, user_id=10)
        # test might fail because 1 can be considered a prefix of 10

        assert response == {
                    "error": "Deletion unsuccessful. Try again later",
                    "details": "Key does not exist"
                    }

