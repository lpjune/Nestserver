from dronekit import connect, VehicleMode, LocationGlobalRelative
import threading, Queue
from heading_test_queue import heading_test
 
from pymavlink import mavutil
from vehicle_class import vehicle_class

# setup queue
q = Queue.Queue()

#setup function 4 printing

def vehicle_data(vehicle, q):
    f = open("dronekit_data.txt", "w+")
    lat = vehicle.location.global_relative_frame.lat
    lon = vehicle.location.global_relative_frame.lon
    # initialize vehicle class
    v_obj = vehicle_class(lat, lon)
    while( vehicle.armed == True ):
        # do stuff
        vehicle = q.get()
        v_obj.update(vehicle)
        msg = "\nTime: " + v_obj.time + "\nMode: " + str(v_obj.mode) + "\nLat: " + str(v_obj.lat) + "\nLon: " + str(v_obj.lon) + "\nAlt: " + str(v_obj.alt) + "\nDistance: " + str(v_obj.dist) + "\nHeading: " + str(v_obj.heading)
        f.write(msg)
        # pass through v_obj to server???
    f.close()
    

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

th1 = threading.Thread(target=heading_test, args=(vehicle,q))
th1.start()
while True:
    v = q.get()
    if (v.armed == True):
        th2 = threading.Thread(target=vehicle_data, args=(q.get(),q))
        th2.start()
        break


