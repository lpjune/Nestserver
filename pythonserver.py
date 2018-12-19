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
        data = conn.recv(1024).decode().strip()
        print(data)
        if data == 'ok':
            print('good job!')
        senddata = input("send data: ")
        conn.sendall(senddata.encode())

    # # close the connection
    # conn.close()

# def listening():
#     data = conn.recv(1024).decode()
#     print(data)
#
# def sending(input):
#     conn.send(input.encode())



server_program()
