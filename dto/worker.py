# coding: utf-8

import typing
from pydantic import BaseModel


class WorkerIn(BaseModel):
    """
    Входной POST запрос
    {
        "id": 111
    }
    """
    id: typing.Optional[int]


class WorkerOut(BaseModel):
    """
    Возвращаем ответ
    {
    "pickle": "1474513503099495002"
    }
    """
    pickle: typing.Optional[str, bytes, bytearray]