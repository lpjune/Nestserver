from __future__ import print_function
import threading
import time
import argparse
import socket, json
from dronekit import connect, VehicleMode, LocationGlobalRelative
from drone_class import drone_class

################################################
############## DRONEKIT FUNCTIONS ##############
################################################

def goto():
    
    arm_and_takeoff(10)
    
    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3
    
    print("Going towards first point for 10 seconds ...")
    point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
    vehicle.simple_goto(point1)
    
    # sleep so we can see the change in map
    time.sleep(10)
    
    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")
    
    # Close vehicle object before exiting script
    print("Close vehicle object")
    #########
    vehicle.armed = False ## !! Careful with this -- want to land before disarming
    #########
    vehicle.close()
    print("Vehicle Closed")



def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


################################################
############## SETUP FOR MAIN ##################
################################################

#### Connect to Server ####
ip = "172.18.135.155" # local ip address
port = 10000

sock = socket.socket()
sock.connect((ip, port))

#### Setup for Vehicle ###

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



#### Thread Setup ####

class ThreadA(threading.Thread): # This transfers vehicle variables to server
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global vehicle
        global sock
        # port vehicle variables to drone class
        drone = drone_class(vehicle.location.global_relative_frame.lat,
                              vehicle.location.global_relative_frame.lon)
        while True:
            if vehicle.armed == True: # only start running when vehicle is armed
                while vehicle.armed:
                    v_obj = self.encode(drone) # pack drone variables into json compatible dictionary
                    j_obj = json.dumps(v_obj)  # convert to json object
                    sock.send(j_obj)           # send json object to server
                    time.sleep(.2)             


                
    # make vehicle variables json compatible
    def encode(self, drone):
        drone.update(vehicle) # update drone object
        v_obj = [{"lat": drone.lat, "lon": drone.lon, "alt": drone.alt,
                  "heading": drone.heading,"mode": drone.mode, "time": drone.time,
                  "distance": drone.dist}] # dump everything into a dictionary
        return v_obj



#### Main Execution ####

a = ThreadA("threadA") # create thread
a.daemon = True
a.start()              # start thread

goto()                 # run drone function
sock.close()





