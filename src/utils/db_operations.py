"""Handles all database operations using pg8000 and src.utils.db_utils."""

from pg8000.native import literal
from src.data.queries import queries
from src.utils.db_utils import run_query
from src.models.models import AddNewUserModel


def util_return_all_users() -> dict:
    all_users_query = queries["all_users"]
    all_users = run_query(all_users_query, json_key="users")
    return all_users


def util_return_all_albums() -> dict:
    all_albums_query = queries["all_albums"]
    all_albums = run_query(all_albums_query, "albums")
    return all_albums


def util_return_all_pictures() -> dict:
    all_pictures_query = queries["all_pictures"]
    all_pictures = run_query(all_pictures_query, "pictures")
    return all_pictures


def util_return_picture(picture_id: int) -> dict:
    picture_query = queries["one_picture"].format(picture_id=literal(picture_id))
    picture = run_query(picture_query, "picture")
    return picture


def util_return_user_details(user_id: int) -> dict:
    user_details_query = queries["user_details"].format(user_id=literal(user_id))
    user_details = run_query(user_details_query, "user")
    return user_details


def util_return_user_albums(user_id: int) -> dict:
    user_albums_query = queries["user_albums"].format(user_id=literal(user_id))
    user_albums = run_query(user_albums_query, "albums")
    return user_albums


def util_return_user_album_details(user_id: int, album_id: int) -> dict:
    user_album_query = queries["user_album"].format(
        user_id=literal(user_id), album_id=literal(album_id)
    )
    user_album = run_query(user_album_query, "album")
    return user_album


def util_return_all_user_pictures(user_id) -> dict:
    all_user_pictures_query = queries["user_pictures"].format(user_id=literal(user_id))
    all_user_pictures = run_query(all_user_pictures_query, "pictures")
    return all_user_pictures


def util_add_new_user(user_details: AddNewUserModel) -> dict:

    new_user_query = queries["add_new_user"].format(
        first_name=literal(user_details.first_name),
        last_name=literal(user_details.last_name),
    )

    new_user_id = run_query(new_user_query)

    new_user_album_query = queries["add_new_user_default_album"].format(
        user_id=literal(new_user_id[0]["user_id"])
    )

    new_album_response = run_query(new_user_album_query)

    if "message" in new_album_response or "message" in new_user_id:
        return {"message": "Error occured during database operation"}

    return {
        "success": "User created successfully",
        "Details": {
            "first_name": user_details.first_name,
            "last_name": user_details.last_name,
            "user_id": new_album_response[0]["user_id"],
            "album_id": new_album_response[0]["album_id"],
            "album_name": new_album_response[0]["album_name"],
        },
    }


def util_insert_new_picture(user_id, album_id, metadata) -> dict:
    if "error" in metadata.keys():
        return metadata

    new_picture_query = queries["add_new_picture"].format(
        picture_name=literal(metadata["picture_name"]),
        date_created=literal(metadata["date_created"]),
        s3_key_name=literal(metadata["s3_key_name"]),
        picture_description=literal(metadata["picture_description"]),
        user_id=literal(user_id),
        album_id=literal(album_id),
    )
    new_picture = run_query(new_picture_query, "picture")
    return new_picture


def util_delete_user_picture(user_id, picture_id, delete_confirmation) -> dict:
    if "error" in delete_confirmation.keys():
        return delete_confirmation

    elif "Success" in delete_confirmation.keys():
        delete_user_picture_query = queries["delete_user_picture"].format(
            user_id=literal(user_id), picture_id=literal(picture_id)
        )
        result = run_query(delete_user_picture_query)
        if (
            result
            and result[0]["user_id"] == user_id
            and result[0]["picture_id"] == picture_id
        ):
            return {
                "success": f"User {user_id}'s picture with picture id {picture_id} deleted successfully"
            }
        else:
            return result


def util_delete_user_album(user_id, album_id, delete_confirmation) -> dict:
    if "error" in delete_confirmation.keys():
        return delete_confirmation

    elif "Success" in delete_confirmation.keys():

        delete_user_album_query = queries["delete_user_album"].format(
            user_id=literal(user_id), album_id=literal(album_id)
        )

        result = run_query(delete_user_album_query)

        if (
            result
            and result[0]["user_id"] == user_id
            and result[0]["album_id"] == album_id
        ):
            return {
                "success": f"User {user_id}'s album with album id {album_id} deleted successfully"
            }


util_funcs = {
    "all_users": util_return_all_users,
    "all_albums": util_return_all_albums,
    "all_pictures": util_return_all_pictures,
    "one_picture": util_return_picture,
    "user_details": util_return_user_details,
    "user_album_details": util_return_user_album_details,
    "user_albums": util_return_user_albums,
    "all_user_pictures": util_return_all_user_pictures,
    "add_new_user": util_add_new_user,
    "insert_new_picture": util_insert_new_picture,
    "delete_user_picture": util_delete_user_picture,
    "delete_user_album": util_delete_user_album,
}
