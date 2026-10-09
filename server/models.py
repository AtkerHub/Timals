from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str]
    password: Mapped[str]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]

    #relationships
    categories: Mapped[List["Category"]] = relationship(back_populates="owner")
    timer_presets: Mapped[List["TimerPreset"]] = relationship(back_populates="owner")

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))

    #relationships
    owner: Mapped[Optional["User"]] = relationship(back_populates="categories")

class TimerPreset(Base):
    __tablename__ = "timerpreset"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    worktime: Mapped[int]
    breaktime: Mapped[int]
    resttime: Mapped[int]
    cycle: Mapped[int]
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))

    #relationships
    owner: Mapped[Optional["User"]] = relationship(back_populates="timer_presets")
