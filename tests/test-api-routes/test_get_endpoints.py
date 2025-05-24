from fastapi.testclient import TestClient
import pytest


@pytest.mark.skip
class TestHealthcheckEndpoint:
    endpoint = "/healthcheck"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        assert response.status_code == 200

    def test_returns_correct_response(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        data = response.json()

        assert data == {"message": "Server is running", "status_code": 200}


@pytest.mark.skip
class TestGetAllUsersEndpoint:

    endpoint = "/users"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        assert response.status_code == 200

    def test_returns_correct_response_strcuture(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        data = response.json()

        assert isinstance(data["users"], list)
        assert len(data["users"]) == 5
        assert data["users"][2]["last_name"] == "three"


@pytest.mark.skip
class TestGetAllAlbumsEndpoint:

    endpoint = "/albums"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        assert response.status_code == 200

    def test_returns_correct_response_strcuture(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        data = response.json()

        assert isinstance(data["albums"], list)
        assert len(data["albums"]) == 9
        assert data["albums"][4]["album_name"] == "random"


@pytest.mark.skip
class TestGetAllPicturesEndpoint:

    endpoint = "/pictures"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        assert response.status_code == 200

    def test_returns_correct_response_strcuture(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        data = response.json()

        assert isinstance(data["pictures"], list)
        assert len(data["pictures"]) == 6
        assert data["pictures"][4]["picture_s3_path"] == "user-4/clothes/spring/pic5"


@pytest.mark.skip
class TestGetUserDetailsEndpoint:
    user_id = 4
    endpoint = f"/users/{user_id}/user-details"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        assert response.status_code == 200

    def test_returns_correct_response_strcuture(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        data = response.json()

        assert isinstance(data["user"], list)
        assert len(data["user"]) == 1
        assert data["user"][0]["albums"] == 3
        assert data["user"][0]["pictures"] == 3

    def test_empty_response_for_no_data_in_database(self, test_client: TestClient):
        user_id = 10
        endpoint = f"/users/{user_id}/user-details"

        response = test_client.get(endpoint)

        data = response.json()

        assert data["user"] == []


@pytest.mark.skip
class TestGetUserAlbumsEndpoint:
    user_id = 4
    endpoint = f"/users/{user_id}/albums"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        assert response.status_code == 200

    def test_returns_correct_response_strcuture(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        data = response.json()

        assert isinstance(data["albums"], list)
        assert len(data["albums"]) == 3
        assert data["albums"][0]["album_name"] == "clothes"
        assert data["albums"][0]["pictures_in_album"] == 2

    def test_empty_response_for_no_data_in_database(self, test_client: TestClient):
        user_id = 10
        endpoint = f"/users/{user_id}/albums/"

        response = test_client.get(endpoint)

        data = response.json()

        assert data["albums"] == []


@pytest.mark.skip
class TestGetUserAlbumEndpoint:
    user_id = 4
    album_id = 6
    endpoint = f"/users/{user_id}/albums/{album_id}"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        assert response.status_code == 200

    def test_returns_correct_response_strcuture(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        data = response.json()

        assert isinstance(data["album"], list)
        assert len(data["album"]) == 3
        assert data["album"][0]["album_name"] == "clothes"
        assert data["album"][0]["pictures_s3_path"] == "user-4/clothes/pic4"

    def test_empty_response_for_no_data_in_database(self, test_client: TestClient):
        user_id = 10
        album_id = 1
        endpoint = f"/users/{user_id}/albums/{album_id}"

        response = test_client.get(endpoint)

        data = response.json()

        assert data["album"] == []


@pytest.mark.skip
class TestGetUserPicturesEndpoint:
    user_id = 2
    endpoint = f"/users/{user_id}/pictures"

    def test_returns_200_response(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        assert response.status_code == 200

    def test_returns_correct_response_strcuture(self, test_client: TestClient):
        response = test_client.get(self.endpoint)

        data = response.json()

        assert isinstance(data["pictures"], list)
        assert len(data["pictures"]) == 3
        assert data["pictures"][0]["album_name"] == "default"
        assert data["pictures"][0]["pictures_s3_path"] == "user-2/pic3"

    def test_empty_response_for_no_data_in_database(self, test_client: TestClient):
        user_id = 10
        endpoint = f"/users/{user_id}/pictures"
        response = test_client.get(endpoint)

        data = response.json()

        assert data["pictures"] == []
