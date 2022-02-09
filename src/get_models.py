# coding: utf-8

from datetime import datetime
from typing import Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.tables import ScheduleDaily, Scenario
from settings.config import logger


def get_task_by_worker(session: Session, id: Union[str, int]) -> ScheduleDaily:
    """
    Получение задания
    1. находим задачу в текущем часе
    2. увеличиваем количество выполненных
    3. отдаем пикл
    :param session: сессия с БД
    :param id: номер воркера
    :return: Первое свободное задание
    """
    try:
        current_datetime = datetime.now()
        logger.info(f"Get task")

        result_sch = session.query(ScheduleDaily.id, ScheduleDaily.pickle_id).\
            filter(ScheduleDaily.sch_month == current_datetime.month).\
            filter(ScheduleDaily.sch_month == current_datetime.month). \
            filter(ScheduleDaily.sch_day == current_datetime.day). \
            filter(ScheduleDaily.sch_hour == current_datetime.hour). \
            filter(ScheduleDaily.plan_quantity > ScheduleDaily.cur_quantity)


        session.query(ScheduleDaily). \
            filter(ScheduleDaily.id == result_sch.one()[0] ). \
            update({"cur_quantity": ScheduleDaily.cur_quantity+1}, synchronize_session='fetch')
        session.commit()

        result = session.query(Scenario.pickle).\
            filter(Scenario.id == result_sch.one()[1])

        return result.one()[0]


    except Exception as e:
        logger.error(f"Failed get task \n {e}")
        return ScheduleDaily()
