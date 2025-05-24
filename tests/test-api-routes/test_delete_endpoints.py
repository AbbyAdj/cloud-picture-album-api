from unittest.mock import Mock 
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
import pytest
from src.utils.db_operations import util_funcs


# TODO: NEED TO PATCH AWS S3 CONNECTION/METHODS

@pytest.mark.skip
class TestDeleteUserPictureEndpoint:
    user_id = 1
    picture_id = 1
    endpoint = f"/users/{user_id}/pictures/{picture_id}"

    def test_returns_200_response(self, test_client: TestClient, s3_delete_mock_success: Mock):
        response = test_client.delete(self.endpoint)

        assert response.status_code == 200
        assert s3_delete_mock_success.assert_called_once()

    def test_returns_correct_response(self, test_client: TestClient, s3_delete_mock_success: Mock):
        response = test_client.delete(self.endpoint)
        
        data = response.json()
        
        assert data == {
                "message": f"User {self.user_id}'s picture with picture id {self.picture_id} deleted successfully"
            }
        
    def test_deletes_record_from_database(self, test_client: TestClient, s3_delete_mock_success: Mock):
        test_client.delete(self.endpoint)

        response = util_funcs["one_picture"](self.picture_id)["picture"]

        assert bool(response) is False
        assert response == []

    def test_handles_error(self, test_client: TestClient, s3_delete_mock_error: Mock):
        user_id = 12
        picture_id = 14
        endpoint = f"/users/{user_id}/pictures/{picture_id}"
        with pytest.raises(HTTPException) as error:
            test_client.delete(endpoint)

        assert s3_delete_mock_error.assert_called_once()
        assert error.value.status_code == 404
        assert "error" in error.value.detail.keys()
 

@pytest.mark.skip
class TestDeleteUserAlbumEndpoint:
    user_id = 4
    album_id = 6
    endpoint = f"/users/{user_id}/albums/{album_id}"

    def test_returns_200_response(self, test_client: TestClient, s3_delete_mock_success: Mock):
        response = test_client.delete(self.endpoint)

        assert response.status_code == 200
        assert s3_delete_mock_success.assert_called_once()

    def test_returns_correct_response(self, test_client: TestClient, s3_delete_mock_success: Mock):
        response = test_client.delete(self.endpoint)
        
        data = response.json()
        
        assert data == {
                "message": f"User {self.user_id}'s album with album id {self.album_id} deleted successfully"
            }

    def test_deletes_record_from_database(self, test_client: TestClient, s3_delete_mock_success: Mock):
        response = test_client.delete(self.endpoint)

        response = util_funcs["user_album"](self.user_id, self.album_id)["album"]

        assert bool(response) is False   
        assert response == [] 

    def test_handles_error(self, test_client: TestClient, s3_delete_mock_error: Mock):
        user_id = 12
        album_id = 14
        endpoint = f"/users/{user_id}/pictures/{album_id}"
        response = test_client.delete(endpoint)

        assert s3_delete_mock_error.assert_called_once()
        assert "error" in response.keys()

