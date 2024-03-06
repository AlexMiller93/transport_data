from flask import Flask, jsonify, request

from transport_data.database import get_db_connection

app = Flask(__name__)

conn = get_db_connection()
cur = conn.cursor()


@app.route('/vehicles', methods = ['GET'])
def get_all_vehicles():
    # GET запрос для получения всех машин с последней геометрией.
    
    cur.execute("""SELECT DISTINCT ON (vehicle_id) *
        FROM track_data
        ORDER BY vehicle_id, gps_time DESC""")
    
    result = cur.fetchall()
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
    cur.close()
    conn.close()
    return jsonify(vehicles)


@app.route('/vehicles/<int:vehicle_id>', methods = ['GET'])
def get_vehicle(vehicle_id): 
    # GET запрос для получения конкретной машины с последней геометрией.

    cur.execute("""
        SELECT *
        FROM track_data
        WHERE vehicle_id = %s
        ORDER BY gps_time DESC
        LIMIT 1
    """, (vehicle_id,))
    result = cur.fetchone()

    vehicle = {
        'id': result[0],
        'longitude': result[1],
        'latitude': result[2],
        'speed': result[3],
        'gps_time': result[4],
        'vehicle_id': result[5]
    }
    
    return jsonify(vehicle)


@app.route('/vehicles/<int:vehicle_id>/track/', methods=['GET'])
def get_vehicle_track(vehicle_id): 
    # GET запрос для построения трека по дате или временному диапазону для конкретной машины.
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    date = request.args.get('date')
    
    if start_date and end_date:
        cur.execute("""
            SELECT *
            FROM track_data
            WHERE vehicle_id = %s AND gps_time BETWEEN %s AND %s
            ORDER BY gps_time ASC
        """, (vehicle_id, start_date, end_date))
        
    elif date:
        cur.execute("""
            SELECT *
            FROM track_data
            WHERE vehicle_id = %s AND gps_time == %s
            ORDER BY gps_time ASC
        """, (vehicle_id, date))
        
    else:
        cur.execute("""
            SELECT *
            FROM track_data
            WHERE vehicle_id = %s
            ORDER BY gps_time ASC
        """, (vehicle_id,))
        
    result = cur.fetchall()

    track = []
    
    for row in result:
        point = {
            'id': row[0],
            'longitude': row[1],
            'latitude': row[2],
            'speed': row[3],
            'gps_time': row[4],
            'vehicle_id': row[5]
        }
        track.append(point)

    return jsonify(track)

if __name__ == '__main__':
    app.run(debug=True)