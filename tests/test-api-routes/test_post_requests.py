from unittest.mock import Mock
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
import pytest
from src.utils.db_operations import util_funcs
from src.models.models import PostPictureModel, AddNewUserModel


@pytest.mark.skip
class TestAddNewUserEndpoint:
    new_user = AddNewUserModel(first_name="Jane", last_name="Doe")
    endpoint = "/users/add"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.post(self.endpoint, json=self.new_user.model_dump())

        assert response.status_code == 201

    def test_returns_correct_response(self, test_client: TestClient):
        response = test_client.post(self.endpoint, json=self.new_user.model_dump())
        
        data = response.json()
        
        assert data["message"] == "User created successfully"
        assert data["Details"]["album_name"] == "default"
        
    def test_adds_record_to_database(self, test_client: TestClient, db_conn):
        response = test_client.post(self.endpoint, json=self.new_user.model_dump())

        new_user_id = response["Details"]["user_id"]
        new_album_id = response["Details"]["album_id"]

        check_user = util_funcs["user_details"](new_user_id)["user"]
        check_album = util_funcs["user_album_details"](new_user_id, new_album_id)["album"]

        assert len(check_user) == 1
        assert len(check_album) == 1
        
        assert check_user[0]["albums"] == 1
        assert check_user[0]["pictures"] == 0
        

@pytest.mark.skip
class TestPostNewPictureEndpoint:
    user_id = 1
    album_id = 2

    picture_metadata = PostPictureModel(
        picture_name="new-pic.jpeg", picture_description="test picture"
    )

    endpoint = f"/users/{user_id}/albums/{album_id}/pictures"

    def test_returns_200_response(self, test_client: TestClient, s3_post_mock: Mock):

        with open("tests/test-files/spongebob.jpeg", "rb") as img:
            response = test_client.post(
                self.endpoint,
                json=self.picture_metadata.model_dump(),
                files={"image": ("spongebob.jpeg", img, "image/jpeg")},
            )

        assert response.status_code == 201
        assert s3_post_mock.assert_called_once()

    def test_returns_correct_response(self, test_client: TestClient, s3_post_mock: Mock):
        with open("tests/test-files/spongebob.jpeg", "rb") as img:
            response = test_client.post(
                self.endpoint,
                json=self.picture_metadata.model_dump(),
                files={"image": ("spongebob.jpeg", img, "image/jpeg")},
            )

        data = response.json()["picture"]

        assert data["s3_key_name"] == f"user-{self.user_id}/summer/{self.picture_metadata.picture_name}"
        assert data["album_id"] == self.album_id      

    def test_adds_record_to_database(self, test_client: TestClient, s3_post_mock: Mock, db_conn):
        with open("tests/test-files/spongebob.jpeg", "rb") as img:
            response = test_client.post(
                self.endpoint,
                json=self.picture_metadata.model_dump(),
                files={"image": ("spongebob.jpeg", img, "image/jpeg")},
            )

        data = response.json()["picture"]
        picture_id = data["picture_id"]

        check = util_funcs["one_picture"](picture_id)

        assert check["picture"] != []
        assert check["picture"]["picture_id"] == picture_id

    def test_returns_error_for_wrong_file_type(self, test_client: TestClient, s3_post_mock: Mock):
        with pytest.raises(HTTPException) as error:
            with open("tests/test-files/seed.sql", "rb") as img:
                test_client.post(
                    self.endpoint,
                    json=self.picture_metadata.model_dump(),
                    files={"image": ("spongebob.jpeg", img, "image/jpeg")},
                )


        assert error.value.status_code == 404
        assert "error" in error.value.detail.keys()
