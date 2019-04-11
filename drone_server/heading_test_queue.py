#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)
Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.
Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from __future__ import print_function
from dronekit import VehicleMode, LocationGlobalRelative
#from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil
import time
import math

def heading_test(vehicle,q):
    #get waypoint coordinates from user
    latlist = []
    longlist = []
    altlist = []
    
    print("Heading Test\n")
    
    lat = input("Enter the latitude of your test point:\n")
    latlist.append(lat)
    lon = input("Enter the longitude of your test point:\n")
    longlist.append(lon)
    alt = input("Enter the altitude of your test point:\n")
    altlist.append(alt)
    
    
    
    #print("Latitudes:", latlist)
    #print("Longitudes:", longlist)
    #print("Altitudes:", altlist)
    
    
    
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
            q.put(vehicle)
            print(" Altitude: ", vehicle.location.global_relative_frame.alt)
            # Break and return from function just below target altitude.
            if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)
    
    
    def condition_yaw(heading, relative=False):
        """
        Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).
        This method sets an absolute heading by default, but you can set the `relative` parameter
        to `True` to set yaw relative to the current yaw heading.
    
        By default the yaw of the vehicle will follow the direction of travel. After setting 
        the yaw using this function there is no way to return to the default yaw "follow direction 
        of travel" behaviour (https://github.com/diydrones/ardupilot/issues/2427)
    
        For more information see: 
        http://copter.ardupilot.com/wiki/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_condition_yaw
        """
        if relative:
            is_relative=1 #yaw relative to direction of travel
        else:
            is_relative=0 #yaw is an absolute angle
        # create the CONDITION_YAW command using command_long_encode()
        msg = vehicle.message_factory.command_long_encode(
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
            0, #confirmation
            heading,    # param 1, yaw in degrees
            0,          # param 2, yaw speed deg/s
            1,          # param 3, direction -1 ccw, 1 cw
            is_relative, # param 4, relative offset 1, absolute angle 0
            0, 0, 0)    # param 5 ~ 7 not used
        # send command to vehicle
        vehicle.send_mavlink(msg)
        vehicle.flush()
    
    speed = 10
    
    
    
    q.put(vehicle)
    arm_and_takeoff(10)
    q.put(vehicle)
    
    degree_symbol = u"\u00b0"
    point = LocationGlobalRelative(latlist[0], longlist[0], altlist[0])
    vehicle.simple_goto(point, groundspeed=speed)
    q.put(vehicle)
    # sleep so we can see the change in map
    time.sleep(5)
    for i in range(359):
        q.put(vehicle)
        print(str(i)+ degree_symbol,"from relative heading angle")
        condition_yaw(i, True)
        time.sleep(0.5)
    
    
    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")
    
    # Close vehicle object before exiting script
    print("Close vehicle object")
    
   
    # Shut down simulator if it was started.
    vehicle.armed = False
    q.put(vehicle)
    vehicle.close()
    
        