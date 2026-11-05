#   Imports from/connected with files
from models import Base, User, Category, TimerPreset, Activity, ActivityLog, CalendarReminder, CalendarEvent
from database import engine, get_db
from schemas import UserCreate, UserResponse
from schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from schemas import TimerPresetCreate, TimerPresetResponse, TimerPresetUpdate
from schemas import ActivityCreate, ActivityResponse, ActivityUpdate
from schemas import ActivityLogCreate, ActivityLogResponse, ActivityLogUpdate
from schemas import CalendarReminderCreate, CalendarReminderResponse, CalendarReminderUpdate
from schemas import CalendarEventCreate, CalendarEventResponse, CalendarEventSimpleResponse, CalendarEventUpdate

#   Imports from/connected with API
from fastapi import FastAPI, Depends, HTTPException

#   Imports from/connected with Database/SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
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
#   GET Methods
@app.get("/")
async def root():
    return {"message": "Timals says Hello~!"}


@app.get("/categories/", response_model=List[CategoryResponse])
async def read_categories(user_id: int , db: Session = Depends(get_db)):
    return db.scalars(select(Category)
                      .where(Category.user_id == user_id)).all()

@app.get("/categories/{category_id}", response_model=CategoryResponse)
async def read_category(category_id: int, user_id: int, db: Session = Depends(get_db)):
    db_category = db.scalar(select(Category)
                            .where(
                                and_(
                                    Category.user_id == user_id,
                                    Category.id == category_id
                                    )
                                ))

    if db_category is None:
        raise HTTPException(status_code = 404, detail = "Category not found")
    
    return db_category


@app.get("/timer_presets/", response_model=List[TimerPresetResponse])
async def read_timer_presets(user_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(TimerPreset)
                      .where(TimerPreset.user_id == user_id)).all()

@app.get("/timer_presets/{timer_preset_id}", response_model=TimerPresetResponse)
async def read_timer_preset(timer_preset_id: int, user_id: int, db: Session = Depends(get_db)):
    db_timer_preset = db.scalar(select(TimerPreset)
                                .where(
                                    and_(
                                        TimerPreset.user_id == user_id,
                                        TimerPreset.id == timer_preset_id
                                        )
                                ))
    
    if db_timer_preset is None:
        raise HTTPException(status_code = 404, detail = "Timer Preset not found")

    return db_timer_preset


@app.get("/activities/{activity_id}/logs", response_model=List[ActivityLogResponse])
async def read_activity_logs(user_id: int, activity_id: int, range_filter: str | None = "30days", db: Session = Depends(get_db)):
    query = select(ActivityLog).where(and_(ActivityLog.user_id == user_id, ActivityLog.activity_id == activity_id))

    today = date.today()

    if range_filter == "30days":
        start_date = today - timedelta(days=30)
    elif range_filter == "year":
        start_date = date(today.year, 1, 1)
    elif range_filter == "all":
        pass
    else:
        raise HTTPException(status_code = 400, detail = "Bad Request")

    if range_filter != "all":
        query = query.where(ActivityLog.date >= start_date)

    query = query.order_by(ActivityLog.date.asc())

    logs = db.scalars(query).all()
    
    return logs

@app.get("/calendar_events/", response_model=List[CalendarEventSimpleResponse])
async def read_calendar_events(user_id: int, start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    if start_date is None or end_date is None:
        today = date.today()
        first_day_of_month = today.replace(day=1)
    
        days_to_substract = first_day_of_month.weekday()
    
        grid_start_date = first_day_of_month - timedelta(days=days_to_substract)
        grid_end_date = grid_start_date + timedelta(days=41)

        start_date = grid_start_date
        end_date = grid_end_date

    limit_date = end_date + timedelta(days=1)

    query = select(CalendarEvent).where(CalendarEvent.user_id == user_id)

    query = query.where(CalendarEvent.start_time >= start_date)
    query = query.where(CalendarEvent.end_time < limit_date)

    db_events = db.scalars(query).all()

    return db_events

@app.get("/calendar_events/{event_id}", response_model=CalendarEventResponse)
async def read_calendar_event(user_id: int, event_id: int, db: Session = Depends(get_db)):
    query = select(CalendarEvent).where(
        CalendarEvent.user_id == user_id,
        CalendarEvent.id == event_id).options(
            selectinload(CalendarEvent.calendarreminders)
        ) 

    db_event = db.scalar(query)

    if db_event is None:
        raise HTTPException(status_code = 404, detail = "Calendar Event not found")

    return db_event


#   POST Methods
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

@app.post("/calendar_events/", response_model=CalendarEventResponse)
async def create_calendar_event(event: CalendarEventCreate, db: Session = Depends(get_db)):
    db_reminders = []

    if event.calendarreminders:
        for reminder in event.calendarreminders:
            db_reminders.append(CalendarReminder(
                minutes_before = reminder.minutes_before))

    db_event = CalendarEvent(
        name = event.name,
        user_id = event.user_id,
        category_id = event.category_id,
        start_time = event.start_time,
        end_time = event.end_time,
        whole_day = event.whole_day,
        repeat = event.repeat,
        note = event.note,
        place = event.place,
        calendarreminders = db_reminders
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event



#   PATCH Methods
@app.patch("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.scalar(select(Category)
                            .where(Category.id == category_id))

    if db_category is None:
        raise HTTPException(status_code = 404, detail = "Category not found")       

    update_data = category_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)

    return db_category

@app.patch("/timer_presets/{timer_preset_id}", response_model=TimerPresetResponse)
async def update_timer_preset(timer_preset_id: int, timer_preset_update: TimerPresetUpdate, db: Session = Depends(get_db)):
    db_timer_preset = db.scalar(select(TimerPreset)
                            .where(TimerPreset.id == timer_preset_id))

    if db_timer_preset is None:
        raise HTTPException(status_code = 404, detail = "Timer Preset not found")       

    update_data = timer_preset_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_timer_preset, key, value)

    db.commit()
    db.refresh(db_timer_preset)

    return db_timer_preset

@app.patch("/activities/{activity_id}", response_model=ActivityResponse)
async def update_activity(activity_id: int, activity_update: ActivityUpdate, db: Session = Depends(get_db)):
    db_activity = db.scalar(select(Activity)
                            .where(Activity.id == activity_id))

    if db_activity is None:
        raise HTTPException(status_code = 404, detail = "Activity not found")       

    update_data = activity_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_activity, key, value)

    db.commit()
    db.refresh(db_activity)

    return db_activity

@app.patch("/activity_logs/{activity_log_id}", response_model=ActivityLogResponse)
async def update_actvitiy_log(activity_log_id: int, activity_log_update: ActivityLogUpdate, db: Session = Depends(get_db)):
    db_log = db.scalar(select(ActivityLog)
                       .where(ActivityLog.id == activity_log_id))

    if db_log is None:
        raise HTTPException(status_code = 404, detail = "Activity Log not found")

    update_data = activity_log_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_log, key, value)

    db.commit()
    db.refresh(db_log)

    return db_log

@app.patch("/calendar_events/{event_id}", response_model=CalendarEventResponse)
async def update_calendar_event(event_id: int, event_update: CalendarEventUpdate, db: Session = Depends(get_db)):
    db_event = db.scalar(select(CalendarEvent)
                            .where(CalendarEvent.id == event_id)
                            .options(
                                selectinload(CalendarEvent.calendarreminders)))

    if db_event is None:
        raise HTTPException(status_code = 404, detail = "Timer Preset not found")       

    #update_data (dict variable)
    update_data = event_update.model_dump(exclude_unset=True)

    # no nested values (calendar reminders) in update_data 
    # (updated calendar reminders are here) (dict variable)
    incoming_reminders = update_data.pop("calendarreminders", None)

    for key, value in update_data.items():
        setattr(db_event, key, value)


    if incoming_reminders is not None:
        incoming_id = set()

        for inc_reminder in incoming_reminders:
            if inc_reminder.get("id") is not None:
                incoming_id.add(inc_reminder["id"])

        for existing_reminder in db_event.calendarreminders[:]:
            if existing_reminder.id not in incoming_id:
                db.delete(existing_reminder)

        for inc_reminder in incoming_reminders:
            if inc_reminder.get("id") is not None:
                for existing_reminder in db_event.calendarreminders:
                    if existing_reminder.id == inc_reminder["id"]:
                        existing_reminder.minutes_before = inc_reminder["minutes_before"]
                        break
            else:
                db_event.calendarreminders.append(CalendarReminder(
                    minutes_before = inc_reminder["minutes_before"]))
            
    db.commit()
    db.refresh(db_event)

    return db_event

#   DELETE Methods
@app.delete("/categories/{category_id}")
async def delete_category(user_id: int, category_id: int, db: Session = Depends(get_db)):
    db_category = db.scalar(select(Category)
                            .where(and_(
                                Category.user_id == user_id,
                                Category.id == category_id
                            )))
    if db_category is None:
        raise HTTPException(status_code = 404, detail = "Category not found")

    db.delete(db_category)
    db.commit()

    return {"detail": "Category successfully deleted"}

@app.delete("/timer_presets/{timer_preset_id}")
async def delete_timer_preset(user_id: int, timer_preset_id: int, db: Session = Depends(get_db)):
    db_timer_preset = db.scalar(select(TimerPreset)
                                .where(and_(
                                    TimerPreset.user_id == user_id,
                                    TimerPreset.id == timer_preset_id
                                )))

    if db_timer_preset is None:
        raise HTTPException(status_code = 404, detail = "Timer Preset not found")

    db.delete(db_timer_preset)
    db.commit()


    return {"detail": "TimerPreset successfully deleted"}

@app.delete("/activities/{activity_id}")
async def delete_activity(user_id: int, activity_id: int, db: Session = Depends(get_db)):
    db_activity = db.scalar(select(Activity)
                            .where(and_(
                                Activity.user_id == user_id,
                                Activity.id == activity_id
                            )))

    if db_activity is None:
        raise HTTPException(status_code = 404, detail = "Activity not found")

    db.delete(db_activity)
    db.commit()

    return {"detail": "Activity successfully deleted"}

@app.delete("/activity_logs/{activity_log_id}")
async def delete_activity_log(user_id: int, activity_log_id: int, db: Session = Depends(get_db)):
    db_activity_log = db.scalar(select(ActivityLog)
                                .where(and_(
                                    ActivityLog.user_id == user_id,
                                    ActivityLog.id == activity_log_id
                                )))
    if db_activity_log is None:
        raise HTTPException(status_code = 404, detail = "Activity Log not found")

    db.delete(db_activity_log)
    db.commit

    return {"detail": "Activity Log successfully deleted"}
    

@app.delete("/calendar_events/{event_id}")
async def delete_calendar_event(user_id: int, event_id: int, db: Session = Depends(get_db)):
    db_event = db.scalar(select(CalendarEvent)
                                .where(and_(
                                    CalendarEvent.user_id == user_id, 
                                    CalendarEvent.id == event_id)))

    if db_event is None:
            raise HTTPException(status_code = 404, detail = "Calendar Event not found")

    db.delete(db_event)
    db.commit()

    return {"detail": "Calendar Event successfully deleted"}