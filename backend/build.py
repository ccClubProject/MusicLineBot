import sqlite3
import pandas as pd

from flask import g
import sys

# 不知為何正常import他抓不到，所以用os去指定路徑
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraping.accupass import scrap_accupass

# 給定DB及schema路徑
SQLITE_DB_PATH = './backend/scraped.db'
SQLITE_DB_SCHEMA = './backend/init.sql'


# 建立資料庫table及儲存爬蟲資訊
def create_table():
    # 讀取DB Schema
    with open(SQLITE_DB_SCHEMA) as f:
        create_db_sql = f.read()

    # DB 連線
    conn = sqlite3.connect(SQLITE_DB_PATH)

    # 根據DB Schema建立Table
    conn.executescript(create_db_sql)

    # 由accupass.py內的函式取得爬蟲dataframe
    df = scrap_accupass()

    # 將爬蟲資料寫入Table並開啟foreign keys模式
    conn.execute("PRAGMA foreign_keys = ON")

    # 將accupass爬蟲資料存入DB
    df.to_sql('tb_accupass', conn, if_exists='append', index=False)


# 讀取資料庫資料
def get_data(keyword):
     # 建立DB連線
     db = sqlite3.connect(SQLITE_DB_PATH)
     cursor = db.cursor()

     # 根據關鍵字找尋特定資料，並返回EventName欄位
     cursor.execute(f"SELECT EventName FROM 'tb_accupass' WHERE EventName LIKE '%{keyword}%'")
     data = cursor.fetchall()
     return str(data)

# 讀取資料庫資料(日期和地點)
def get_random_music_events(date, location):
     # 建立DB連線
     db = sqlite3.connect(SQLITE_DB_PATH)
     cursor = db.cursor()

     # 根據日期和地點尋特定資料，並返回結果
     query = """
     SELECT StartTime, EndTime, Address 
     FROM tb_accupass 
     WHERE DATE(StartTime) = ? AND Address LIKE ?
     """
     cursor.execute(query, (date, f'%{location}%'))
     data = cursor.fetchall()
     return data

# # create_table()
# print(get_data('爵士'))