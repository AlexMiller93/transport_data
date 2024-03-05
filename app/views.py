from flask import Flask

app = Flask(__name__)


@app.route('/vehicles/')
def get_all_vehicles():
    # Страница всех машин 
    return 'Page for all vehicles'


@app.route('/vehicles/<vehicle_id>')
def get_vehicle(vehicle_id): 
    # Страница машины по id 
    
    return f'Page for one vehicle with id {vehicle_id}'


@app.route('/vehicles/<vehicle_id>/track/')
def get_vehicle_track(vehicle_id): 
    # Страница для построения трека машины по дате или по временному диапазону  
    
    return 'Page for track one vehicle with id {vehicle_id}'
