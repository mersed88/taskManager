# coding: utf-8

from datetime import datetime
from typing import Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.tables import ScheduleDaily, Scenario, DeviceCookies, Profile, Device
from dto.profile import ProfileOut
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
            filter(ScheduleDaily.id == result_sch.one()[0]). \
            update({"cur_quantity": ScheduleDaily.cur_quantity+1}, synchronize_session='fetch')
        session.commit()

        result = session.query(Scenario.pickle).\
            filter(Scenario.id == result_sch.one()[1])

        return result.one()[0]


    except Exception as e:
        logger.error(f"Failed get task \n {e}")
        return None


def get_profile_by_worker(session: Session, id: Union[str, int]) -> Profile:
    """
    Получение задания
    1. находим свободный профиль
    2. проставляем признак - занят
    3. отдаем профиль
    :param session: сессия с БД
    :param id: номер воркера
    :return: Первый свободный профиль

    {
        "profile": {
            "id": 1,
            "nick_name": "meta-first",
            "gender": "male",
            "age": 25,
            "region": null,
            "device_id": 1,
            "active": false
        },
        "device": {
            "id": 1,
            "device_type": "mobile",
            "screen_size": "375*812",
            "os": "Iphone X",
            "browser": "chrome",
            "device_cookies_id": 1
        },
        "deviceCookies": {
            "id": 1,
            "device_cookies": "hfkfhdhfdhjdfjhfdhjdkfhjdkfhjfdhjfdjhdkf",
            "last_update": null,
            "valid": null
        }
    }

    """

    try:
        current_datetime = datetime.now()
        logger.info(f"Get profile")

        result_profile = session.query(Profile.id, Profile.device_id, Profile.nick_name, Profile.active, Profile.age, Profile.gender).\
            filter(Profile.active == False)
        print(result_profile.one())

        result_device = session.query(Device.id, Device.os, Device.browser, Device.device_type, Device.screen_size, Device.device_cookies_id).\
            filter(Device.id == result_profile.one()[1])
        print(result_device.one())

        result_cookies = session.query(DeviceCookies.id, DeviceCookies.device_cookies, DeviceCookies.is_valid, DeviceCookies.last_update).\
            filter(DeviceCookies.id == result_device.one()[5])
        print(result_cookies.one())

        # session.query(Profile). \
        #     filter(Profile.id == result_profile.one()[0]). \
        #     update({"active": True}, synchronize_session='fetch')
        # session.commit()

        result = ProfileOut(profile=result_profile.one(), device=result_device.one(), deviceCookies=result_cookies.one())

        return result


    except Exception as e:
        logger.error(f"Failed get task \n {e}")
        return None