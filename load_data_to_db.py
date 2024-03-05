import psycopg2
import pandas as pd

from config import host, port, database, user, password 

# Открываем соединение с базой данных
conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
cursor = conn.cursor()

# Загружаем данные из Excel файла в DataFrame
df = pd.read_excel('./data/track_data.xlsx')


# Создаем таблицу в базе данных PostGIS для хранения данных
cursor.execute("""
    CREATE TABLE IF NOT EXISTS track_data (
        id SERIAL PRIMARY KEY,
        longitude NUMERIC(7, -5),
        latitude NUMERIC(7, -5),
        speed INTEGER CHECK (speed >= 0),
        gps_time: TIMESTAMP
        vehicle_id: INTEGER
    );
""")

# Вставляем данные из DataFrame в таблицу PostGIS
for row in df.itertuples():
    
    # Извлекаем данные из строки
    id = row.id
    longitude = row.longitude
    latitude = row.latitude
    speed = row.speed
    gps_time = row.gps_time
    vehicle_id = row.vehicle_id
    

    # Вставляем данные в таблицу
    cursor.execute("""
        INSERT INTO vehicle_data (id, longitude, latitude, speed, gps_time, vehicle_id)
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (id, longitude, latitude, speed, gps_time, vehicle_id))

# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение с базой данных
cursor.close()
conn.close()
