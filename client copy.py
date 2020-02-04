import socket
import sys
from time import sleep
from ev3dev.ev3 import *
from inputs import get_gamepad


#Connect to server
HOST, PORT = "192.168.43.43", 9998

sleep(0.05)
while True:
    events = get_gamepad()
    #print(events)
    for e in events:
        data = str(e.code) + ',' + str(e.state)

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))

    # Receive data from the server and shut down
    #received = str(sock.recv(1024), "utf-8")

    print("Sent:     {}".format(data))
    #print("Received: {}".format(received))





