DROP DATABASE IF EXISTS random;

CREATE DATABASE random;

\c random

CREATE TABLE public.users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR 
);  

CREATE TABLE public.albums (
    album_id SERIAL PRIMARY KEY,
    album_name VARCHAR UNIQUE NOT NULL,
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

-- ADD INSERT STATEMENTS ONLY IF YOU INTEND TO PREPOPULATE THE DATABASE

INSERT INTO public.users 
(first_name, last_name)
VALUES
('User', 'one'),
('User', 'two'),
('User', 'three'),
('User', 'four'),
('User', 'five');

INSERT INTO public.albums
(album_name, album_s3_path, album_description, user_id)
VALUES
('default', 'user-1', 'user 1 album', 1),
('summer', 'user-1/summer', 'user 1 summer album', 1),
('default', 'user-2', 'user 2 album', 2),
('default', 'user-3', 'user 3 album', 3),
('random', 'user-3/random', 'user 3 misc album', 3),
('clothes', 'user-4/clothes', 'user 4 clothes album', 4),
('spring_clothes', 'user-4/clothes/spring', 'user 4 spring clothes album', 4),
('cooking', 'user-4/cooking', 'user 4 cooking album', 4),
('default', 'user-5', 'user 5 album', 5);

INSERT INTO public.pictures
(picture_name, date_created, S3_key_name, picture_description, user_id, album_id)
VALUES
('pic1', '2025-05-12', 'user-1/pic1', NULL, 1, 1),
('pic2', '2025-05-12', 'user-1/summer/pic2', NULL, 1, 2),
('pic3', '2025-05-12', 'user-2/pic3', NULL, 2, 3),
('pic4', '2025-05-12', 'user-4/clothes/pic4', NULL, 4, 6),
('pic5', '2025-05-12', 'user-4/clothes/spring/pic5', NULL, 4, 7),
('pic6', '2025-05-12', 'user-4/clothes/pic6', NULL, 4, 6)
;