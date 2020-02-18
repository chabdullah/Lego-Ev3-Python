import socket
import sys
from time import sleep
from ev3dev.ev3 import *
from inputs import get_gamepad


#Connect to server
host, port = "192.168.43.219", 12397

stick_values_X = []
stick_values_Y = []
sleep(0.05)
count = 0
while True:
    events = get_gamepad()
    #print (events)
    #sleep(1)
    
    #print(len(events))
    #print(events[0].ev_type)

    if events[0].ev_type != 'Sync':
        code = events[0].code
        state = events[0].state

        '''
        for e in events:
            data = str(e.code) + ',' + str(e.state)
            #print(data)
        

        code, state = data.split(',')
        '''
        n_comandi = 5
        if (code == 'ABS_X'):
            stick_values_X.append(state)
            if len(stick_values_X) == n_comandi:
                data = 'ABS_X' + ',' + str(stick_values_X[n_comandi-1])
                stick_values_X = []
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    # Connect to server and send data
                    sock.connect((host, port))
                    sock.sendall(bytes(data, "utf-8"))
                    #count += 1
                    #print(count)
        elif (code == 'ABS_Y'):
            stick_values_Y.append(state)
            if len(stick_values_Y) == n_comandi:
                data = 'ABS_Y' + ',' + str(stick_values_Y[n_comandi-1])
                stick_values_Y = []
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    # Connect to server and send data
                    sock.connect((host, port))
                    sock.sendall(bytes(data, "utf-8"))
                    #count += 1
                    #print(count)
            elif (len(stick_values_Y) < n_comandi) and (state >= -386) and (state <= 128):
                data = 'ABS_Y' + ',' + str(state)
                stick_values_Y = []
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    # Connect to server and send data
                    sock.connect((host, port))
                    sock.sendall(bytes(data, "utf-8"))
                    #count += 1
                    #print(count)
        else:
            data = str(code) + ',' + str(state)
            # Create a socket (SOCK_STREAM means a TCP socket)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server and send data
                sock.connect((host, port))
                sock.sendall(bytes(data, "utf-8"))
                #count += 1
                #print(count)
                
                #code, state = data.split(',')

                #if (code == 'ABS_Y') or (code == 'ABS_X'):
                #    sleep(0.5)
                
        sleep(0.001)
        
    # Receive data from the server and shut down
    #received = str(sock.recv(1024), "utf-8")

    #print("Sent:     {}".format(data))
    #print("Received: {}".format(received))





