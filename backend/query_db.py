from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime, and_
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
    print(info.EventName)
    print(info.EventTime)
    print(info.Venue)
    print(info.Address)
    print(info.PageURL)
    print(info.ImageURL)

印出範例：
鳴石樂集樂壇新秀《琴恩飛揚》王唯恩小提琴獨奏會
2024/07/20 (Sat) 19:30 - 21:00
鳴石音樂空間
台灣台北市100中正區仁愛路二段34號5F
https://www.accupass.com/event/2403091016294643336910?utm_source=web&utm_medium=search_result_&utm_campaign=accu_e_
https://static.accupass.com/eventbanner/2406072310565290498870.jpg
鳴石樂集樂壇新秀《昕昕相惜》 吳昕叡小提琴獨奏會
2024/07/06 (Sat) 19:30 - 21:00
鳴石音樂空間
台灣台北市100中正區仁愛路二段34號5F
https://www.accupass.com/event/2308160154011909123190?utm_source=web&utm_medium=search_result_&utm_campaign=accu_e_
https://static.accupass.com/eventbanner/2406030950273424381960.jpg
'''


# 用時間+地點搜尋，返回活動全部資訊（名字、時間、展演空間、地址、圖片網址、活動網頁）
# 時間格式為 YYYY-MM-DD
def info_search_by_time_city(time, city):
    session = Session()
    filters = []
    if time == None:
        filters.append(tb_accupass.c.Address.like(f'%{city}%'))
    else:
        filters.append(and_(tb_accupass.c.StartTime <= time, tb_accupass.c.EndTime >= time, tb_accupass.c.Address.like(f'%{city}%')))

    try:
        query = session.query(
            tb_accupass.c.EventName,
            tb_accupass.c.EventTime,
            tb_accupass.c.Venue,
            tb_accupass.c.Address,
            tb_accupass.c.ImageURL,
            tb_accupass.c.PageURL,
            tb_accupass.c.StartTime,
            tb_accupass.c.EndTime
        ).filter(and_(*filters))
        results = query.all()

        # 將查詢結果轉換成字典的列表
        results_dicts = [
            {
                'EventName': result[0],
                'EventTime': result[1],
                'Venue': result[2],
                'Address': result[3],
                'ImageURL': result[4],
                'PageURL': result[5],
                'StartTime': result[6],
                'EndTime': result[7],
            }
            for result in results
        ]

        return results_dicts
    finally:
        session.close()
        
# test = info_search_by_time_city(None,"台北市")





