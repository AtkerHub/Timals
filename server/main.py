from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData
from models import Base

engine = create_engine("postgresql+psycopg://admin:timmy@localhost:5433/timals-postgres-db", echo=True)

with engine.connect() as connection:
    result = connection.execute(text("select 1;"))
    print(result.one())

Base.metadata.create_all(engine)