
CREATE TABLE public.users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR 
);  

CREATE TABLE public.albums (
    album_id SERIAL PRIMARY KEY,
    album_name VARCHAR NOT NULL CONSTRAINT cannot_have_duplicate_album_names UNIQUE,
    album_s3_path TEXT NOT NULL,
    album_description TEXT NOT NULL,
    user_id INT REFERENCES users(user_id)
);

CREATE TABLE public.pictures (
    picture.id SERIAL PRIMARY KEY,
    picture_name NOT NULL,
    date_created DATE NOT NULL,
    S3_object_link TEXT NOT NULL,
    picture_description TEXT NOT NULL,
    user_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    album_id INT REFERENCES albums(album_id) ON DELETE CASCADE
)

-- ADD INSERT STATEMENTS ONLY IF YOU INTEND TO PREPOPULATE THE DATABASE

