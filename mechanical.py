'''
This module is used to control motors and lifts. All commands are sent to an arduino that
will actually control these mechanisms. All commands are sent via USB as serial.
Austin Flynt
MS STATE IMPRESS LAB
'''

import time
import serial

port = 'COM4'

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

def lift(level):

    global top
    global bottom
        
    if level =='top':
        ser.write('T'.encode('ascii'))
        print("Please wait 20 seconds...")
        time.sleep(20)
        back_talk = ser.read()
        back_talk = back_talk.decode('ascii')
        if top == True:
            top = False
        else:
            top = True
        
        return back_talk
                
    if level == 'bottom':
        ser.write('B'.encode('ascii'))
        print("Please wait 20 seconds...")
        time.sleep(20)
        back_talk = ser.read()
        back_talk = back_talk.decode('ascii')
        if bottom == True:
            bottom = False
        else:
            bottom = True
        
        
        return back_talk
    else:
        return
                
################################################################################
            

def emergency_stop():
    command = '0'.encode('ascii')
    ser.write(command)
    back_talk = ser.read()
    back_talk = back_talk.decode('ascii')
    
    if back_talk == '1':
        print("EMERGENCY STOP")
        return 'stop'
    
    if back_talk == '0':
        print("SYSTEM RESUME")
        return 'resume'
    else:
        return


################################################################################


def on_off_switch():
    command = '1'.encode('ascii')
    ser.write(command)
    back_talk = ser.read()
    back_talk = back_talk.decode('ascii')
    if back_talk == '1':
        print("On")
        return 'on'
    
    if back_talk == '0':
        print("Off")
        return 'off'
    else:
        return

################################################################################

def doors(side):
    
    global left
    global right
    
    if side == 'left':
        command = '3'.encode('ascii')
        ser.write(command)
        back_talk = ser.read()
        back_talk = back_talk.decode('ascii')
        if back_talk  == '1':
            left = True
            return 'left_open'
        

        if back_talk  == '0':
            left = False
            return 'left_closed'
        

    if side == 'right':
            command = '4'.encode('ascii')
            ser.write(command)
            back_talk = ser.read()
            back_talk = back_talk.decode('ascii')
            if back_talk  == '1':
                left = True
                return 'right_open'
            

            if back_talk  == '0':
                left = False
                return 'right_closed'
            
    else:
        return

################################################################################
    
def floor_pad():

    global extended

    command = '2'.encode('ascii')
    ser.write(command)
    back_talk = ser.read()
    back_talk = back_talk.decode('ascii')
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
    if back_talk == '1':
        roof == True
        return 'roof_open'

    if back_talk == '0':
        roof == False
        return 'roof_closed'
    else:
        return

################################################################################











    
