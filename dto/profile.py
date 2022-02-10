# coding: utf-8

import typing
from pydantic import BaseModel
import datetime


class ProfileIn(BaseModel):
    """
    Входной POST запрос
    {
        "id": 111
    }
    """
    id: typing.Optional[int]


class ProfileDto(BaseModel):

    id: int
    nick_name: typing.Optional[str]
    gender: typing.Optional[str]
    age: typing.Optional[int]
    region: typing.Optional[str]
    device_id: typing.Optional[int]
    active: typing.Optional[bool]


class DeviceCookiesDto(BaseModel):

    id: typing.Optional[int]
    device_cookies: typing.Optional[bytes]
    last_update: typing.Optional[datetime.datetime]
    is_valid: typing.Optional[bool]



class DeviceDto(BaseModel):

    id: typing.Optional[int]
    device_type: typing.Optional[str]
    screen_size: typing.Optional[str]
    os: typing.Optional[str]
    browser: typing.Optional[str]
    device_cookies_id: typing.Optional[int]


class ProfileOut(BaseModel):

    profile: typing.Optional[ProfileDto]
    device: typing.Optional[DeviceDto]
    deviceCookies: typing.Optional[DeviceCookiesDto]
