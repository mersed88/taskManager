FROM python:3.9-rc-slim

WORKDIR /home/app
COPY alembic alembic
COPY dto dto
COPY models models
COPY settings settings
COPY src src
COPY alembic.ini alembic.ini
COPY main.py main.py
COPY requirements.txt  requirements.txt

RUN pip install -r requirements.txt

CMD python main.py