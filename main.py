# coding: utf-8


import json
import hashlib

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from dto.worker import WorkerIn, WorkerOut
from settings.config import host, port
from src.get_models import get_task_by_worker
from src.init_db import init_db, get_session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get('/healthcheck')
async def HealthCheck():
    """Функция проверки что сервис работает"""
    return JSONResponse(status_code=200, content={})


# @app.post('/GetEpkIdByPhone', status_code=200, response_model=UcpId)
# async def get_epk_id_by_phone(phone: WorkerIn, session: Session = Depends(get_session)):
#     result = await get_epk_by_phone(session=session, phone=phone.phone)
#
#     if not result:
#         return UcpId(error_code="not_found")
#
#     return result


@app.post('/GetTask', status_code=200, response_model=WorkerOut)
async def get_task(worker: WorkerIn, session: Session = Depends(get_session)):
    result = await get_task_by_worker(session=session, id=worker.id)

    return result

if __name__ == '__main__':
    uvicorn.run(app, host=str(host), port=int(port), debug=False)
