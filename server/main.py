from models import Base, User
from database import engine, get_db
from schemas import UserCreate

from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session


#tables creations
Base.metadata.create_all(engine)


#   Testing FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Timals says Hello~!"}

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username = user.username, email = user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user