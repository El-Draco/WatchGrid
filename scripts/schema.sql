-- GUYS CAREFUL WHEN RUNNING THIS -  UNCOMMENT TABLE DELETION ONLY WHEN U HAVE TO


-- DROP TABLE Includes;
-- DROP TABLE HasMovieCast;
-- DROP TABLE HasTags;
-- DROP TABLE IsGenre;
-- DROP TABLE AvailableOn;
-- DROP TABLE Review;
-- DROP TABLE WatchHistory;
-- DROP TABLE WatchList;
-- DROP TABLE UserProfileSettings;
-- DROP TABLE Tag;
-- DROP TABLE Genre;
-- DROP TABLE MovieCast;
-- DROP TABLE Platform;
-- DROP TABLE Movie;

-- DROP TABLE "User";

-- USERS table
CREATE TABLE Users (
    user_id VARCHAR2(36),
    first_name VARCHAR2(100) NOT NULL,
    last_name VARCHAR2(100) NOT NULL,  -- made NOT NULL for validation
    email VARCHAR2(255) NOT NULL UNIQUE,
    password_hash VARCHAR2(255) NOT NULL,
    date_of_birth DATE NOT NULL,

    CONSTRAINT Users_PK PRIMARY KEY (user_id)
);

-- USER PROFILE SETTINGS with avatar + optional notification prefs
CREATE TABLE UserProfileSettings (
    user_id VARCHAR2(36),
    notification_pref VARCHAR2(50),
    avatar_blob BLOB,
    avatar_mime_type VARCHAR2(50),

    CONSTRAINT UserProfileSettings_PK PRIMARY KEY (user_id),
    CONSTRAINT UserProfileSettings_User_FK FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Movie (
    movie_id INT,
    title VARCHAR2(255) NOT NULL,
    release_date DATE,
    duration INT,
    language VARCHAR2(10),
    image_url VARCHAR2(500),
    avg_rating NUMBER(3,1),

    CONSTRAINT Movie_PK PRIMARY KEY (movie_id)
);

CREATE TABLE MovieCast (
    cast_id INT,
    first_name VARCHAR2(100),
    last_name VARCHAR2(100),
    role VARCHAR2(255),

    CONSTRAINT MovieCast_PK PRIMARY KEY (cast_id)
);

CREATE TABLE Platform (
    platform_id INT,
    name VARCHAR2(100) NOT NULL UNIQUE,
    url VARCHAR2(500),

    CONSTRAINT Platform_PK PRIMARY KEY (platform_id)
);

CREATE TABLE Genre (
    genre_id INT,
    genre_name VARCHAR2(100) NOT NULL UNIQUE,

    CONSTRAINT Genre_PK PRIMARY KEY (genre_id)
);

CREATE TABLE Tag (
    tag_id INT,
    tag_text VARCHAR2(100) NOT NULL UNIQUE,

    CONSTRAINT Tag_PK PRIMARY KEY (tag_id)
);

CREATE TABLE WatchList (
    watchlist_id INT,
    user_id VARCHAR2(36),
    title VARCHAR2(100) NOT NULL,
    date_created DATE DEFAULT CURRENT_DATE,
    watch_status VARCHAR2(50),

    CONSTRAINT WatchList_PK PRIMARY KEY (watchlist_id),
    CONSTRAINT WatchList_User_FK FOREIGN KEY (user_id) REFERENCES Users(user_id)
);



CREATE TABLE Review (
    review_id INT,
    user_id VARCHAR2(36),
    movie_id INT,
    platform_id INT,
    rating NUMBER(3,1) NOT NULL,
    review_date DATE NOT NULL,
    headline VARCHAR2(255),
    review_text VARCHAR2(4000),
    review_body VARCHAR2(4000),

    CONSTRAINT Review_PK PRIMARY KEY (review_id),
    CONSTRAINT Review_User_FK FOREIGN KEY (user_id) REFERENCES Users(user_id),
    CONSTRAINT Review_Movie_FK FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    CONSTRAINT Review_Platform_FK FOREIGN KEY (platform_id) REFERENCES Platform(platform_id),
    CONSTRAINT Review_UQ UNIQUE (user_id, movie_id, platform_id)
);

CREATE TABLE WatchHistory (
    user_id VARCHAR2(36),
    movie_id INT,
    watch_date DATE,
    device_used VARCHAR2(100),
    duration_watched INT,

    CONSTRAINT WatchHistory_PK PRIMARY KEY (user_id, movie_id, watch_date),
    CONSTRAINT WatchHistory_User_FK FOREIGN KEY (user_id) REFERENCES Users(user_id),
    CONSTRAINT WatchHistory_Movie_FK FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
);

CREATE TABLE Includes (
    watchlist_id INT,
    movie_id INT,

    CONSTRAINT Includes_PK PRIMARY KEY (watchlist_id, movie_id),
    CONSTRAINT Includes_WatchList_FK FOREIGN KEY (watchlist_id) REFERENCES WatchList(watchlist_id),
    CONSTRAINT Includes_Movie_FK FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
);

CREATE TABLE HasMovieCast (
    movie_id INT,
    cast_id INT,
    role VARCHAR2(255),

    CONSTRAINT HasMovieCast_PK PRIMARY KEY (movie_id, cast_id),
    CONSTRAINT HasMovieCast_Movie_FK FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    CONSTRAINT HasMovieCast_Cast_FK FOREIGN KEY (cast_id) REFERENCES MovieCast(cast_id)
);

CREATE TABLE HasTags (
    movie_id INT,
    tag_id INT,

    CONSTRAINT HasTags_PK PRIMARY KEY (movie_id, tag_id),
    CONSTRAINT HasTags_Movie_FK FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    CONSTRAINT HasTags_Tag_FK FOREIGN KEY (tag_id) REFERENCES Tag(tag_id)
);

CREATE TABLE IsGenre (
    movie_id INT,
    genre_id INT,

    CONSTRAINT IsGenre_PK PRIMARY KEY (movie_id, genre_id),
    CONSTRAINT IsGenre_Movie_FK FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    CONSTRAINT IsGenre_Genre_FK FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
);

CREATE TABLE AvailableOn (
    movie_id INT,
    platform_id INT,

    CONSTRAINT AvailableOn_PK PRIMARY KEY (movie_id, platform_id),
    CONSTRAINT AvailableOn_Movie_FK FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    CONSTRAINT AvailableOn_Platform_FK FOREIGN KEY (platform_id) REFERENCES Platform(platform_id)
);
