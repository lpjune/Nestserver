import socket, json
from drone_class import drone_class

s = socket.socket()
port = 10000
s.bind(('', port))
s.listen(1)
c, addr = s.accept()
print "Socket Up and running with a connection from",addr
while True:
    rcvdData = c.recv(4096)
    v_obj = json.loads(rcvdData)
    v_dict = v_obj[0]
    # get variables
    lat = v_dict["lat"]
    lon = v_dict["lon"]
    alt = v_dict["alt"]
    heading = v_dict["heading"]
    mode = v_dict["mode"]
    time = v_dict["time"]
    dist = v_dict["distance"]
    # print variables
    print ("time: " + time + "\nlat: " + str(lat) + "\nlon: " + str(lon) + "\nalt: " + str(alt) +
          "\nmode: " + mode + "\nheading: " + str(heading) + "\ndistance from initial postion: " +
          str(dist) + "\n")
