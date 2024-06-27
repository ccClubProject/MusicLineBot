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

def search_events(keyword):
    session = Session()
    try:
        # Example query: Get EventName where EventName contains the keyword
        query = session.query(tb_accupass.c.EventName).filter(tb_accupass.c.EventName.like(f'%{keyword}%'))
        results = query.all()
        return str(results)
    finally:
        session.close()

