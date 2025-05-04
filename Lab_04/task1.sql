CREATE TABLE Artist (
    artist_id INT PRIMARY KEY,
    name char(50) NOT NULL
);

CREATE TABLE Album (
    album_id INT PRIMARY KEY,
    name char(50) NOT NULL,
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
);

CREATE TABLE Track (
    track_id INT PRIMARY KEY,
    name char(50) NOT NULL,
    length TIME,
    album_id INT,
    FOREIGN KEY (album_id) REFERENCES Album(album_id)
);