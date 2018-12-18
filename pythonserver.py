import socket
import sys
# import arduino_motor_control_interface
import serial


def server_program():
    # get the hostname
    host = socket.gethostname()
    # initiate port no above 1024
    port = 43434
    # get instance
    server_socket = socket.socket()
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
    while True:
        print("Now listening...")
        listening()
        sending('hey you sent something')

    # close the connection
    conn.close()

def listening():
    data = conn.recv(1024).decode()
    print(data)

def sending(input):
    server_socket.send(input.encode())
# def send(to_device, data):


server_program()
