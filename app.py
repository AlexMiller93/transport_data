from flask import Flask, abort, jsonify, request
from psycopg2 import OperationalError
from database import get_db_connection

app = Flask(__name__)

conn = get_db_connection()
cur = conn.cursor()


@app.route('/vehicles', methods = ['GET'])
def get_all_vehicles():
    # GET запрос для получения всех машин с последней геометрией.
    
    result = None
    
    try:
        # Выполнение запроса в БД 
        cur.execute("""SELECT DISTINCT ON (vehicle_id) *
            FROM track_data
            ORDER BY vehicle_id, gps_time DESC""")
        
        result = cur.fetchall()
        
        # формирование списка для вывода результата запроса в БД
        vehicles = []
        
        for row in result:
            vehicle = {
                'id': row[0],
                'longitude': row[1],
                'latitude': row[2],
                'speed': row[3],
                'gps_time': row[4],
                'vehicle_id': row[5]
            }
            vehicles.append(vehicle)

        return jsonify(vehicles), 200
    
    # вызов исключения
    except OperationalError as e:
        print(f"Произошла ошибка при выполнения запроса: \n'{e}' ")
        
    # обработка ошибки если нет результата
    if result is None:
        abort(404)
        
    
@app.route('/vehicles/<int:vehicle_id>', methods = ['GET'])
def get_vehicle(vehicle_id): 
    # GET запрос для получения конкретной машины с последней геометрией.
    
    result = None
    
    try:
        # Выполнение запроса в БД 
        cur.execute("""
            SELECT *
            FROM track_data
            WHERE vehicle_id = %(vehicle_id)s
            ORDER BY gps_time DESC
            LIMIT 1""", {'vehicle_id': vehicle_id})
        
        result = cur.fetchone()
        
        # формирование результата запроса в БД
        vehicle = {
            'id': result[0],
            'longitude': result[1],
            'latitude': result[2],
            'speed': result[3],
            'gps_time': result[4],
            'vehicle_id': result[5]
        }
        
        return jsonify(vehicle), 200
    
    # вызов исключения
    except OperationalError as e:
        print(f"Произошла ошибка при выполнения запроса: \n'{e}' ")
        
    # обработка ошибки 
    if result is None:
        abort(404)

@app.route('/vehicles/<int:vehicle_id>/track/', methods=['GET'])
def get_vehicle_track(vehicle_id): 
    # GET запрос для построения трека по дате или временному диапазону для конкретной машины.
    
    # получение данных из запроса временной диапазон / дата 
    # TODO: обработать входные данные на тип
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    date = request.args.get('date')
    
    result = None
    
    
    # Выполнение запроса в БД в зависимости от входных данных
    if start_date and end_date:
        try:
            cur.execute("""
                SELECT *
                FROM track_data
                WHERE vehicle_id = %(vehicle_id)s AND gps_time BETWEEN %(start_date)s AND %(end_date)s
                ORDER BY gps_time ASC
            """, {
                    'vehicle_id': vehicle_id, 
                    'start_date': start_date, 
                    'end_date': end_date 
                }
            )
            
        # вызов исключения
        except OperationalError as e:
            print(f"Произошла ошибка при выполнения запроса: \n'{e}' ")
        
    elif date:
        try:
            cur.execute("""
                SELECT *
                FROM track_data
                WHERE vehicle_id = %(vehicle_id)s AND gps_time == %(date)s
                ORDER BY gps_time ASC
            """, {
                    'vehicle_id': vehicle_id, 
                    'date': date, 
                }
            )
            
        # вызов исключения
        except OperationalError as e:
            print(f"Произошла ошибка при выполнения запроса: \n'{e}' ")
        
    else:
        try:
            cur.execute("""
            SELECT *
            FROM track_data
            WHERE vehicle_id = %(vehicle_id)s
            ORDER BY gps_time DESC
            """, {'vehicle_id': vehicle_id})
            
        # вызов исключения
        except OperationalError as e:
            print(f"Произошла ошибка при выполнения запроса: \n'{e}' ")
    
    try:
        result = cur.fetchall()
        
        # обработка ошибки 
        if result is None:
            abort(404)
            
        # формирование списка для вывода результата запроса в БД
        track = []
        
        for row in result:
            vehicle = {
                'id': row[0],
                'longitude': row[1],
                'latitude': row[2],
                'speed': row[3],
                'gps_time': row[4],
                'vehicle_id': row[5]
            }
            
            track.append(vehicle)

        return jsonify(track), 200
    
    except Exception as e:
        print(f'Вызов исключения: {e}')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5473)