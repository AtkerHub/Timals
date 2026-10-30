#   Imports from/connected with files
from models import Base, User, Category, TimerPreset, Activity, ActivityLog
from database import engine, get_db
from schemas import UserCreate, UserResponse
from schemas import CategoryCreate, CategoryResponse
from schemas import TimerPresetCreate, TimerPresetResponse
from schemas import ActivityCreate, ActivityResponse
from schemas import ActivityLogCreate, ActivityLogResponse

#   Imports from/connected with API
from fastapi import FastAPI, Depends, HTTPException

#   Imports from/connected with Database/SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_

#   Imports from/connected with others
from typing import List
from datetime import date, timedelta, datetime


#   Tables generating
Base.metadata.create_all(engine)


#   Testing FastAPI
app = FastAPI()


#   Functions
def add_days():
    return None


#   HTTP Methods
@app.get("/")
async def root():
    return {"message": "Timals says Hello~!"}


@app.get("/categories/", response_model=List[CategoryResponse])
async def read_categories(user_id: int | None = None, db: Session = Depends(get_db)):
    return db.scalars(select(Category)
                      .where(
                          or_(Category.user_id == user_id, Category.user_id.is_(None))
                      )).all()

@app.get("/categories/{category_id}", response_model=CategoryResponse)
async def read_category(category_id: int, user_id: int | None = None, db: Session = Depends(get_db)):
    db_category = db.scalar(select(Category)
                            .where(
                                and_(
                                    or_(Category.user_id == user_id, Category.user_id.is_(None)),
                                    Category.id == category_id
                                    )
                                ))

    if db_category is None:
        raise HTTPException(status_code = 404, detail = "Category not found")
    
    return db_category


@app.get("/timer_presets/", response_model=List[TimerPresetResponse])
async def read_timer_presets(user_id: int | None = None, db: Session = Depends(get_db)):
    return db.scalars(select(TimerPreset)
                      .where(
                          or_(TimerPreset.user_id == user_id, TimerPreset.user_id.is_(None))
                      )).all()

@app.get("/timer_presets/{timer_preset_id}", response_model=TimerPresetResponse)
async def read_timer_preset(timer_preset_id: int, user_id: int | None = None, db: Session = Depends(get_db)):
    db_timer_preset = db.scalar(select(TimerPreset)
                                .where(
                                    and_(
                                        or_(TimerPreset.user_id == user_id, TimerPreset.user_id.is_(None)),
                                        TimerPreset.id == timer_preset_id
                                        )
                                ))
    if db_timer_preset is None:
        raise HTTPException(status_code = 404, detail = "Timer Preset not found")

    return db_timer_preset




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

@app.post("/activities/", response_model=ActivityResponse)
async def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = Activity(
        name = activity.name,
        user_id = activity.user_id,
        category_id = activity.category_id)

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity) 

    return db_activity

@app.post("/activities/{activity_id}/generate_logs", response_model=List[ActivityLogResponse])
async def create_activity_logs(activity_id: int, user_id: int, for_days: int, db: Session = Depends(get_db)):
    db_activity = db.scalar(select(Activity)
                            .where(Activity.id == activity_id))
    if db_activity is None:
        raise HTTPException(status_code = 404, detail = "Timer Preset not found")
    
    last_log_date = db.scalar(select(ActivityLog.date)
                             .where(ActivityLog.activity_id == activity_id)
                             .order_by(ActivityLog.date.desc())
                             )

    if last_log_date is None:
        start_date = datetime.today()
    else:
        start_date = last_log_date + timedelta(days = 1)

    logs_to_create = []

    for i in range(for_days):
        new_log = ActivityLog(
            user_id = user_id,
            activity_id = activity_id,
            date = start_date + timedelta(days = i)
        )

        logs_to_create.append(new_log)

    db.add_all(logs_to_create)
    db.commit()
    #No refresh here

    return logs_to_create