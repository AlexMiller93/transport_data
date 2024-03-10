import psycopg2
from psycopg2 import OperationalError
import pandas as pd

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Установим параметры подключения к базе данных PostGIS
host = 'localhost'
port = 5435
database = 'track_data'
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

path_to_excel_file = './data/track_data.xlsx'

create_track_table = """
    CREATE TABLE IF NOT EXISTS track_data (
        id: INTEGER,
        longitude NUMERIC(7, -5),
        latitude NUMERIC(7, -5),
        speed INTEGER CHECK (speed >= 0),
        gps_time TIMESTAMP
        vehicle_id INTEGER
    )
"""

def create_connection(db_name: str, db_user:str, db_password:str, db_host:str, db_port:int):
    '''
    Функция создает соединение с БД
    '''
    
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Соединение к БД PostgreSQL прошло успешно")
    except OperationalError as e:
        print(f"Произошла ошибка при создании соединения: \n'{e}' ")
    return connection


def load_data_to_db(host: str, port: int, database: str, user: str, password: str, path: str):
    '''
    Функция записывает данные из excel файла
    '''
    
    # Открываем соединение с базой данных
    conn = create_connection(
        host = host,
        port = port,
        database = database,
        user = user, 
        password = password
        )
    
    conn.autocommit = True
    
    # Создаем таблицу в базе данных PostGIS для хранения данных
    cursor = conn.cursor()

    # cursor.execute("""
    #     COPY track_data (id, longitude, latitude, speed, gps_time, vehicle_id)
    #     FROM path_to_excel_file
    #             """)
    
    try:
        cursor.execute(create_track_table)
        
    except OperationalError  as e:
        print(f'Произошла ошибка при создании таблицы: \n{e}')

    # Загружаем данные из Excel файла в DataFrame
    df = pd.read_excel(path)

    # Вставляем данные из DataFrame в таблицу PostGIS
    for row in df.itertuples():
        
        # Вставляем данные в таблицу
        cursor.execute("""
            INSERT INTO track_data (id, longitude, latitude, speed, gps_time, vehicle_id)
            VALUES (%s, %s, %s, %s, %s, %s);
            """, (row.id, row.longitude, row.latitude, row.speed, row.gps_time, row.vehicle_id))

    # Сохраняем изменения в базе данных
    conn.commit()

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

    return conn


def get_db_connection():
    conn = load_data_to_db(host, port, database, user, password, path_to_excel_file)
    return conn