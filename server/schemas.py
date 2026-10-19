from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date

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


class ActivityCreate(BaseModel):
    name: str
    user_id: int | None
    category_id: int | None

class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_id: int | None
    category_id: int | None


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

