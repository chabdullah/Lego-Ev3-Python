#!/usr/bin/env python3
from __future__ import division
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveSteering
from ev3dev2.motor import SpeedPercent, MoveTank, Motor
#from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.led import Leds
import socketserver as socket
from threading import Thread
from time import sleep

# TODO Ripulire codice da commenti
# TODO Dividere questo file in due/tre classi (una per definire i controlli, una per il server)

# TCP HANDLER - It is instantiated once per connection to the server
class TCPHandler(socket.BaseRequestHandler): 
    global speed_y
    global speed_x
    global motorSpeed_var
    speed_y = 0
    speed_x = 0
    motorSpeed_var = 30

    # FUNCTION DEFINITIONS
    def forward(self, s, axis):
        global speed_y
        global speed_x
        percent = 5
        self.leds_green()
        #print('questo è s: ',s)
        print('x: ', speed_x, 'y: ', speed_y)
        if axis == 'ABS_Y':
            if (s >= -386) and (s <= 128):  # -386/+128
                #print('ciao')
                #print(speed_y)
                self.stop()
                #print('dopo lo stop: ',speed_y)
            elif s == 32767:
                speed_y = -100.0
                if speed_x > percent:
                    motor.on(SpeedPercent(speed_y),SpeedPercent(speed_x))
                elif speed_x < -percent:
                    motor.on(SpeedPercent(speed_x),SpeedPercent(speed_y))
                else:
                    #print('max back: ',speed_y)
                    motor.on(SpeedPercent(speed_y),SpeedPercent(speed_y))
            else:
                speed_y = ((-s)/32768.0)*100.0
                if speed_x > percent:
                    motor.on(SpeedPercent(speed_y),SpeedPercent(speed_x))
                elif speed_x < -percent:
                    motor.on(SpeedPercent(speed_x),SpeedPercent(speed_y))
                else:
                    motor.on(SpeedPercent(speed_y),SpeedPercent(speed_y))
        else:  # velocità su X
            if (s >= -129) and (s <= 385):  # -129/+385
                #print('ciao')
                #print(speed_y)
                speed_x = 0.0
                motor.on(SpeedPercent(speed_y),SpeedPercent(speed_y))
                #self.stop()
            elif s == 32767:
                speed_x = 0.0
                #print('max back: ',speed_y)
                motor.on(SpeedPercent(speed_y),SpeedPercent(speed_x))
            else:
                # TODO Funzione di normalizzazione della velocità in base a s (il valore preso dalla levetta analogica)
                speed_x = ((abs(s))/32768.0)*100.0
                speed_x = (speed_y/100.0)*speed_x
                #print(speed_x)
                if s > 385:
                    motor.on(SpeedPercent(speed_y),SpeedPercent(speed_x))
                elif s < -129:
                    motor.on(SpeedPercent(speed_x),SpeedPercent(speed_y))

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

    '''
    def turn(self, s):
        global speed_y
        self.leds_green()
        if (s >= -129) and (s <= 385):
            self.stop()
        elif s == 32767:
            speed_y = 100.0
            print(speed_y)
            motor.on(SpeedPercent(-motorSpeed_var),SpeedPercent(-motorSpeed_var))  # TODO
        else:
            speed_y = ((s)/32768.0)*100.0
            motor.on(SpeedPercent(-motorSpeed_var),SpeedPercent(-motorSpeed_var)) # TODO
            print(speed_y)
    '''

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

        #speed_y = 30  # Default motor speed (%)

        # CONTROLS
        # A button: accelerate
        # B button: reverse
        # D-paself.stop()d right button: turn right
        # D-pad left button: turn left
        # D-pad up button: speed up (+10%)
        # D-pad down button: speed down (-10%)

        if (self.code == 'BTN_SOUTH') and (self.state == '1'):
            #print('A button pressed')
            self.forward_var()
        if (self.code == 'BTN_SOUTH') and (self.state == '0'):
            #print('A button released')
            self.stop()

        if (self.code == 'BTN_EAST') and (self.state == '1'):
            #print('B button pressed')
            self.backward_var()
        if (self.code == 'BTN_EAST') and (self.state == '0'):
            #print('B button released')
            self.stop()

        if (self.code == 'BTN_START') and (self.state == '1'):
            #print('START button pressed')
            self.stop()

        if (self.code == 'BTN_SELECT') and (self.state == '1'):
            pass

        if (self.code == 'ABS_HAT0X') and (self.state == '1'):
            #print('D-pad right button pressed')
            self.right_var()

        if (self.code == 'ABS_HAT0X') and (self.state == '-1'):
            #print('D-pad left button pressed')
            self.left_var()

        if (self.code == 'ABS_HAT0Y') and (self.state == '-1'):
            #print('D-pad up button pressed')
            self.speed_up()

        if (self.code == 'ABS_HAT0Y') and (self.state == '1'):
            #print('D-pad down button pressed')
            self.speed_down()

        if (self.code == 'ABS_Y'):
            #print('Left analog stick moved up')
            #print(self.state)
            self.forward(float(self.state), 'ABS_Y')

        if (self.code == 'ABS_X'):
            #print('Left analog stick moved right')
            #print(self.state)
            self.forward(float(self.state), 'ABS_X')

        # TODO Again, understand what this does and properly comment it
        # just send back the same data, but upper-cased
        #self.request.sendall(self.data.upper())




class UltrasonicThread (Thread):
    def __init__(self, nome):
        Thread.__init__(self)
        self.nome = nome
        print("Thread Ultrasonic avviato")

    def stop(self):
        #self.leds_orange()
        motor.on(SpeedPercent(0),SpeedPercent(0))
        motor.off() 

    def run(self):
        global wall
        period = 0.350
        while True:
            t = time()
            while True:
                if ultrasonic.distance_centimeters < minDistance:
                    self.stop()
                    wall = True
                else:
                    wall = False
                if time()-t >= period:
                    break
                else:
                    sleep(period-(time() -t))


class MotorInfoThread (Thread):
    def __init__(self, nome):
        Thread.__init__(self)
        self.nome = nome
        print("Thread MotorInfo avviato")
    
    def run(self):
        global motor_info
        global motor_info2
        while True:
            sleep(1)
            print("A: ",motor_info.speed, " D: ",motor_info2.speed)
            print("A: ",motor_info.position%360, " D: ",motor_info2.position%360)
            print("_"*50)



if __name__ == "__main__":
    
    # BRICK INITIALIZATION
    # Brick LEDs
    leds = Leds()

    # Ultrasonic sensor
    ultrasonic = UltrasonicSensor()

    # Drive using two motors
    motor = MoveTank(OUTPUT_A, OUTPUT_D)
    motor_info = Motor(OUTPUT_A)
    motor_info2 = Motor(OUTPUT_D)
    steer = MoveSteering(OUTPUT_A, OUTPUT_D)

    # Parameters
    motorSpeed = 30  # Default motor speed (%)
    steeringValue = -100  # Steering value (to be used when turning around); goes from -100 to 100
    steeringSpeed = 30
    steeringDegrees = 0.554  # TODO Find the right value for 90 degrees steering
    minDistance = 20  # Minimum distance (in cm) before the brick starts decelerating or stops to turn around

    wall = False

    
    # SERVER SETTINGS & CREATION
    host = '192.168.43.219'
    port = 12397

    print("Inizializing server...")
    server = socket.TCPServer((host, port), TCPHandler)  # Creates the server, binding to the specified host and port

    #try:
    print("Ready")
    ultrasonicThread = UltrasonicThread("Thread Ultrasonic")
    ultrasonicThread.start()
    motorInfoThread = MotorInfoThread("Thread MotorInfo")
    motorInfoThread.start()
    server.serve_forever()  # Activates the server, which will keep running until the user stops the program with Ctrl+C (KeyboardInterrupt exception)
    #except KeyboardInterrupt:
    #    print('\n Stopped by user. Data is not being received anymore.')