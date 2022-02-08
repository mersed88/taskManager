# coding: utf-8

from datetime import datetime
from typing import Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.tables import ScheduleDaily
from settings.config import logger


async def get_task_by_worker(session: Session, id: Union[str, int]) -> ScheduleDaily:
    """
    Получение задания
    :param session: сессия с БД
    :param id: номер воркера
    :return: Первое свободное задание
    """
    try:
        current_datetime = datetime.now()
        logger.info(f"Get task")
        stmt = select(ScheduleDaily). \
            where(ScheduleDaily.sch_month == current_datetime.month). \
            where(ScheduleDaily.sch_day == current_datetime.day). \
            where(ScheduleDaily.sch_hour == current_datetime.hour)
        print(current_datetime.month, current_datetime.day, current_datetime.hour)
        result = await session.execute(stmt)
        print(result.one())
        # print(type(result))
        return result.one()


    except Exception as e:
        logger.error(f"Failed get task \n {e}")
        return ScheduleDaily()
