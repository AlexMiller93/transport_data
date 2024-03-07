from flask import Flask, abort, jsonify, request

from database import get_db_connection

app = Flask(__name__)

conn = get_db_connection()
cur = conn.cursor()


@app.route('/vehicles', methods = ['GET'])
def get_all_vehicles():
    # GET запрос для получения всех машин с последней геометрией.
    
    # Выполнение запроса в БД 
    cur.execute("""SELECT DISTINCT ON (vehicle_id) *
        FROM track_data
        ORDER BY vehicle_id, gps_time DESC""")
    
    result = cur.fetchall()
    
    # обработка ошибки если нет результата
    if result is None:
        abort(404)
        
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


@app.route('/vehicles/<int:vehicle_id>', methods = ['GET'])
def get_vehicle(vehicle_id): 
    # GET запрос для получения конкретной машины с последней геометрией.

    # Выполнение запроса в БД 
    cur.execute("""
        SELECT *
        FROM track_data
        WHERE vehicle_id = {0}
        ORDER BY gps_time DESC
        LIMIT 1
    """.format(vehicle_id))
    
    result = cur.fetchone()
    
    # обработка ошибки 
    if result is None:
        abort(404)

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


@app.route('/vehicles/<int:vehicle_id>/track/', methods=['GET'])
def get_vehicle_track(vehicle_id): 
    # GET запрос для построения трека по дате или временному диапазону для конкретной машины.
    
    # получение данных из запроса временной диапазон / дата 
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    date = request.args.get('date')
    
    # Выполнение запроса в БД в зависимости от входных данных
    if start_date and end_date:
        cur.execute("""
            SELECT *
            FROM track_data
            WHERE vehicle_id = {0} AND gps_time BETWEEN {1} AND {2}
            ORDER BY gps_time ASC
        """.format(vehicle_id, start_date, end_date))
        
    elif date:
        cur.execute("""
            SELECT *
            FROM track_data
            WHERE vehicle_id = {0} AND gps_time == {1}
            ORDER BY gps_time ASC
        """.format(vehicle_id, date))
        
    else:
        cur.execute("""
            SELECT *
            FROM track_data
            WHERE vehicle_id = {0}
            ORDER BY gps_time ASC
        """.format(vehicle_id,))
        
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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5473)