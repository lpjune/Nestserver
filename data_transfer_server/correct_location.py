import datetime
from remote_pi import DronePi
from transform_location_data import *


def correct_location(remote_file_path, local_file_path, latposition, longposition):
    now = datetime.datetime.now()
    pi = DronePi()                                                          # SSH into pi and get yyyy-mm-dd_land_log.txt
    pi.connect()
    pi.read_file(remote_file_path, local_file_path)
    pi.close()

    f = open(now.strftime("%Y-%m-%d")+'_land_log.txt', 'rb')                 # open the file and read the coordiante vectors
    correction_vector = f.read()
    correction = correction_vector.decode()
                                                                             # The last line is the correction coordinates in x,y
    correction = correction.split(',')
    correction[0] = int(correction[0])
    correction[1] = int(correction[1])
    
    posX,posY = latlong_to_xy(latposition, longposition)                    # Transform position into the x,y; correct the position; transform back to lat long
    correctedX = posX - correction[0]
    correctedY = posY - correction[1]

    
    return xy_to_latlong(correctedX, correctedY)
    
    
def correct_landing(vehicle, speed, increment, remote_file_path, local_file_path):
    
    lat, lon, current_alt = vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon,  vehicle.location.global_relative_frame.alt
    
    new_lat, new_long = correct_location(remote_file_path, local_file_path, lat, lon)
    new_alt = current_alt - increment
    
    point = LocationGlobalRelative(new_lat, new_long, new_alt)
    vehicle.simple_goto(point, groundspeed=speed)
    time.sleep(increment/speed)
    
    return new_lat, new_long, new_alt
