import socket
import sys
# import arduino_motor_control_interface
import serial


def server_program():
    # get the hostname
    host = socket.gethostname()
    # initiate port no above 1024
    port = 8080
    # get instance
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # try to bind host address and port together
    try:
        server_socket.bind((host, port))
        print("///// NEST Server Online /////")
    except socket.error as e:
        print(str(e))
    # configure how many client the server can listen simultaneously
    server_socket.listen(5)
    # accept new connection
    conn, address = server_socket.accept()
    running = True
    print("Connection from: " + str(address))
    print("Now listening...")

    while running == True:
        # listen for messages from client
        data = conn.recv(1024).decode().strip()
        print(data)
        tasker(conn, data)

    # close the connection
    conn.close()
    server_program()



def tasker(conn, msg):
    global running
    if msg == "backButton":
        sender(conn, 'Previous camera...')

    elif msg == 'nextButton':
        sender(conn, 'Next camera...')

    elif msg == 'menuDiagnosticBtn':
        sender(conn, 'Running diagnostics...')

    elif msg == 'systemHaltButton':
        sender(conn, '!HALTING!')

    elif msg == 'doorsSwitchOn':
        sender(conn, 'Opening door...')

    elif msg == 'doorsSwitchOff':
        sender(conn, 'Closing door...')

    elif msg == 'roofSwitchOn':
        sender(conn, 'Opening roof...')

    elif msg == 'roofSwitchOff':
        sender(conn, 'Closing roof...')

    elif msg == 'extendPadSwitchOn':
        sender(conn, 'Extending pad...')

    elif msg == 'extendPadSwitchOff':
        sender(conn, 'Retracting pad...')

    elif msg == 'raisePadSwitchOn':
        sender(conn, 'Raising pad...')

    elif msg == 'raisePadSwitchOff':
        sender(conn, 'Lowering pad...')

    elif msg == 'menuDisconnectBtn':
            running = False



def sender(conn, msg):
    # wont send without \n because java uses readline
    conn.send((msg + '\n').encode())


server_program()
