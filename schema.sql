-- Disable checks to create the tables in any order
PRAGMA foreign_keys = OFF;

-- movie table with enriched attributes from the ER diagram
CREATE TABLE movie (
    id INTEGER PRIMARY KEY,
    title TEXT,
    original_title TEXT,
    overview TEXT,
    tagline TEXT,
    release_date TEXT,
    budget INTEGER,
    revenue INTEGER,
    runtime REAL,
    original_language TEXT,
    popularity REAL,
    homepage TEXT,
    adult INTEGER DEFAULT 0
);

-- genre table
CREATE TABLE genre (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- productioncompany table
CREATE TABLE productioncompany (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- collection table
CREATE TABLE collection (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- keyword table
CREATE TABLE keyword (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- movie_cast table updated with gender and person_id
CREATE TABLE movie_cast (
    cid INTEGER PRIMARY KEY, -- This acts as the unique credit ID
    movie_id INTEGER,
    person_id INTEGER, -- Unique ID for the actor
    name TEXT,
    character TEXT,
    gender INTEGER, -- Usually 1 for female, 2 for male
    FOREIGN KEY (movie_id) REFERENCES movie(id)
);

-- movie_crew table updated with department, job, and gender
CREATE TABLE movie_crew (
    cid INTEGER PRIMARY KEY, -- Unique credit ID
    movie_id INTEGER,
    person_id INTEGER, -- Unique ID for the crew member
    name TEXT,
    department TEXT,
    job TEXT,
    gender INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movie(id)
);

-- ratings table (using a composite primary key)
CREATE TABLE ratings (
    user_id INTEGER,
    movie_id INTEGER,
    rating REAL,
    timestamp INTEGER,
    PRIMARY KEY (user_id, movie_id),
    CONSTRAINT fk_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id)
);

-- Junction table for movies and collections (M:N or 1:N depending on business logic)
CREATE TABLE belongsTocollection (
    movie_id INTEGER,
    collection_id INTEGER,
    PRIMARY KEY (movie_id, collection_id),
    CONSTRAINT fk_movieid FOREIGN KEY (movie_id) REFERENCES movie(id),
    CONSTRAINT fk_collectionid FOREIGN KEY (collection_id) REFERENCES collection(id)
);

-- Junction table for movies and genres
CREATE TABLE hasGenre (
    movie_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (movie_id, genre_id),
    CONSTRAINT fk_moveId FOREIGN KEY (movie_id) REFERENCES movie(id),
    CONSTRAINT fk_genreId FOREIGN KEY (genre_id) REFERENCES genre(id)
);

-- Junction table for movies and production companies
CREATE TABLE hasProductioncompany (
    movie_id INTEGER,
    pc_id INTEGER,
    PRIMARY KEY (movie_id, pc_id),
    CONSTRAINT fkMoveId FOREIGN KEY (movie_id) REFERENCES movie(id),
    CONSTRAINT fkProdComp FOREIGN KEY (pc_id) REFERENCES productioncompany(id)
);

-- Junction table for movies and keywords
CREATE TABLE haskeyword (
    movie_id INTEGER,
    keyword_id INTEGER,
    PRIMARY KEY (movie_id, keyword_id),
    CONSTRAINT foreignK_MovieId FOREIGN KEY (movie_id) REFERENCES movie(id),
    CONSTRAINT foreignK_KeywordId FOREIGN KEY (keyword_id) REFERENCES keyword(id)
);

-- Activation of foreign keys
PRAGMA foreign_keys = ON;