from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData
from models import Base

from fastapi import FastAPI



engine = create_engine("postgresql+psycopg://admin:timmy@localhost:5433/timals-postgres-db", echo=True)

# - - - Connection test - - - 
#with engine.connect() as connection:
#    result = connection.execute(text("select 1;"))
#    print(result.one())

Base.metadata.create_all(engine)



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Timals says Hello~!"}