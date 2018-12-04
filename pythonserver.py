import socket
import sys
# import arduino_motor_control_interface
import serial


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5555  # initiate port no above 1024
    # get instance
    server_socket = socket.socket()
    # try to bind host address and port together
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(str(e))
    # configure how many client the server can listen simultaneously
    server_socket.listen(5)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        listen()
        conn.send(data.encode())  # send data to the client
    # close the connection
    conn.close()

# all lan uses antenna right outside of nest
def listen(from_device):
    data = conn.recv(1024).decode()
    # app
    if from_device == 'app':
        app(data)
    # arduino (motors) is wired to master computer
    elif from_device == 'arduino':
        arduino(data)
    # pi (drone)
    elif from_device == 'pi_drone':
        pi_drone(data)
    # latte panda (pressure matrix)
    elif from_device == 'latte_panda':
        latte_panda(data)

# def send(to_device, data):


server_program()
