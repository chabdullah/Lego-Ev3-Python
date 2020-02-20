import socket  # Data transmission
from ev3dev.ev3 import *  # LEGO MINDSTORMS EV3 ev3dev Python library
from inputs import get_gamepad  # Gamepad input
from time import sleep


# Auxiliary function for easy data sending
def send_data(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))  # Connects to server...
        sock.sendall(bytes(data, 'utf-8'))  # ...and sends data


# Setup
host = '192.168.43.219'  # Server IP
port = 12397  # Server port

stick_values_X = []  # Array used for collecting input events from the left analog stick (X axis)
stick_values_Y = []  # Array used for collecting input events from the left analog stick (Y axis)

sleep(0.05)  # Avoids lagging related problems


# Main loop
while True:  # Listens for gamepad input events and sends them to server

    events = get_gamepad()  # Gets input events generated by the gamepad

    if events[0].ev_type != 'Sync':  # Only considers 'Key' type events

        code = events[0].code  # Event code
        state = events[0].state  # Event state (pressed, released or somewhere in between for non-binary buttons)

        commands_to_send = 5  # Number of commands to send to server (needs to be reduced for the left analog stick to avoid lagging)

        # Left analog stick (X axis)
        if (code == 'ABS_X'):

            stick_values_X.append(state)  # Appends the value of an input to the stick_values_X array

            if len(stick_values_X) == commands_to_send:  # If the maximum number of events to collect before sending them to the server has been reached...
                data = 'ABS_X' + ',' + str(stick_values_X[commands_to_send-1])  # ...then the last event is sent...
                stick_values_X = []  # ...and the array is reset

                self.send_data(host, port, data)  # Actual sending of the data
        
        # Left analog stick (Y axis)
        elif (code == 'ABS_Y'):

            stick_values_Y.append(state)  # Appends the value of an input to the stick_values_Y array

            if len(stick_values_Y) == commands_to_send:  # If the maximum number of events to collect before sending them to the server has been reached...
                data = 'ABS_Y' + ',' + str(stick_values_Y[commands_to_send-1])  # ...then the last event is sent...
                stick_values_Y = []  # ...and the array is reset
                
                self.send_data(host, port, data)  # Actual sending of the data
        
        # Every other button
        else:
            data = str(code) + ',' + str(state)  # Data to be sent
            
            self.send_data(host, port, data)  # Actual sending of the data


        sleep(0.001)  # Avoids lagging related problems