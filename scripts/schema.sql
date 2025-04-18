-- GUYS CAREFUL WHEN RUNNING THIS -  UNCOMMENT TABLE DELETION ONLY WHEN U HAVE TO


-- DROP TABLE IF EXISTS Includes;
-- DROP TABLE IF EXISTS HasMovieCast;
-- DROP TABLE IF EXISTS HasTags;
-- DROP TABLE IF EXISTS IsGenre;
-- DROP TABLE IF EXISTS AvailableOn;
-- DROP TABLE IF EXISTS Review;
-- DROP TABLE IF EXISTS WatchHistory;
-- DROP TABLE IF EXISTS WatchList;
-- DROP TABLE IF EXISTS UserProfileSettings;
-- DROP TABLE IF EXISTS Tag;
-- DROP TABLE IF EXISTS Genre;
-- DROP TABLE IF EXISTS MovieCast;
-- DROP TABLE IF EXISTS Platform;
-- DROP TABLE IF EXISTS Movie;
-- DROP TABLE IF EXISTS "User";

-- User
CREATE TABLE "User" (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL
);

-- UserProfileSettings
CREATE TABLE UserProfileSettings (
    user_id INT PRIMARY KEY REFERENCES "User"(user_id),
    notification_pref VARCHAR(50)
);

-- Movie
CREATE TABLE Movie (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE,
    duration INT,
    language VARCHAR(10),
    image_url TEXT,
    avg_rating NUMERIC(3, 1)
);

-- MovieCast
CREATE TABLE MovieCast (
    cast_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(255)
);

-- Platform
CREATE TABLE Platform (
    platform_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    url TEXT
);

-- Genre
CREATE TABLE Genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL
);

-- Tag
CREATE TABLE Tag (
    tag_id SERIAL PRIMARY KEY,
    tag_text VARCHAR(100)
);

-- WatchList
CREATE TABLE WatchList (
    watchlist_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES "User"(user_id),
    title VARCHAR(100),
    date_created DATE DEFAULT CURRENT_DATE,
    watch_status VARCHAR(50)
);

-- Review
CREATE TABLE Review (
    review_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES "User"(user_id),
    movie_id INT REFERENCES Movie(movie_id),
    platform_id INT REFERENCES Platform(platform_id),
    rating NUMERIC(3, 1),
    review_date DATE,
    headline VARCHAR(255),
    review_text TEXT,
    review_body TEXT,
    UNIQUE (user_id, movie_id, platform_id)
);

-- WatchHistory
CREATE TABLE WatchHistory (
    user_id INT REFERENCES "User"(user_id),
    movie_id INT REFERENCES Movie(movie_id),
    watch_date DATE,
    device_used VARCHAR(100),
    duration_watched INT,
    PRIMARY KEY (user_id, movie_id)
);

-- Includes
CREATE TABLE Includes (
    watchlist_id INT REFERENCES WatchList(watchlist_id),
    movie_id INT REFERENCES Movie(movie_id),
    PRIMARY KEY (watchlist_id, movie_id)
);

-- HasMovieCast
CREATE TABLE HasMovieCast (
    movie_id INT REFERENCES Movie(movie_id),
    cast_id INT REFERENCES MovieCast(cast_id),
    role VARCHAR(255),
    PRIMARY KEY (movie_id, cast_id)
);

-- HasTags
CREATE TABLE HasTags (
    movie_id INT REFERENCES Movie(movie_id),
    tag_id INT REFERENCES Tag(tag_id),
    PRIMARY KEY (movie_id, tag_id)
);

-- IsGenre
CREATE TABLE IsGenre (
    movie_id INT REFERENCES Movie(movie_id),
    genre_id INT REFERENCES Genre(genre_id),
    PRIMARY KEY (movie_id, genre_id)
);

-- AvailableOn
CREATE TABLE AvailableOn (
    movie_id INT REFERENCES Movie(movie_id),
    platform_id INT REFERENCES Platform(platform_id),
    PRIMARY KEY (movie_id, platform_id)
);
