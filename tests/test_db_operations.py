from datetime import date
import pytest
from pg8000.exceptions import DatabaseError
from src.utils.db_operations import util_funcs
from src.models.models import PostPictureModel, AddNewUserModel


@pytest.mark.skip
class TestReturnAllUsers:
    all_users = util_funcs["all_users"]
    all_users_list = all_users["users"]

    def test_returns_all_users(self):
        # check first record 
        first_record = self.all_users_list[0]
        assert first_record["user_id"] == 1
        assert first_record["first_name"] == "User"
        assert first_record["last_name"] == "one"
        
        # check last record
        last_record = self.all_users_list[-1]
        assert last_record["user_id"] == 5
        assert last_record["first_name"] == "User"
        assert last_record["last_name"] == "five"      


    def test_returns_correct_datatype(self):
        for record in self.all_users_list:
            assert isinstance(record["user_id"], int)
            assert isinstance(record["first_name"], str)
            assert isinstance(record["last_name"], str)


    def test_returns_correct_number_of_records(self):
        assert len(self.all_users_list) == 5


    def test_returns_all_columns(self):
        first_record = self.all_users_list[0]
        columns = list(first_record.keys())

        assert len(columns) == 3


@pytest.mark.skip
class TestReturnAllAlbums:
    all_albums = util_funcs["all_albums"]
    all_albums_list = all_albums["albums"]

    def test_returns_all_albums(self):
        # check first record 
        first_record = self.all_albums_list[0]
        assert first_record["user_id"] == 1
        assert first_record["user_first_name"] == "User"
        assert first_record["user_last_name"] == "one"
        assert first_record["album_id"] == 1
        assert first_record["album_name"] == "default"
        assert first_record["album_s3_path"] == "user-1"
        assert first_record["album_description"] == "user 1 album"

        # check last record
        last_record = self.all_albums_list[-1]
        assert last_record["user_id"] == 5
        assert last_record["user_first_name"] == "User"
        assert last_record["user_last_name"] == "five"
        assert last_record["album_id"] == 9
        assert last_record["album_name"] == "default"
        assert last_record["album_s3_path"] == "user-5"
        assert last_record["album_description"] == "user 5 album"


    def test_returns_correct_datatype(self):
        for record in self.all_albums_list:
            assert isinstance(record["user_id"], int)
            assert isinstance(record["user_first_name"], str)
            assert isinstance(record["user_last_name"], str)
            assert isinstance(record["album_id"], int)
            assert isinstance(record["album_name"], str)
            assert isinstance(record["album_s3_path"], str)
            assert isinstance(record["album_description"], str)


    def test_returns_correct_number_of_records(self):
        # Num of rows
        assert len(self.all_albums_list) == 9
    

    def test_returns_all_columns(self):
        first_record = self.all_albums_list[0]
        columns = list(first_record.keys())

        assert len(columns) == 7


@pytest.mark.skip
class TestReturnAllPictures:
    all_pictures = util_funcs["all_pictures"]
    all_pictures_list = all_pictures["pictures"]

    def test_returns_all_pictures(self):
        # check first record 
        first_record = self.all_pictures_list[0]
        assert first_record["user_id"] == 1
        assert first_record["album_id"] == 1
        assert first_record["user_first_name"] == "User"
        assert first_record["user_last_name"] == "one"
        assert first_record["picture_name"] == "pic1"
        assert first_record["album_name"] == "default"
        assert first_record["picture_s3_path"] == "user-1/pic1"
        assert first_record["picture_description"] == None
        assert first_record["date_created"] == "2025-05-12"

        # check last record
        last_record = self.all_pictures_list[-1]
        assert last_record["user_id"] == 4
        assert last_record["album_id"] == 6
        assert last_record["user_first_name"] == "User"
        assert last_record["user_last_name"] == "four"
        assert last_record["picture_name"] == "pic6"
        assert last_record["album_name"] == "clothes"
        assert last_record["picture_s3_path"] == "user-4/clothes/pic6"
        assert last_record["picture_description"] == None
        assert last_record["date_created"] == "2025-05-12"


    def test_returns_correct_datatype(self):
        for record in self.all_albums_list:
            assert isinstance(record["user_id"], int)
            assert isinstance(record["album_id"], int)
            assert isinstance(record["user_first_name"], str)
            assert isinstance(record["user_last_name"], str)
            assert isinstance(record["picture_name"], str)
            assert isinstance(record["album_name"], str)
            assert isinstance(record["picture_s3_path"], str)
            assert isinstance(record["picture_description"], str)
            assert isinstance(record["date_created"], date)


    def test_returns_correct_number_of_records(self):
        # Num of rows
        assert len(self.all_pictures_list) == 6
    

    def test_returns_all_columns(self):
        first_record = self.all_pictures_list[0]
        columns = list(first_record.keys())

        assert len(columns) == 9


@pytest.mark.skip
class TestReturnPicture:
    picture = util_funcs["one_picture"](picture_id=1)
    record = picture["picture"][0]

    def test_returns_one_picture_(self):
        assert self.record["picture_id"] == 1
        assert self.record["picture_name"] == "pic1"
        assert self.record["date_created"] == "2025-05-12"
        assert self.record["S3_key_name"] == "user-1/pic1"
        assert self.record["picture_description"] == None
        assert self.record["user_id"] == 1
        assert self.record["album_id"] == 1


    def test_returns_correct_datatype(self):
        assert isinstance(self.record["picture_id"], int)
        assert isinstance(self.record["picture_name"], str)
        assert isinstance(self.record["date_created"], date)
        assert isinstance(self.record["S3_key_name"], str)
        assert isinstance(self.record["picture_description"], str)
        assert isinstance(self.record["user_id"], int)
        assert isinstance(self.record["album_id"], int)


    def test_returns_correct_number_of_records(self):
        # Num of rows
        assert len(self.picture["picture"]) == 1
    

    def test_returns_all_columns(self):
        columns = list(self.record.keys())

        assert len(columns) == 7


@pytest.mark.skip
class TestReturnUserDetails:
    user_details = util_funcs["user_details"](user_id=1)
    record = user_details["user"][0]

    def test_returns_user_details(self):
        assert self.record["first_name"] == "User"
        assert self.record["last_name"] == "one"
        assert self.record["albums"] == 2
        assert self.record["pictures"] == 2


    def test_returns_correct_datatype(self):
        assert isinstance(self.record["first_name"], str)
        assert isinstance(self.record["last_name"], str)
        assert isinstance(self.record["albums"], int)
        assert isinstance(self.record["pictures"], int)


    def test_returns_correct_number_of_records(self):
        # Num of rows
        assert len(self.user_details["user_details"]) == 1
    

    def test_returns_all_columns(self):
        columns = list(self.record.keys())

        assert len(columns) == 4


@pytest.mark.skip
class TestReturnUserAlbums:
    user_albums = util_funcs[""](user_id=1)
    user_albums_list = user_albums["albums"]
    first_record = user_albums_list[0]
    last_record = user_albums_list[-1]

    def test_returns_user_albums(self):
        assert self.first_record["album_name"] == "default"
        assert self.first_record["album_description"] == "user 1 album"
        assert self.first_record["pictures_in_album"] == 1        
        
        assert self.last_record["album_name"] == "summer"
        assert self.last_record["album_description"] == "user 1 summer album"
        assert self.last_record["pictures_in_album"] == 1


    def test_returns_correct_datatype(self):
        for record in self.user_albums_list:
            assert isinstance(record["album_name"], str)
            assert isinstance(record["album_description"], str)
            assert isinstance(record["pictures_in_album"], int)


    def test_returns_correct_number_of_records(self):
        # Num of rows
        assert len(self.user_albums_list) == 2
    

    def test_returns_all_columns(self):
        columns = list(self.first_record.keys())

        assert len(columns) == 3


@pytest.mark.skip
class TestReturnUserAlbumDetails:
    user_album_details = util_funcs["user_album_details"](user_id=1, album_id=1)
    user_album_details_list = user_album_details["album"]
    record = user_album_details_list[0]

    def test_returns_all_user_album_details(self):
        assert self.record["album_name"] == ""
        assert self.record["album_s3_path"] == ""
        assert self.record["picture_name"] == ""
        assert self.record["picture_s3_path"] == ""
        assert self.record["picture_description"] == ""
        assert self.record["date_created"] == ""


    def test_returns_correct_datatype(self):
        assert isinstance(self.record["album_name"], str)
        assert isinstance(self.record["album_s3_path"], str)
        assert isinstance(self.record["picture_name"], str)
        assert isinstance(self.record["picture_s3_path"], str)
        assert isinstance(self.record["picture_description"], str)
        assert isinstance(self.record["date_created"], date)


    def test_returns_correct_number_of_records(self):
        # Num of rows
        assert len(self.user_album_details_list) == 1
    

    def test_returns_all_columns(self):
        columns = list(self.record.keys())

        assert len(columns) == 6


@pytest.mark.skip
class TestReturnAllUserPictures:
    all_user_pictures = util_funcs["all_user_pictures"](user_id=4)
    all_user_pictures_list = all_user_pictures["pictures"]
    first_record = all_user_pictures_list[0]
    last_record = all_user_pictures_list[-1]

    def test_returns_all_user_pictures(self):
        assert self.first_record["picture_name"] == "pic4"
        assert self.first_record["album_name"] == "clothes"
        assert self.first_record["picture_s3_path"] == "user-4/clothes/pic4"
        assert self.first_record["date_created"] == "2025-05-12"
        assert self.first_record["picture_description"] == None

        assert self.first_record["picture_name"] == "pic6"
        assert self.first_record["album_name"] == "clothes"
        assert self.first_record["picture_s3_path"] == "user-4/clothes/pic6"
        assert self.first_record["date_created"] == "2025-05-12"
        assert self.first_record["picture_description"] == None


    def test_returns_correct_datatype(self):
        for record in self.all_user_pictures:
            assert isinstance(record["picture_name", str])
            assert isinstance(record["album_name", str])
            assert isinstance(record["picture_s3_path", str])
            assert isinstance(record["date_created", str])
            assert isinstance(record["picture_description", str|None])


    def test_returns_correct_number_of_records(self):
        # Num of rows
        assert len(self.all_user_pictures_list) == 3
    

    def test_returns_all_columns(self):
        columns = list(self.first_record.keys())

        assert columns == 5


@pytest.mark.skip
class TestAddNewUser:
    new_user_details = AddNewUserModel(first_name="John", last_name="Doe")

    def test_adds_new_user_record(self):
        users_before_insertion = util_funcs["all_users"]["users"]
        new_user = util_funcs["add_new_user"](user_details=self.new_user_details)
        users_after_insertion = util_funcs["all_users"]["users"]

        assert len(users_after_insertion) == len(users_before_insertion) + 1

        assert new_user["Details"]["first_name"] == "John"
        assert new_user["Details"]["last_name"] == "Doe"


    def test_adds_new_default_album_for_user(self):
        albums_before_insertion = util_funcs["all_albums"]["albums"]
        new_user = util_funcs["add_new_user"](user_details=self.new_user_details)
        albums_after_insertion = util_funcs["all_albums"]["albums"]

        assert len(albums_after_insertion) == len(albums_before_insertion) - 1

        assert new_user["Details"]["album_name"] == "default"


    @pytest.mark.skip("need to check which errors we might encounter")
    def test_returns_error_with_wrong_input_type(self):
        pass
    


@pytest.mark.skip
class TestInsertNewPicture:
    new_picture_details = PostPictureModel(picture_name="new-pic", picture_description="new input")

    def test_inserts_new_picture(self):
        user_id = 3
        album_id = 6
        album_name = f"user-{user_id}/clothes"
        key = f"{album_name}/{self.new_picture_details.picture_name}"

        s3_response = {
            "picture_name":self.new_picture_details.picture_name,
            "s3_key_name": key,
            "date_created": "2025-05-06",
            "picture_description": self.new_picture_details.picture_description,
            "album_name": album_name
        }

        pictures_before_insertion = util_funcs["all_pictures"]["pictures"]
        new_picture =util_funcs["insert_new_picture"]["picture"](user_id, album_id, s3_response)
        pictures_after_insertion = util_funcs["all_pictures"]["pictures"]

        assert len(pictures_after_insertion) == len(pictures_before_insertion) - 1

        assert new_picture["picture_name"] == self.new_picture_details.picture_name
        assert new_picture["date_created"] == "2025-05-06"
        assert new_picture["s3_key_name"] == key
        assert new_picture["picture_description"] == self.new_picture_details.picture_description


    def test_handles_errors_from_s3_upload(self):
        user_id = 3
        album_id = 6
        album_name = f"user-{user_id}/clothes"
        key = f"{album_name}/{self.new_picture_details.picture_name}"

        s3_response = {
            "picture_name": None,
            "s3_key_name": key,
            "date_created": "2025-05-06",
            "picture_description": None,
            "album_name": album_name
        }

        response = util_funcs["insert_new_picture"]["picture"](user_id, album_id, s3_response)

        assert response["error"] == "Upload unsuccessful. Try again later"


@pytest.mark.skip
class TestDeleteUserPicture:

    def test_deletes_user_picture(self):
        user_id = 4
        picture_id = 6
        s3_response = {"Success": "Object deleted successfully"}

        pictures_before_deletion = util_funcs["all_pictures"]["pictures"]
        user_pictures_before_deletion = util_funcs["user_pictures"]["pictures"]
        
        new_picture = util_funcs["delete_user_picture"](user_id, picture_id, s3_response)
        
        pictures_after_deletion = util_funcs["all_pictures"]["pictures"]
        user_pictures_after_deletion = util_funcs["user_pictures"]["pictures"]

        assert len(pictures_after_deletion) == len(pictures_before_deletion) - 1
        assert len(user_pictures_after_deletion) == len(user_pictures_before_deletion) - 1
        
        assert new_picture["message"] == f"User {user_id}'s picture with picture id {picture_id} deleted successfully"


    def test_handles_errors_from_s3_delete(self):
        user_id = 4
        picture_id = 6
        s3_response = {
                "error": "Deletion unsuccessful. Try again later",
                "details": "Ignore this"}
        
        new_picture = util_funcs["insert_new_picture"]["picture"](user_id, picture_id, s3_response)
        
        assert new_picture == s3_response
        

@pytest.mark.skip
class TestDeleteUserAlbum:

    def test_deletes_user_album(self):
        user_id = 4
        album_id = 6
        s3_response =  {"Success": "Object deleted successfully"}

        albums_before_deletion = util_funcs["all_albums"]["albums"]
        user_albums_before_deletion = util_funcs["user_albums"]["albums"]
        
        response = util_funcs["delete_user_album"](user_id, album_id, s3_response)
        
        albums_after_deletion = util_funcs["all_albums"]["albums"]
        user_albums_after_deletion = util_funcs["user_albums"]["albums"]

        assert len(albums_after_deletion) == len(albums_before_deletion) - 1
        assert len(user_albums_after_deletion) == len(user_albums_before_deletion) - 1

        assert response["message"] == f"User {user_id}'s album with album id {album_id} deleted successfully"

    def test_recursively_deletes_user_pictures_in_album(self):
        # check how many pictures in album before deleting
        # check total user pictures before and after deleting
    
        user_id = 4
        album_id = 6
        s3_response =  {"Success": "Object deleted successfully"}

        user_pictures_in_album = len(util_funcs["user_album_details"]["album"])
        user_pictures_before_deletion = len(util_funcs["all_pictures"]["pictures"])

        util_funcs["delete_user_album"](user_id, album_id, s3_response)

        user_pictures_after_deletion = len(util_funcs["user_pictures"]["pictures"])

        assert user_pictures_before_deletion == user_pictures_in_album + user_pictures_after_deletion


    def test_handles_errors_from_s3_delete(self):
        user_id = 4
        album_id = 6
        s3_response = {
                "error": "Deletion unsuccessful. Try again later",
                "details": "Ignore this"}
        
        response = util_funcs["delete_user_album"](user_id, album_id, s3_response)
        
        assert response["message"] == s3_response
