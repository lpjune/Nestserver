from mechanical import *
time.sleep(1)
print("0 = Emergency stop\n1 = On/Off\n2 = Floor actuator\n3 = Doors\n5 = Lift\n7 = Roof\nEnter exit to quit")
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
        side = input("Enter left or right\n").lower()
        task = doors(side)
        print(task)
        return
    elif command == '5':
        level = input("Enter top or bottom\n").lower()
        task = lift(level)
        print(task)
        return
    elif command == '7':
        task = roof()
        print(task)
        return
    else:
        print("?")
        return
    
def main():
    command = input('>>>')
    if command == 'exit':
        return '0'
    mech_test(command)
    return '1'

while(1):
    state = main()
    if state == '0':
        break
    else:
        continue
    
    
