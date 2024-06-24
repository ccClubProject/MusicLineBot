-- init.sql schema
-- 定義資料庫Table Schema(有哪些欄位以及資料型態），一個網站一個table

CREATE TABLE IF NOT EXISTS tb_accupass (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName VARCHAR(255) NOT NULL,
    EventTime VARCHAR(255), -- 呈現給使用者看的時間格式
    Venue VARCHAR(255),
    [Address] VARCHAR(255),
    Artists VARCHAR(255),
    ImageURL VARCHAR(1000),
    PageURL VARCHAR(1000),
    StartTime DATETIME, -- 活動開始時間，DATETIME時間格式，用來query活動用的
    EndTime DATETIME -- 活動結束時間，DATETIME時間格式，用來query活動用的
);

CREATE TABLE IF NOT EXISTS tb_kktix (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName VARCHAR(255) NOT NULL,
    EventTime VARCHAR(255),
    Venue VARCHAR(255),
    [Address] VARCHAR(255),
    Artists VARCHAR(255),
    ImageURL VARCHAR(1000),
    PageURL VARCHAR(1000),
    StartTime DATETIME,
    EndTime DATETIME
);

CREATE TABLE IF NOT EXISTS tb_indievox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName VARCHAR(255) NOT NULL,
    EventTime VARCHAR(255),
    Venue VARCHAR(255),
    [Address] VARCHAR(255),
    Artists VARCHAR(255),
    ImageURL VARCHAR(1000),
    PageURL VARCHAR(1000),
    StartTime DATETIME,
    EndTime DATETIME
);

CREATE TABLE IF NOT EXISTS tb_tixcraft (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName VARCHAR(255) NOT NULL,
    EventTime VARCHAR(255),
    Venue VARCHAR(255),
    [Address] VARCHAR(255),
    Artists VARCHAR(255),
    ImageURL VARCHAR(1000),
    PageURL VARCHAR(1000),
    StartTime DATETIME,
    EndTime DATETIME
);