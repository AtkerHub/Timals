from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine("postgresql+psycopg://admin:timmy@localhost:5433/timals-postgres-db")

with engine.connect() as connection:
    result = connection.execute(text("select 1;"))
    print(result.one())
