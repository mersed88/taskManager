# coding: utf-8


import json
import hashlib

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from dto.worker import WorkerIn, WorkerOut
from dto.profile import ProfileIn, ProfileOut
from settings.config import host, port
from src.get_models import get_task_by_worker
from src.get_models import get_profile_by_worker
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


@app.get('/GetTask', status_code=200)
async def get_task(worker: WorkerIn, session: Session = Depends(get_session)):
    result = get_task_by_worker(session=session, id=worker.id)
    res_js = WorkerOut(pickle=result)
    if result:
        return PlainTextResponse(res_js.pickle)
    else:
        return JSONResponse(status_code=204, content=None)
        # HTMLResponse(content=None, status_code=300)

    # JSONResponse(status_code=200, content=result)

@app.get('/GetProfile', status_code=200, response_model=ProfileOut)
async def get_task(profile: ProfileIn, session: Session = Depends(get_session)):
    result = get_profile_by_worker(session=session, id=profile.id)
    # res_js = ProfileOut(result)
    if result:
        return result
    else:
        return JSONResponse(status_code=204, content=None)



if __name__ == '__main__':
    uvicorn.run(app, host=str(host), port=int(port), debug=False)
