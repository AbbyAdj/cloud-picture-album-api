"""SQL Queries for endpoints"""

# TODO update_album_data_sql and update_picture_data_sql not yet implemented

# get_user_by_secret_key_sql = """
#         SELECT * FROM users u
#         WHERE secret_key = :secret_key;
# """


all_users_sql = """
        SELECT * FROM users u
        ORDER BY u.user_id;
"""

all_albums_sql = """
        SELECT 
            u.user_id,
            u.first_name AS user_first_name,
            u.last_name AS user_last_name,
            a.album_id,
            a.album_name,
            a.album_s3_path,
            a.album_description
        FROM albums a
        LEFT JOIN users u
        ON a.user_id = u.user_id
        ORDER BY u.user_id;      
"""

all_pictures_sql = """
        SELECT 
            u.user_id,
            a.album_id,
            u.first_name AS user_first_name,
            u.last_name AS user_last_name,
            p.picture_name,
            a.album_name,
            p.s3_key_name AS picture_s3_path,
            p.picture_description,
            p.date_created
        FROM pictures p
        LEFT JOIN users u
        ON p.user_id = u.user_id
        LEFT JOIN albums a
        ON p.album_id = a.album_id
        ORDER BY u.user_id;
"""

one_picture_sql = """
        SELECT *
        FROM pictures
        WHERE pictures.picture_id = {picture_id}            
"""

user_details_sql = """
    WITH new_table AS (
        SELECT 
            u.first_name, 
            u.last_name, 
            a.album_id, 
            p.picture_id
        FROM users u
        JOIN albums a 
        ON u.user_id = a.user_id
        LEFT JOIN pictures p
        ON a.album_id = p.album_id
        WHERE u.user_id = {user_id}
        GROUP BY p.picture_id, u.first_name, u.last_name, a.album_id
    )

    SELECT first_name, last_name, COUNT(DISTINCT(album_id)) AS albums, COUNT(picture_id) AS pictures
    FROM new_table
    GROUP BY first_name, last_name;
"""

user_albums_sql = """
        SELECT 
            a.album_name,
            a.album_description,
            COUNT(p.picture_id) AS pictures_in_album
        FROM users u
        JOIN albums a
        ON u.user_id = a.user_id
        LEFT JOIN pictures p
        ON a.album_id = p.album_id
        WHERE u.user_id = {user_id}
        GROUP BY a.album_name, a.album_description, a.album_id
        ORDER BY a.album_id;
"""

user_album_sql = """
        SELECT 
            a.album_name,
            a.album_s3_path,
            p.picture_name,
            p.s3_key_name AS picture_s3_path,
            p.picture_description,
            p.date_created
        FROM pictures p
        RIGHT JOIN albums a
        ON p.album_id = a.album_id
        WHERE 
            a.user_id = {user_id} 
            AND 
            a.album_id = {album_id}
        ORDER BY p.picture_id;
"""

user_pictures_sql = """
        SELECT
            p.picture_name,
            a.album_name,
            p.s3_key_name AS picture_s3_path,
            p.date_created,
            p.picture_description
        FROM users u
        JOIN pictures p
        ON u.user_id = p.user_id
        JOIN albums a
        ON a.album_id = p.album_id
        WHERE u.user_id = {user_id}
        ORDER BY p.picture_id
"""

add_new_user_sql = """
        INSERT INTO users
        (first_name, last_name)
        VALUES
        ({first_name}, {last_name})
        RETURNING user_id
"""

add_new_user_default_album_sql = """
        INSERT INTO albums
        (album_name, album_s3_path, album_description, user_id)
        VALUES
        ('default', 'user-{user_id}', 'user {user_id} album', {user_id})
        RETURNING *
"""

add_new_picture_sql = """
        INSERT INTO pictures
        (
            picture_name, 
            date_created, 
            s3_key_name, 
            picture_description,
            user_id,
            album_id
        )
        
        VALUES
        (
            {picture_name}, 
            {date_created}, 
            {s3_key_name}, 
            {picture_description},
            {user_id},
            {album_id}
        )
        RETURNING *;
"""

# Returning * returns the deleted rows
delete_user_picture_sql = """
        DELETE
        FROM pictures
        WHERE
            user_id = {user_id}
            AND
            picture_id = {picture_id}
        RETURNING pictures.user_id, pictures.picture_id
"""

delete_user_album_sql = """
    DELETE
    FROM albums
    WHERE 
        album_id = {album_id}
        AND
        user_id = {user_id}
    RETURNING user_id, album_id, album_s3_path
"""

queries = {
    "all_users": all_users_sql,
    "all_albums": all_albums_sql,
    "one_picture": one_picture_sql,
    "all_pictures": all_pictures_sql,
    "user_details": user_details_sql,
    "user_albums": user_albums_sql,
    "user_album": user_album_sql,
    "user_pictures": user_pictures_sql,
    "add_new_user": add_new_user_sql,
    "add_new_user_default_album": add_new_user_default_album_sql,
    "add_new_picture": add_new_picture_sql,
    "delete_user_picture": delete_user_picture_sql,
    "delete_user_album": delete_user_album_sql,
}
