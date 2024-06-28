from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os


# PostgreSQL connection details
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = os.environ.get('db_endpoint')
USER = os.environ.get('db_user')
PASSWORD = os.environ.get('db_pwd')
PORT = 5432
DATABASE = os.environ.get('db_name')

# Create SQLAlchemy engine
engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}')


# Reflect the table structure
metadata = MetaData()
metadata.reflect(bind=engine)

# Get the table object
tb_accupass = metadata.tables['tb_accupass']

# Create a session
Session = sessionmaker(bind=engine)

# 簡單測試用（用關鍵字搜尋返回活動名稱）
def search_events(keyword):
    session = Session()
    try:
        # Example query: Get EventName where EventName contains the keyword
        query = session.query(tb_accupass.c.EventName).filter(tb_accupass.c.EventName.like(f'%{keyword}%'))
        results = query.all()
        return str(results)
    finally:
        session.close()

# 用關鍵字搜尋活動名稱，返回活動全部資訊（名字、時間、展演空間、地址、圖片網址、活動網頁）
def info_search_by_name(keyword):
    session = Session()
    try:
        query = session.query(
            tb_accupass.c.EventName,
            tb_accupass.c.EventTime,
            tb_accupass.c.Venue,
            tb_accupass.c.Address,
            tb_accupass.c.ImageURL,
            tb_accupass.c.PageURL
        ).filter(tb_accupass.c.EventName.like(f'%{keyword}%'))
        results = query.all()
        return results
    finally:
        session.close()

'''
# 使用方式，利用迴圈一一呼叫，再搭配資料庫欄位名稱印出
# all_info 會是list
all_info = info_search_by_name("小提琴")

# info會是 <class 'sqlalchemy.engine.row.Row'>
# info.EventName 會是str
for info in all_info:
    print(type(info))
    print(info.EventName)
    print(info.EventTime)
    print(info.Venue)
    print(info.Address)
    print(info.PageURL)
    print(info.ImageURL)
'''





