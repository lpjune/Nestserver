from mechanical import *
'''
This script is used to test mechanical.py. All commands are sent to an arduino that
will actually control these mechanisms. All commands are sent via USB as serial.
Austin Flynt
MS STATE IMPRESS LAB
'''
time.sleep(1)
print("0 = Emergency stop\n1 = On/Off\n2 = Floor actuator\n3 = Doors\n4 = Lift\n5 = Roof\n6 = Status\nEnter (e)xit to quit")
def mech_test(command):
    if command == '0':
        task = emergency_stop()
        print(task)
        return
    elif command == '1':
        task = on_off_switch()
        print(task)
        return
    elif command == '2':
        task = floor_pad()
        print(task)
        return
    elif command == '3':
        side = input("Enter (l)eft or (r)ight\n").lower()
        task = doors(side)
        print(task)
        return
    elif command == '4':
        level = input("Enter (t)op or (b)ottom\n").lower()
        task = lift(level)
        print(task)
        return
    elif command == '5':
        task = roof()
        print(task)
        return
    elif command == '6':
        task = nest_status()
        print(task)
        return
    else:
        print("?")
        return
    
def main():
    command = input('>>>')
    if command == 'exit' or command == 'e':
        return '0'
    mech_test(command)
    return '1'

while(1):
    state = main()
    if state == '0':
        break
    else:
        continue
    
    
