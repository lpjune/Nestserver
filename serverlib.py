import sys
import selectors
import json
import io
import struct
import time
import serial
from mechanical import *

# status of all NEST components
# 0 = closed/off, 1 = open/on
doorStatus = 0
roofStatus = 0
bPadStatus = 0
tPadStatus = 0
powerStatus = 0

status = str(doorStatus) + str(roofStatus) + str(bPadStatus) + str(tPadStatus) + str(powerStatus)

def get_status():
    global status
    return status


# key = received message, value = response
request_dict = {
    "backButton": "Previous camera...",
    "nextButton": "Next camera...",
    "menuDiagnosticBtn": "Running diagnostics...",
    "systemHaltButton": "HALTING.",
    "doorsSwitchOn": "Opening doors...",
    "doorsSwitchOff": "Closing doors...",
    "roofSwitchOn": "Opening roof...",
    "roofSwitchOff": "Closing roof...",
    "extendPadSwitchOn": "Extending pad...",
    "extendPadSwitchOff": "Retracting pad...",
    "raisePadSwitchOn": "Raising pad...",
    "raisePadSwitchOff": "Lowering pad...",
    "status": status,
    "switchPower": "Toggled Power ",
    "closeConnection": "Connection Closed"
}


# receive messages from Connection
# decode and strip whitespace/newlines
def receiver(conn):
    data = conn.recv(1024).decode().strip()
    print(data)
    return data


# send encoded messages to connection
# must have newline for java to receive
# if message is empty string send default
def sender(conn, message):
    if message == None:
        conn.send(("Unknown response" + "\n").encode())
    else:
        conn.send((message + '\n').encode())
    return


# create response to send back
# check for blocks to command
# eg no door open allowed while pad up
# match message to response in dict
# send command to machine and return response
def create_response(query):
    global doorStatus
    global roofStatus
    global bPadStatus
    global tPadStatus
    global powerStatus
    global status

    motorStatus = nest_status()

    if motorStatus[3] == '1' and motorStatus[4] == '1':
        doorStatus = '1'
    else:
        doorStatus = '0'

    roofStatus = motorStatus[7]
    bPadStatus = motorStatus[2]
    tPadStatus = motorStatus[6]
    powerStatus = motorStatus[1]

    # check for error, i.e. opening opened doors
    error_exists = create_error_response(query)

    if error_exists != 0:
        return error_exists

    answer = request_dict.get(query)
    response = machine_control(answer)

    return response


# called if block command in create_response
# return error response
def create_error_response(query):
    global doorStatus
    global roofStatus
    global bPadStatus
    global tPadStatus
    global powerStatus
    global status
    if query == "doorsSwitchOff" and bPadStatus == '1':
        answer = "Error: Cannot close doors with bottom pad extended"
    elif query == "extendPadSwitchOn" and doorStatus == '0':
        answer = "Error: Cannot extend pad with doors closed"
    elif query == "raisePadSwitchOn" and roofStatus == '0':
        answer = "Error: Cannot raise pad with roof closed"
    elif query == "roofSwitchOff" and tPadStatus == '1':
        answer = "Error: Cannot close roof with pad raised"
    elif query == "doorsSwitchOn" and doorStatus == '1':
        answer = "Error: Doors already open"
    elif query == "doorsSwitchOff" and doorStatus == '0':
        answer = "Error: Doors already closed"
    elif query == "roofSwitchOn" and roofStatus == '1':
        answer = "Error: Roof already open"
    elif query == "roofSwitchOff" and roofStatus == '0':
        answer = "Error: Roof already closed"
    elif query == "extendPadSwitchOn" and bPadStatus == '1':
        answer = "Error: Bottom Pad already extended"
    elif query == "extendPadSwitchOff" and bPadStatus == '0':
        answer = "Error: Bottom Pad already retracted"
    elif query == "raisePadSwitchOn" and tPadStatus == '1':
        answer = "Error: Top Pad already raised"
    elif query == "raisePadSwitchOff" and tPadStatus == '0':
        answer = "Error: Top Pad already lowered"
    else:
        answer = 0
    return answer


# sends command to machine
# updates status
# return response
def machine_control(answer):
    global doorStatus
    global roofStatus
    global bPadStatus
    global tPadStatus
    global powerStatus
    global status

    if answer == "Opening doors...":
        left = doors("left")
        right = doors("right")
        print(left)
        print(right)

    elif answer == "Closing doors...":
        left = doors("left")
        right = doors("right")
        print(left)
        print(right)

    elif answer == "Opening roof...":
        top_roof = roof()
        print(top_roof)

    elif answer == "Closing roof...":
        top_roof = roof()
        print(top_roof)

    elif answer == "Extending pad...":
        bPad = floor_pad()
        print(bPad)

    elif answer == "Retracting pad...":
        bPad = floor_pad()
        print(bPad)

    elif answer == "Raising pad...":
        #tPad = lift('top')
        tPad = lift('bottom')
        print(tPad)

    elif answer == "Lowering pad...":
        #tPad = lift('top')
        tPad = lift('bottom')
        print(tPad)

    if answer == "Toggled Power ":
        on_off_switch()
        if motorStatus[1] == '1':
            answer = answer + 'Off'
        else:
            answer = answer + 'On'

    motorStatus = nest_status()

    print(motorStatus)
    if motorStatus[3] == '1' and motorStatus[4] == '1':
        doorStatus = '1'
    else:
        doorStatus = '0'

    roofStatus = motorStatus[7]
    bPadStatus = motorStatus[2]
    tPadStatus = motorStatus[6]
    powerStatus = motorStatus[1]

    return answer
