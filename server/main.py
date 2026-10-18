#imports from/connected with files
from models import Base, User, Category, TimerPreset
from database import engine, get_db
from schemas import UserCreate, UserResponse
from schemas import CategoryCreate, CategoryResponse
from schemas import TimerPresetCreate, TimerPresetResponse

#imports from/connected with API
from fastapi import FastAPI, Depends, HTTPException

#imports from/connected with Database/SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import select

#imports from/connected with others
from typing import List


#tables creations
Base.metadata.create_all(engine)


#   Testing FastAPI
app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Timals says Hello~!"}

@app.get("/categories/", response_model=List[CategoryResponse])
async def read_categories(db: Session = Depends(get_db)):
    return db.scalars(select(Category)).all() 

@app.get("/categories/{category_id}", response_model=CategoryResponse)
async def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.scalar(select(Category).where(Category.id == category_id)).first()

    if db_category is None:
        raise HTTPException(status_code = 404, detail="Category not found")
    
    return db_category





@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username = user.username, 
        email = user.email,
        password = user.password,
        first_name = user.first_name,
        last_name = user.last_name)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/categories/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(
        name = category.name,
        user_id = category.user_id)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

@app.post("/timer_presets/", response_model=TimerPresetResponse)
async def create_timer_preset(timer_preset: TimerPresetCreate, db: Session = Depends(get_db)):
    db_timer_preset = TimerPreset(
        name = timer_preset.name,
        worktime = timer_preset.worktime,
        breaktime = timer_preset.breaktime,
        resttime = timer_preset.resttime,
        cycle = timer_preset.cycle,
        user_id = timer_preset.user_id)

    db.add(db_timer_preset)
    db.commit()
    db.refresh(db_timer_preset)

    return db_timer_preset