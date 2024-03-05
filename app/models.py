from app import db

# Столбцы из excel файла
# id: int, longitude: float, latitude, speed, gps_time, vehicle_id

class Track(db.Model):
    """ 
    Таблица для 
    """
    id = db.Column(db.Integer, primary_ley=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Integer)
    gps_time = db.Column(db.DateTime, nullable=False)
    vehicle_id = db.Column(db.Integer, unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Track vehicle> with id {self.vehicle_id}'