from mechanical import *

time.sleep(1)

command_dictionary = {'0': "(0) Emergency Stop",'1': "(1) On/Off Switch", '2': "(2) Linear Actuator", '3': "(3-L) Left Door", '4': "(3-R) Right Door", '5': "(4-T) Top Lift", '6': "(4-B) Bottom Lift", '7': "(5) Roof"}

print("0 = Emergency stop\n1 = On/Off\n2 = Floor actuator\n3 = Doors\n4 = Lift\n5 = Roof\n6 = Status\nEnter (e)xit to quit")

toggle = 0

def display_status():
    task = nest_status()
    for index in range(8):
        print(command_dictionary[str(index)], "=", task[index])
            
    return

def mech_test(command):
    
    if command == '0':
        task = emergency_stop()
        return
    elif command == '1':
        task = on_off_switch()
        return
    elif command == '2':
        task = floor_pad()
        return
    elif command == '3':
        side = input("Enter (l)eft or (r)ight\n").lower()
        task = doors(side)
        return
    elif command == '4':
        level = input("Enter (t)op or (b)ottom\n").lower()
        task = lift(level)
        return
    elif command == '5':
        task = roof()
        return
    elif command == '6':
        display_status()
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
    
    global toggle
    toggle += 1

    if toggle > 5:
        display_status()
        toggle = 0
    
    state = main()
    if state == '0':
        break
    else:
        continue
    
    
