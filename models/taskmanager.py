# coding: utf-8

import typing
from pydantic import BaseModel


class Scenario(BaseModel):

    id = int
    name_scenario = str
    pickle = bytes


class ScheduleDaily(BaseModel):

    id = int
    sch_month = int
    sch_day = int
    sch_hour = int
    plan_quantity = int
    cur_quantity = int
    pickle_id = int
