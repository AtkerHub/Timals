from sqlalchemy import create_engine
from sqlalchemy import text

from sqlalchemy.orm import sessionmaker



#   Connecting with database (Postgre)
engine = create_engine("postgresql+psycopg://admin:timmy@localhost:5433/timals-postgres-db", echo=True)

# - - - Connection test - - - 
#with engine.connect() as connection:
#    result = connection.execute(text("select 1;"))
#    print(result.one())


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