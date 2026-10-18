from pydantic import BaseModel, EmailStr, ConfigDict

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