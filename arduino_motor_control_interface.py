'''
0.3
This program is currently the interface for the motor driver controller.
In the future the call to main needs to be removed and this software would need to be called by another program
It will likely need to be adapted to return information that is being printed in this version
'''

import time
import serial

ser = serial.Serial('COM4', 9600)


#   this is supposed to search for available COM ports but I didn't get the opportunity to test it
'''
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports :
    print(port.device)
'''

def serial_control(command):

    command_dictionary = {'0': "Emergency Stop",'1': "On/Off Switch", '2': "Linear Actuator", '3': "Left Door", '4': "Right Door", '5': "Lift Actuator", '6': "Doors"}

    command = command.encode('ascii')
    ser.write(command)
    if(command.decode('ascii') != '5'):
        back_talk = ser.read()
        back_talk = back_talk.decode('ascii')

    #   exit command

    if(command.decode('ascii').lower() == "exit"):
        return 'e'

    #   lift actuator commands
    
    if(command.decode('ascii') == '5'):
        lift_command = input("Enter T to change the top actuator position\nEnter B to change the bottom actuator position\n")
        lift_command = lift_command.upper()
        lift_command = lift_command.encode('ascii')
        ser.write(lift_command)
        print("Please wait 20 seconds...")
        time.sleep(20)
        back_talk = ser.read()
        back_talk = back_talk.decode('ascii')
        print('')
        if(lift_command.decode('ascii') == 'T') and (back_talk == '>'):
            print("The top lift was raised")
            return 'n'
        if(lift_command.decode('ascii') == 'T') and (back_talk == '<'):
            print("The top lift was lowered")
            return 'n'
        if(lift_command.decode('ascii') == 'B') and (back_talk == '>'):
            print("The bottom lift was raised")
            return 'n'
        if(lift_command.decode('ascii') == 'B') and (back_talk == '<'):
            print("The bottom lift was lowered")
            return 'n'

    #	one recieved

    if(back_talk == '1') and (command.decode('ascii') == '0'):
        print("The", command_dictionary['0'], "has been executed")
        return 'n'

    if(back_talk == '1') and (command.decode('ascii') == '1'):
        print("The", command_dictionary['1'], "has been switched to on")
        return 'n'

    if(back_talk == '1') and (command.decode('ascii') == '3' or command.decode('ascii') == '4'):
        print("The", command_dictionary[command.decode('ascii')], "has been opened")
        return 'n'

    if(back_talk == '1') and (command.decode('ascii') == '2'):
        print("The", command_dictionary[command.decode('ascii')], "has been extended")
        return 'n'

    '''if(back_talk == '1') and (command.decode('ascii') == '5'):
        print("The", command_dictionary[command.decode('ascii')], "has been raised")
        return 'n'
        '''

    if(back_talk == '1') and (command.decode('ascii') == '6'):
        print("The", command_dictionary[command.decode('ascii')], "have been opened")
        return 'n'

    #	zero recieved

    if(back_talk == '0') and (command.decode('ascii') == '0'):
        print("The", command_dictionary['0'], "has ended")
        return 'n'

    if(back_talk == '0') and (command.decode('ascii') == '1'):
        print("The", command_dictionary['1'], "has been switched to off")
        return 'n'

    if(back_talk == '0') and (command.decode('ascii') == '3' or command.decode('ascii') == '4'):
        print("The", command_dictionary[command.decode('ascii')], "has been closed")
        return 'n'

    if(back_talk == '0') and (command.decode('ascii') == '2'):
        print("The", command_dictionary[command.decode('ascii')], "has been retracted")
        return 'n'

    '''if(back_talk == '0') and (command.decode('ascii') == '5'):
        print("The", command_dictionary[command.decode('ascii')], "has been lowered")
        return 'n'
        '''

    if(back_talk == '0') and (command.decode('ascii') == '6'):
        print("The", command_dictionary[command.decode('ascii')], "have been closed")
        return 'n'

    #   invalid command responses

    elif(back_talk != '1') and (back_talk != '0') and (back_talk != '>') and (back_talk != '<'):
        print("There was invalid input from the motor controller")
        return 'n'

    else:
        print("Invalid command.")
        return 'n'



def main():
    print("== This is the motor control interface ==")
    print("=========================================\n")
    print("The commands are as follows:")
    print("0:\tEmergency Stop\n1:\tOn/Off\n2:\tLinear Actuator\n3:\tLeft Door\n4:\tRight Door\n5:\tLift Actuator\n6:\tBoth Doors\n")
    print("If door states do not match, command 6 will return an error\n")
    print("Enter exit to close the program.\n")
    #print("Command 5: Lift Actuator will not work as intended. Do not use.")
    while(1):
        user_command = input("Enter a command here:\n")
        command = serial_control(user_command)
        if(command == 'e'):
            break
        else:
            continue
        
main()
