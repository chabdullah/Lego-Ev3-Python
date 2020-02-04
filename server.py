#!/usr/bin/env python3
from __future__ import division
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveSteering
from ev3dev2.motor import SpeedPercent, MoveTank
#from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.led import Leds
import socketserver as socket

# TODO Ripulire codice da commenti
# TODO Dividere questo file in due/tre classi (una per definire i controlli, una per il server)

# TCP HANDLER - It is instantiated once per connection to the server
class TCPHandler(socket.BaseRequestHandler): 
    global motorSpeed
    global motorSpeed_var
    motorSpeed = 30
    motorSpeed_var = 30

    # FUNCTION DEFINITIONS
    def forward(self, s):
        global motorSpeed
        self.leds_green()
        print('questo è s: ',s)
        if (s >= -386) and (s <= 128):  # -386/+128
            print('ciao')
            #print(motorSpeed)
            self.stop()
            print('dopo lo stop: ',motorSpeed)
        elif s == 32767:
            motorSpeed = -100.0
            print('max back: ',motorSpeed)
            motor.on(SpeedPercent(motorSpeed),SpeedPercent(motorSpeed))
        else:
            # TODO Funzione di normalizzazione della velocità in base a s (il valore preso dalla levetta analogica)
            motorSpeed = ((-s)/32768.0)*100.0
            motor.on(SpeedPercent(motorSpeed),SpeedPercent(motorSpeed))

    def forward_var(self):
        self.leds_green()
        motor.on(SpeedPercent(motorSpeed_var),SpeedPercent(motorSpeed_var))

    def backward_var(self):
        self.leds_green()
        motor.on(SpeedPercent(-motorSpeed_var),SpeedPercent(-motorSpeed_var))

    def stop(self):
        self.leds_orange()
        motor.on(SpeedPercent(0),SpeedPercent(0))
        motor.off()  # Stop motors

    def turn(self, s):
        global motorSpeed
        self.leds_green()
        if (s >= -129) and (s <= 385):
            self.stop()
        elif s == 32767:
            motorSpeed = 100.0
            print(motorSpeed)
            motor.on(SpeedPercent(-motorSpeed_var),SpeedPercent(-motorSpeed_var))  # TODO
        else:
            motorSpeed = ((s)/32768.0)*100.0
            motor.on(SpeedPercent(-motorSpeed_var),SpeedPercent(-motorSpeed_var)) # TODO
            print(motorSpeed)

    def right_var(self):
        self.leds_green()
        steer.on_for_rotations(-steeringValue, steeringSpeed, steeringDegrees)

    def left_var(self):
        self.leds_green()
        steer.on_for_rotations(steeringValue, steeringSpeed, steeringDegrees)

    def speed_up(self):
        global motorSpeed_var
        if motorSpeed_var <= 90:
            motorSpeed_var += 10
        else:
            print('Maximum motor speed reached.')

    def speed_down(self):
        global motorSpeed_var
        if motorSpeed_var >= 20:
            motorSpeed_var -= 10
        else:
            print('Minimum motor speed reached.')

    def leds_green(self):
        leds.set_color('LEFT','GREEN')
        leds.set_color('RIGHT','GREEN')

    def leds_orange(self):
        leds.set_color('LEFT','ORANGE')
        leds.set_color('RIGHT','ORANGE')


    # TODO Understand what this function does and properly comment it
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print("{} wrote:".format(self.client_address[0])) # specifica ip
        self.code, self.state = self.data.decode('utf-8').split(',')

        #motorSpeed = 30  # Default motor speed (%)

        # CONTROLS
        # A button: accelerate
        # B button: reverse
        # D-paself.stop()d right button: turn right
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

        if (self.code == 'BTN_START') and (self.state == '1'):
            print('START button pressed')
            self.stop()

        if (self.code == 'BTN_SELECT') and (self.state == '1'):
            pass

        if (self.code == 'ABS_HAT0X') and (self.state == '1'):
            print('D-pad right button pressed')
            self.right_var()

        if (self.code == 'ABS_HAT0X') and (self.state == '-1'):
            print('D-pad left button pressed')
            self.left_var()

        if (self.code == 'ABS_HAT0Y') and (self.state == '-1'):
            print('D-pad up button pressed')
            self.speed_up()

        if (self.code == 'ABS_HAT0Y') and (self.state == '1'):
            print('D-pad down button pressed')
            self.speed_down()

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
        #self.request.sendall(self.data.upper())





if __name__ == "__main__":
    
    # BRICK INITIALIZATION
    # Brick LEDs
    leds = Leds()

    # Ultrasonic sensor
    #ultrasonic = UltrasonicSensor()

    # Drive using two motors
    motor = MoveTank(OUTPUT_A, OUTPUT_D)
    steer = MoveSteering(OUTPUT_A, OUTPUT_D)

    # Parameters
    motorSpeed = 30  # Default motor speed (%)
    steeringValue = -100  # Steering value (to be used when turning around); goes from -100 to 100
    steeringSpeed = 30
    steeringDegrees = 0.554  # TODO Find the right value for 90 degrees steering
    minDistance = 20  # Minimum distance (in cm) before the brick starts decelerating or stops to turn around

    
    # SERVER SETTINGS & CREATION
    host = '192.168.43.219'
    port = 12397

    server = socket.TCPServer((host, port), TCPHandler)  # Creates the server, binding to the specified host and port

    #try:
    print("Ready")
    server.serve_forever()  # Activates the server, which will keep running until the user stops the program with Ctrl+C (KeyboardInterrupt exception)
    #except KeyboardInterrupt:
    #    print('\n Stopped by user. Data is not being received anymore.')
