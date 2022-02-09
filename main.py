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
def on_startup():
    init_db()


@app.get('/healthcheck')
async def HealthCheck():
    """Функция проверки что сервис работает"""
    return JSONResponse(status_code=200, content={})


@app.get('/GetTask', status_code=200, response_model=WorkerOut)
async def get_task(worker: WorkerIn, session: Session = Depends(get_session)):
    result = get_task_by_worker(session=session, id=worker.id)
    res_js = WorkerOut(pickle=str(result))
    return res_js
    # JSONResponse(status_code=200, content=result)


if __name__ == '__main__':
    uvicorn.run(app, host=str(host), port=int(port), debug=False)
