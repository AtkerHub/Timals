from typing import List, Optional
from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Boolean, Date
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
    activities: Mapped[List["Activity"]] = relationship(back_populates="owner")
    activitieslog: Mapped[List["ActivityLog"]] = relationship(back_populates="owner")

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))

    #relationships
    owner: Mapped[Optional["User"]] = relationship(back_populates="categories")
    activities: Mapped[List["Activity"]] = relationship(back_populates="assignment")
    
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

class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))

    #relationships
    owner: Mapped[Optional["User"]] = relationship(back_populates="activities")
    assignment: Mapped[Optional["Category"]] = relationship(back_populates="activities")
    activitieslog: Mapped[List["ActivityLog"]] = relationship(back_populates="dailyactivity")


class ActivityLog(Base):
    __tablename__ = "activitylog"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    activity_id: Mapped[int] = mapped_column(ForeignKey("activity.id"))
    finished: Mapped[bool] = mapped_column(Boolean, default=False)
    date: Mapped[date] = mapped_column(Date)

    #relationships
    owner: Mapped["User"] = relationship(back_populates="activitieslog")
    dailyactivity: Mapped["Activity"] = relationship(back_populates="activitieslog")