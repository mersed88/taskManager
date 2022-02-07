# coding: utf-8

import logging
import requests
import os
from cmreslogging.handlers import CMRESHandler
import yaml
import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# [%(asctime)s]-%(levelname)#-8s  %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S',
                    level=logging.INFO)
logger.setLevel(logging.DEBUG)

headers = {'Content-Type': 'application/json;charset=UTF-8'}

HOST = str(os.getenv('HOST', '0.0.0.0'))
PORT = int(os.getenv('PORT', 8080))

ELASTIC_HOST = str(os.getenv('ELASTIC_HOST', '---'))
CONFIG_URL = os.getenv('CONFIG_URL', '---')
NAME_PROJECT = os.getenv('NAME_PROJECT', 'taskManager')
PYTHON_PROFILES_ACTIVE = os.getenv('PYTHON_PROFILES_ACTIVE', 'dev')
BRANCH = os.getenv('BRANCH', 'master')
URL_PROFILE = CONFIG_URL + '/' + NAME_PROJECT + '-' + PYTHON_PROFILES_ACTIVE + '.yml'
elastic_host = ELASTIC_HOST
elastic_host = elastic_host if not 'http://' in elastic_host else elastic_host.replace('http://', '')
# elastic_host, elastic_port = elastic_host.split(':')

handler = None
# try:
#     handler = CMRESHandler(hosts=[{'host': elastic_host, 'port': elastic_port}], auth_type=CMRESHandler.AuthType.NO_AUTH,
#                            es_index_name=NAME_PROJECT,
#                            index_name_frequency=CMRESHandler.IndexNameFrequency.DAILY,
#                            es_additional_fields={'timestamp': datetime.datetime.now()}
#                            )
#     logger.addHandler(handler)
# except Exception as e:
#     handler = None

logger.info(f'''urlProfile = {URL_PROFILE}''')
task = yaml.load(requests.get(URL_PROFILE).text, Loader=yaml.Loader)

try:

    user_postgres = os.getenv("USER_POSTGRES", "postgres")
    password_postgres = os.getenv("PASSWORD_POSTGRES", "4265d93e7d8aa3893fc899f4414fbef9d2eddc5913ec76201ae11bb8fc1eea89")
    host_postgres = os.getenv("HOST_POSTGRES", "ec2-52-214-125-106.eu-west-1.compute.amazonaws.com")
    port_postgres = os.getenv("PORT_POSTGRES", "5432")
    db_postgres = os.getenv("DB_POSTGRES", "dei9is9m72ghmj")

    engine_string = f'postgresql+asyncpg://{user_postgres}:{password_postgres}@{host_postgres}:{port_postgres}/{db_postgres}'
    schema_db = os.getenv("SCHEMA", "taskManager")

    host = str("0.0.0.0")
    port = int(8080)

except Exception as e:
    logger.error(e)