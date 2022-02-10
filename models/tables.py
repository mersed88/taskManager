# coding: utf-8

from sqlalchemy import Column, Integer, String, event, LargeBinary, DDL, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from settings.config import schema_db

SCHEMA = schema_db
Base = declarative_base()
from sqlalchemy.schema import CreateSchema

event.listen(Base.metadata, 'before_create', DDL(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}"))


class Scenario(Base):
    __tablename__ = 'scenario'
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, nullable=False)
    name_scenario = Column(String)
    pickle = Column(LargeBinary)
    children = relationship("ScheduleDaily")


class ScheduleDaily(Base):
    __tablename__ = 'schedule_daily'
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, nullable=False)
    sch_month = Column(Integer)
    sch_day = Column(Integer)
    sch_hour = Column(Integer)
    plan_quantity = Column(Integer)
    cur_quantity = Column(Integer)
    pickle_id = Column(Integer, ForeignKey(f'{SCHEMA}.scenario.id'))
    parent = relationship("Scenario", back_populates="children")


class DeviceCookies(Base):
    __tablename__ = 'devicecookies'
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, nullable=False)
    device_cookies = Column(LargeBinary)
    last_update = Column(DateTime)
    is_valid = Column(Boolean)



class Device(Base):
    __tablename__ = 'device'
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, nullable=False)
    device_type = Column(String)
    screen_size = Column(String)
    os = Column(String)
    browser = Column(String)
    device_cookies_id = Column(Integer, ForeignKey(f'{SCHEMA}.devicecookies.id'))



class Profile(Base):
    __tablename__ = 'profile'
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, nullable=False)
    nick_name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    region = Column(String)
    device_id = Column(Integer, ForeignKey(f'{SCHEMA}.device.id'))
    active = Column(Boolean)


