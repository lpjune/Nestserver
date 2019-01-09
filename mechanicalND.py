'''
This module is used to control motors and lifts. All commands are sent to an arduino that
will actually control these mechanisms. All commands are sent via USB as serial.
Austin Flynt
MS STATE IMPRESS LAB
'''

import time
import serial

port = 'COM10'

ser = serial.Serial(port, 9600)

print("Connection established with Arduino on port" ,port)


# state of the left door: false = closed and true = open
left = False

#state of the right door: false = close and true = open
right = False

#state of the floor pad actuator: false = retracted and true = extended
extended = False

#state of the roof: false = close and true = open
roof = False

#state of the bottom lift: false = lowered and top = raised
bottom = False

#state of the top lift: false = lowered and top = raised
top = False

################################################################################

# this is the function for controlling the lift:
# command is a boolean that states whether to lower or raise the lift
# level states which lift (top or bottom) that we are controlling

def lift(level = '', halt = ''):

    global top
    global bottom

    if halt != '':
        
        command = 'h'.encode('ascii')
        ser.write(command)
        time.sleep(0.1)
        
        back_talk = ser.read()
        back_talk = back_talk.decode('ascii')
        print(back_talk)
        if back_talk == '!':
            print("Unexpected Input")
            
        if top == True:
            top = False
            
        if top == False:
            top = True

        if bottom == True:
            bottom = False
            
        if bottom == False:
            bottom = True

        ser.read()
        return back_talk

    level = level.lower()
    command = '5'.encode('ascii')
    ser.write(command)
    
    if level =='top' or level == 't':
        ser.write('T'.encode('ascii'))
        return 'top_transition'
                
    if level == 'bottom' or level == 'b':
        ser.write('B'.encode('ascii'))
        return 'bottom_transition'
    
    else:
        return "Unexpected Input"
                
################################################################################
            

def emergency_stop():
    command = '0'.encode('ascii')
    ser.write(command)
    back_talk = ser.read()
    back_talk = back_talk.decode('ascii')
    if back_talk == '!':
        print("Unexpected Input")
    
    if back_talk == '1':
        print("EMERGENCY STOP")
        return 'stop'
    
    if back_talk == '0':
        return 'resume'
    else:
        return


################################################################################


def on_off_switch():
    command = '1'.encode('ascii')
    ser.write(command)
    back_talk = ser.read()
    back_talk = back_talk.decode('ascii')
    if back_talk == '!':
        print("Unexpected Input")
    if back_talk == '1':
        return 'on'
    
    if back_talk == '0':
        return 'off'
    else:
        return

################################################################################

def doors(side):
    
    global left
    global right

    side = side.lower()
    if side == 'left' or side == 'l':
        command = '3'.encode('ascii')
        ser.write(command)
        back_talk = ser.read()
        if back_talk == '!':
            print("Unexpected Input")
        back_talk = back_talk.decode('ascii')
        if back_talk  == '1':
            left = True
            return 'left_open'
        

        if back_talk  == '0':
            left = False
            return 'left_closed'
        

    if side == 'right' or side == 'r':
            command = '4'.encode('ascii')
            ser.write(command)
            back_talk = ser.read()
            back_talk = back_talk.decode('ascii')
            if back_talk == '!':
                print("Unexpected Input")
            if back_talk  == '1':
                left = True
                return 'right_open'
            

            if back_talk  == '0':
                left = False
                return 'right_closed'
            
    else:
        return "Unexpected Input"

################################################################################
    
def floor_pad():

    global extended

    command = '2'.encode('ascii')
    ser.write(command)
    back_talk = ser.read()
    back_talk = back_talk.decode('ascii')
    if back_talk == '!':
        print("Unexpected Input")
    if back_talk == '1':
        extended == True
        return 'floor_pad_extended'

    if back_talk == '0':
        extended == False
        return 'floor_pad_retracted'
    else:
        return

################################################################################

def roof():

    global roof

    command = '7'.encode('ascii')
    ser.write(command)
    back_talk = ser.read()
    back_talk = back_talk.decode('ascii')
    if back_talk == '!':
        print("Unexpected Input")
    if back_talk == '1':
        roof == True
        return 'roof_open'

    if back_talk == '0':
        roof == False
        return 'roof_closed'
    else:
        return

################################################################################

def nest_status():
    data_str = ''
    command = '8'.encode('ascii')
    ser.write(command)
    
    while len(data_str) < 8:
        data = ser.read()
        data = data.decode('ascii')
        
        if data == 'l':
            data = '0'
            
        if data == 'h':
            data = '1'
            
        data_str = data_str + data
            
    status = data_str
    return status

    
    
