# coding: utf-8

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Text, MetaData, DDL, event, Float, JSON, Boolean, Sequence, Identity, \
    Date, LargeBinary
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.types import DateTime

from settings.config import schema_db, engine_string

SCHEMA = schema_db
Base = declarative_base()
event.listen(Base.metadata, 'before_create', DDL(f"Create schema if not exists {SCHEMA}"))

class Scenario(Base):
    __tablename__ = 'scenario'
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, nullable=False)
    name_scenario = Column(String)
    pickle = Column(LargeBinary)
    children = relationship("ScheduleDaily", back_populates="parent")


class ScheduleDaily(Base):
    __tablename__ = 'schedule_daily'
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, nullable=False)
    sch_month = Column(Integer)
    sch_day = Column(Integer)
    sch_hour = Column(Integer)
    pickle_id = Column(Integer, ForeignKey('scenario.id'))
    parent = relationship("Scenario", back_populates="children")


