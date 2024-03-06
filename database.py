import psycopg2
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()

# Установим параметры подключения к базе данных PostGIS
host = 'localhost',
port = 5432,
database = 'track_data',
user = os.getenv("DB_USER"), 
password = os.getenv("DB_PASSWORD")

path_to_excel_file = './data/track_data.xlsx'

def load_data_to_db(host: str, port: int, database: str, user: str, password: str, path: str):
    '''
    Функция записывает данные из excel файла
    '''
    
    # Открываем соединение с базой данных
    conn = psycopg2.connect(
        
        host = host,
        port = port,
        database = database,
        user = user, 
        password = password
        )

    # Создаем таблицу в базе данных PostGIS для хранения данных
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS track_data (
            id: INTEGER,
            longitude NUMERIC(7, -5),
            latitude NUMERIC(7, -5),
            speed INTEGER CHECK (speed >= 0),
            gps_time: TIMESTAMP
            vehicle_id: INTEGER
        );
    """)

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