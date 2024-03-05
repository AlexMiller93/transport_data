import os
from dotenv import load_dotenv
load_dotenv()

# Установим параметры подключения к базе данных PostGIS
host = os.getenv("DB_HOST") #'localhost'
port = os.getenv("DB_PORT") # 5432
database = 'track_data_db'
user = os.getenv("DB_USER") #'postgres'
password = os.getenv("DB_PASSWORD") #'password'