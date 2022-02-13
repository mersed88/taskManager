FROM python:3.9-rc-slim

WORKDIR /home/app
COPY requirements.txt  requirements.txt

RUN pip install -r requirements.txt

COPY alembic alembic
COPY dto dto
COPY models models
COPY settings settings
COPY src src
COPY alembic.ini alembic.ini
COPY main.py main.py

CMD python main.py