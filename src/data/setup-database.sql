-- DROP DATABASE IF EXISTS cloud_api_db;
-- CREATE DATABASE cloud_api_db;
-- change to albumapidb

\c albumapidb

CREATE TABLE public.users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR 
);

CREATE TABLE public.albums (
    album_id SERIAL PRIMARY KEY,
    album_name VARCHAR NOT NULL,
    album_s3_path TEXT NOT NULL,
    album_description TEXT,
    user_id INT REFERENCES users(user_id)
);

CREATE TABLE public.pictures (
    picture_id SERIAL PRIMARY KEY,
    picture_name TEXT NOT NULL,
    date_created DATE NOT NULL,
    S3_key_name TEXT NOT NULL,
    picture_description TEXT,
    user_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    album_id INT REFERENCES albums(album_id) ON DELETE CASCADE
);
