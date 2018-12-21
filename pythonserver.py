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
    print("Connection from: " + str(address))
    print("Now listening...")

    while True:
        # listen for messages from client
        data = conn.recv(1024).decode().strip()
        print(data)
        tasker(conn, data)

    # close the connection
    # conn.close()

def tasker(conn, msg):
    if msg == "backButton":
        sender(conn, 'Previous camera...')

    elif msg == 'nextButton':
        sender(conn, 'Next camera...')

    elif msg == 'menuDiagnosticBtn':
        sender(conn, 'Running diagnostics...')

    elif msg == 'systemHaltButton':
        sender(conn, '!HALTING!')

    elif msg == 'doorsSwitch':
        sender(conn, 'Opening door...')

    elif msg == 'roofSwitch':
        sender(conn, 'Opening roof...')

    elif msg == 'extendPadSwitch':
        sender(conn, 'Extending pad...')

    elif msg == 'raisePadSwitch':
        sender(conn, 'Raising pad...')


def sender(conn, msg):
    # wont send without \n because java uses readline
    conn.send((msg + '\n').encode())


server_program()
