from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str | None
    last_name: str | None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    #password - not displayed here, safety reasons
    first_name: str | None
    last_name: str | None

    # stwórz nową klasę
    # jedną dla wprowadzania użytkownika
    # drugą do zwracania użytkownika
    # wykorzystaj to EmailStr żeby od razu wykluczyć walidację maili
    # oprócz tego to zwracanie użytkownika musi być bez hasła
    # Note for future "None" here "null" in JSON