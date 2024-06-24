-- init.sql schema
CREATE TABLE IF NOT EXISTS ACCUPASS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName VARCHAR(255) NOT NULL,
    EventTime TEXT,
    Venue VARCHAR(255),
    Address VARCHAR(255),
    Artists VARCHAR(255),
    ImageURL VARCHAR(255),
    PageURL VARCHAR(255),
    StartTime TEXT,
    EndTime TEXT
);

CREATE TABLE IF NOT EXISTS KKTIX (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName VARCHAR(255) NOT NULL,
    EventTime TEXT,
    Venue VARCHAR(255),
    Address VARCHAR(255),
    Artists VARCHAR(255),
    ImageURL VARCHAR(255),
    PageURL VARCHAR(255),
    StartTime TEXT,
    EndTime TEXT
);
