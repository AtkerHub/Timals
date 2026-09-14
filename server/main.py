from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData
from models import Base

from fastapi import FastAPI

from sqlalchemy.orm import sessionmaker


#   Connecting with database (Postgre)
engine = create_engine("postgresql+psycopg://admin:timmy@localhost:5433/timals-postgres-db", echo=True)

# - - - Connection test - - - 
#with engine.connect() as connection:
#    result = connection.execute(text("select 1;"))
#    print(result.one())

Base.metadata.create_all(engine)


#   Testing FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Timals says Hello~!"}


#   Session 
SessionLocal = sessionmaker(bind=engine)

def get_db():
    #opening of a session
    db = SessionLocal()
    try:
        #waiting for operations on db from e.g. FastAPI, "stopping iteration"
        yield db
    finally:
        #closure of session so it wont make any error or incorrect data input
        db.close()