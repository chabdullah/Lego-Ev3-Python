#!/usr/bin/env python3
from __future__ import division
#from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveSteering
#from ev3dev2.motor import SpeedPercent, MoveTank
#from ev3dev2.sensor.lego import UltrasonicSensor
#from ev3dev2.led import Leds
import socketserver as socket

# TODO Create global function for leds color
# TODO Ripulire codice da commenti
# TODO Dividere questo file in due/tre classi (una per definire i controlli, una per il server)

# TCP HANDLER - It is instantiated once per connection to the server
class TCPHandler(socket.BaseRequestHandler):
    global motorSpeed
    motorSpeed = 30
    # TODO Flag to be used as manual start/stop switch; default is False (brick does not move)
    started = False

    # FUNCTION DEFINITIONS
    def forward(self, s):
        #print('forward')
        global motorSpeed
        #motorSpeed = float(motorSpeed)
        #print('prima di incrementare: ', motorSpeed)  # TODO DELETE
        if (s >= -386) and (s <= 128):
            self.stop()
        elif s == 32767:
            motorSpeed = -100.0
            print('max back: ',motorSpeed)
        else:
            # TODO Funzione di normalizzazione della velocità in base a s (il valore preso dalla levetta analogica)
            motorSpeed = ((-s)/32768.0)*100.0
            print(motorSpeed)
        #print('dopo aver incrementato: ', motorSpeed)  # TODO DELETE
        # motor.on(SpeedPercent(motorSpeed),SpeedPercent(motorSpeed))

    def forward_var(self):
        started = True  # TODO Delete this?
        #leds.set_color('LEFT','GREEN')
        #leds.set_color('RIGHT','GREEN')
        print('leds are green')
        print('forward_var')

    def backward_var(self):
        started = True  # TODO Delete this?
        #leds.set_color('LEFT','GREEN')
        #leds.set_color('RIGHT','GREEN')
        print('leds are green')
        print('backward_var')

    def stop(self):
        #leds.set_color('LEFT','YELLOW')
        #leds.set_color('RIGHT','YELLOW')
        #print('leds are yellow')
        print('stop')

    def turn(self, s):
        global motorSpeed
        if (s >= -129) and (s <= 385):
            self.stop()
        elif s == 32767:
            motorSpeed = 100.0
            print(motorSpeed)
        else:
            # TODO Funzione di normalizzazione della velocità in base a s (il valore preso dalla levetta analogica)
            motorSpeed = ((s)/32768.0)*100.0
            print(motorSpeed)

    def right_var(self):
        #leds.set_color('LEFT','GREEN')
        #leds.set_color('RIGHT','GREEN')
        print('leds are green')
        print('turn right var')

    def left_var(self):
        #leds.set_color('LEFT','GREEN')
        #leds.set_color('RIGHT','GREEN')
        print('leds are green')
        print('turn left var')

    def speed_up(self):
        global motorSpeed
        #print('prima di incrementare: ', motorSpeed)  # TODO DELETE
        if motorSpeed <= 90:
            motorSpeed = motorSpeed + 10
        else:
            print('Maximum motor speed reached.')
        #print('dopo aver incrementato: ', motorSpeed)  # TODO DELETE

    def speed_down(self):
        global motorSpeed
        #print('prima di decrementare: ', motorSpeed)  # TODO DELETE
        if motorSpeed >=20:
            motorSpeed = motorSpeed - 10
        else:
            print('Minimum motor speed reached.')
        #print('dopo aver decrementato: ', motorSpeed)  # TODO DELETE

    # TODO Understand what this function does and properly comment it
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print("{} wrote:".format(self.client_address[0])) # specifica ip
        self.code, self.state = self.data.decode('utf-8').split(',')

    # CONTROLS
    # A button: accelerate
    # B button: reverse
    # D-pad right button: turn right
    # D-pad left button: turn left
    # D-pad up button: speed up (+10%)
    # D-pad down button: speed down (-10%)

        if (self.code == 'BTN_SOUTH') and (self.state == '1'):
            print('A button pressed')
            self.forward_var()
        if (self.code == 'BTN_SOUTH') and (self.state == '0'):
            print('A button released')
            self.stop()

        if (self.code == 'BTN_EAST') and (self.state == '1'):
            print('B button pressed')
            self.backward_var()
        if (self.code == 'BTN_EAST') and (self.state == '0'):
            print('B button released')
            self.stop()

        if (self.code == 'ABS_HAT0X') and (self.state == '1'):
            print('D-pad right button pressed')
            self.right_var()

        if (self.code == 'ABS_HAT0X') and (self.state == '-1'):
            print('D-pad left button pressed')
            self.left_var()

        if (self.code == 'ABS_HAT0Y') and (self.state == '-1'):
            self.speed_up()

        if (self.code == 'ABS_HAT0Y') and (self.state == '1'):
            self.speed_down()

        # ABS_Y a riposo: -129
        # ABS_Y in su: segno negativo (valore massimo: -32768)
        # ABS_Y in basso: segno positivo (valore massimo: 32767)
        if (self.code == 'ABS_Y'):
            #print('Left analog stick moved up')
            #print(self.state)
            self.forward(float(self.state))

        if (self.code == 'ABS_X'):
            #print('Left analog stick moved right')
            #print(self.state)
            self.turn(float(self.state))

        # TODO Again, understand what this does and properly comment it
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    
    # BRICK INITIALIZATION
    # Brick LEDs
    #leds = Leds()

    # Ultrasonic sensor
    #ultrasonic = UltrasonicSensor()

    # Drive using two motors
    #motor = MoveTank(OUTPUT_A, OUTPUT_D)
    #steer = MoveSteering(OUTPUT_A, OUTPUT_D)

    # Parameters
    print('main:', motorSpeed)
    steeringValue = -100  # Steering value (to be used when turning around); goes from -100 to 100
    steeringSpeed = 30
    steeringDegrees = 0.5  # TODO Find the right value for 90 degrees steering
    minDistance = 20  # Minimum distance (in cm) before the brick starts decelerating or stops to turn around

    # TODO Flag to be used as manual start/stop switch; default is False (brick does not move)
    started = False

    
    # SERVER SETTINGS & CREATION
    host = '192.168.43.43'
    port = 9998

    server = socket.TCPServer((host, port), TCPHandler)  # Creates the server, binding to the specified host and port

    try:
        server.serve_forever()  # Activates the server, which will keep running until the user stops the program with Ctrl+C (KeyboardInterrupt exception)
    except KeyboardInterrupt:
        print('\n Stopped by user. Data is not being received anymore.')