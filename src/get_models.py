# coding: utf-8

import hashlib

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.tables import ScheduleDaily
from settings.config import logger
from datetime import datetime


async def get_task_by_worker(session: Session, id: str) -> ScheduleDaily:
    """
    Получение задания
    :param session: сессия с БД
    :param id: номер воркера
    :return: Первое свободное задание
    """
    try:
        current_datetime = datetime.now()
        logger.info(f"Get task")
        stmt = select(ScheduleDaily.pickle_id).\
        where(ScheduleDaily.sch_month == current_datetime.month).\
        where(ScheduleDaily.sch_day == current_datetime.day).\
        where(ScheduleDaily.sch_hour == current_datetime.hour)
        result = await session.execute(stmt)
        return result.first()

    except Exception as e:
        logger.error(f"Failed get task \n {e}")
        return ScheduleDaily()