from unittest.mock import Mock, patch
from pprint import pprint
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
import pytest
from src.utils.db_operations import util_funcs
from src.models.models import PostPictureModel, AddNewUserModel
from src.api.main import random_func

# @patch("src.api.main.insert_into_bucket")
# def test_random(s3_post_mock):
#     # mock.return_value = {
#     #         "picture_name": "new-pic.jpeg",
#     #         "s3_key_name": "user-1/summer/new-pic.jpeg",
#     #         "date_created": "2025-05-24",
#     #         "picture_description": "test picture",
#     #         "album_name": "summer",
#     #     }
#     picture_metadata = PostPictureModel(
#         picture_name="new-pic.jpeg", picture_description="test picture"
#     )
#     random = random_func(picture_metadata)
#     print(random)


# @pytest.mark.skip
class TestAddNewUserEndpoint:
    new_user = AddNewUserModel(first_name="Jane", last_name="Doe")
    endpoint = "/users/add"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.post(self.endpoint, json=self.new_user.model_dump())

        assert response.status_code == 201

    def test_returns_correct_response(self, test_client: TestClient):
        response = test_client.post(self.endpoint, json=self.new_user.model_dump())

        data = response.json()

        assert data["success"] == "User created successfully"
        assert data["Details"]["album_name"] == "default"

    def test_adds_record_to_database(self, test_client: TestClient):
        response = test_client.post(self.endpoint, json=self.new_user.model_dump())

        data = response.json()

        new_user_id = data["Details"]["user_id"]
        new_album_id = data["Details"]["album_id"]

        check_user = util_funcs["user_details"](new_user_id)["user"]

        check_album = util_funcs["user_album_details"](new_user_id, new_album_id)[
            "album"
        ]

        assert len(check_user) == 1
        assert len(check_album) == 1

        assert check_user[0]["albums"] == 1
        assert check_user[0]["pictures"] == 0


# @pytest.mark.skip
class TestPostNewPictureEndpoint:
    user_id = 1
    album_id = 2

    picture_metadata = PostPictureModel(
        picture_name="new-pic.jpeg", picture_description="test picture"
    )

    endpoint = f"/users/{user_id}/albums/{album_id}/pictures"

    # @pytest.mark.skip
    def test_returns_200_response(self, test_client: TestClient, s3_post_mock: Mock):

        with open("tests/test-files/spongebob.jpeg", "rb") as img:
            response = test_client.post(
                self.endpoint,
                data=self.picture_metadata.model_dump(),
                files={"new_file": ("spongebob.jpeg", img, "image/jpeg")},
            )

        assert response.status_code == 201
        s3_post_mock.assert_called_once()

    # @pytest.mark.skip
    def test_returns_correct_response(
        self, test_client: TestClient, s3_post_mock: Mock
    ):
        with open("tests/test-files/spongebob.jpeg", "rb") as img:
            response = test_client.post(
                self.endpoint,
                data=self.picture_metadata.model_dump(),
                files={"new_file": ("spongebob.jpeg", img, "image/jpeg")},
            )

        data = response.json()["picture"][0]

        assert (
            data["s3_key_name"]
            == f"user-{self.user_id}/summer/{self.picture_metadata.picture_name}"
        )
        assert data["album_id"] == self.album_id

    # @pytest.mark.skip
    def test_adds_record_to_database(
        self, test_client: TestClient, s3_post_mock: Mock, db_conn
    ):
        with open("tests/test-files/spongebob.jpeg", "rb") as img:
            response = test_client.post(
                self.endpoint,
                data=self.picture_metadata.model_dump(),
                files={"new_file": ("spongebob.jpeg", img, "image/jpeg")},
            )

        data = response.json()["picture"][0]
        picture_id = data["picture_id"]

        check = util_funcs["one_picture"](picture_id)["picture"][0]

        assert check != []
        assert check["picture_id"] == picture_id

    # @pytest.mark.skip
    def test_returns_error_for_wrong_file_type(
        self, test_client: TestClient, s3_post_mock: Mock
    ):

        with open("tests/test-files/seed.sql", "rb") as img:
            response = test_client.post(
                self.endpoint,
                data=self.picture_metadata.model_dump(),
                files={"new_file": ("spongebob.jpeg", img, "image/txt")},
            )

        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "Invalid File Type. Allowed types are jpeg, png and webp"
        )
