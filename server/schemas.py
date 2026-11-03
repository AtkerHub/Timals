from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime, time

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str | None
    last_name: str | None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    #password - not displayed here, safety reasons
    first_name: str | None
    last_name: str | None

    # Note for future: "None" in here; "null" in JSON


class CategoryCreate(BaseModel):
    name: str
    user_id: int | None

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_id: int | None

class CategoryUpdate(BaseModel):
    name: str | None = None


class TimerPresetCreate(BaseModel):
    name: str
    worktime: int
    breaktime: int
    resttime: int
    cycle: int
    user_id: int | None

class TimerPresetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    worktime: int
    breaktime: int
    resttime: int
    cycle: int
    user_id: int | None

class TimerPresetUpdate(BaseModel):
    name: str | None = None
    worktime: int | None = None
    breaktime: int | None = None
    resttime: int | None = None
    cycle: int | None = None


class ActivityCreate(BaseModel):
    name: str | None
    user_id: int | None
    category_id: int | None

class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_id: int | None
    category_id: int | None

class ActivityUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None


class ActivityLogCreate(BaseModel):
    user_id: int
    activity_id: int
    finished: bool = False
    date: date

class ActivityLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    activity_id: int
    finished: bool
    date: date

class ActivityLogUpdate(BaseModel):
    finished: bool


class CalendarReminderCreate(BaseModel):
    minutes_before: int

class CalendarReminderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    minutes_before: int | None

class CalendarReminderUpdate(BaseModel):
    id: int | None = None
    minutes_before: int | None = None


class CalendarEventCreate(BaseModel):
    name: str | None
    user_id: int
    category_id: int | None
    start_time: datetime
    end_time: datetime
    whole_day: bool
    repeat: str | None
    note: str | None
    place: str | None
    calendarreminders: list[CalendarReminderCreate] | None

class CalendarEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str | None
    user_id: int
    category_id: int | None
    start_time: datetime
    end_time: datetime
    whole_day: bool
    repeat: str | None
    note: str | None
    place: str | None
    calendarreminders: list[CalendarReminderResponse] | None

class CalendarEventSimpleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str | None
    user_id: int
    category_id: int | None
    start_time: datetime
    end_time: datetime

class CalendarEventUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    whole_day: bool | None = None
    repeat: str | None = None
    note: str | None = None
    place: str | None = None
    calendarreminders: list[CalendarReminderUpdate] | None = None