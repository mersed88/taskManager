# coding: utf-8

from sqlalchemy import Column, Integer, String, event, LargeBinary, DDL
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
