from math import atan2, sin, cos, sqrt
import datetime
class vehicle_class:
    def __init__(self, lat, lon):
        self.init_lat = lat
        self.init_lon = lon
        
    def update(self, vehicle):
        self.lat = vehicle.location.global_relative_frame.lat
        self.lon = vehicle.location.global_relative_frame.lon        
        self.alt = vehicle.location.global_relative_frame.alt
        self.heading = vehicle.heading
        self.mode = vehicle.mode
        time_str = str(datetime.datetime.now())
        self.time = time_str[11:len(time_str)]
        self.dist = self.calc_dist(self.lat, self.lon)
        
    def calc_dist(self, lat, lon):
        dlon = lon - self.init_lon
        dlat = lat - self.init_lat
        a = (sin(dlat/2))**2 + cos(self.init_lat) * cos(lat) * (sin(dlon/2))**2 
        c = 2 * atan2( sqrt(a), sqrt(1-a) ) 
        d = 6373 * c
        
        return d
        
        