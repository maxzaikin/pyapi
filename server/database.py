import sqlalchemy
from databases import Database

DB_URL= 'sqlite:///db.db'
database= Database(DB_URL)
sqlalchemy_engine= sqlalchemy.create_engine(DB_URL)

def get_database() -> Database:
    return database