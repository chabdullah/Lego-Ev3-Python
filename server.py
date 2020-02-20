#!/usr/bin/env python3
from threading import Thread  # Multi-threading
import socketserver as socket  # Data transmission
from __future__ import division  # Better divisions
from time import sleep, time  # Sleeping (to avoid laggs) and timing
import json  # JSON logging
from pprint import pprint  # Pretty print, for readable JSON [debug purposes only]

 # LEGO MINDSTORMS EV3 ev3dev Python library
from ev3dev2.led import Leds
from ev3dev2.motor import Motor, MoveTank, MoveSteering, SpeedPercent, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound

# TODO Dividere questo file in due/tre classi (una per definire i controlli, una per il server)

# TCP HANDLER - It is instantiated once per connection to the server
class TCPHandler(socket.BaseRequestHandler):

    # Setup
    global motor_speed_var  # Default speed for variant forward/backward function
    global s_old  # Variable used to store the previous state received from the gamepad (only needed for left analog stick)
    global speed_x  # Current speed on left analog stick x axis
    global speed_y  # Current speed on left analog stick y axis

    motor_speed_var = 30
    s_old = 0
    speed_x = 0
    speed_y = 0
    
    # Auxiliary function definitions

    # Left analog stick moving function (forward/backward)
    def move(self, s, axis):
        global speed_y
        global speed_x
        global s_old
        percent = 5  # Minimum percentage to be reached before activating x axis

        self.leds_green()

        if axis == 'ABS_Y':
            if s > 0:
                reverse = True
            if s<0 and (s-s_old)>=1500:
                self.stop()
            elif s>0 and (s-s_old)<=-1500:
                self.stop()
            else:
                speed_y = (-(s)/32768.0)*100.0
                if -percent < speed_x < percent:
                    motor.on(SpeedPercent(speed_y),SpeedPercent(speed_y))
                else:
                    self.v = (100-abs(speed_x))*(speed_y/100)+speed_y
                    self.w = (100-abs(speed_y))*(speed_x/100)+speed_x
                    self.r = (self.v+self.w)/2
                    self.l = (self.v-self.w)/2
                    motor.on(SpeedPercent(self.l),SpeedPercent(self.r))
        else:  # velocità su X
            if s<0 and (s-s_old)>=500:
                self.stop()
            elif s>0 and (s-s_old)<=-500:
                self.stop()
            else:
                speed_x = (-(s)/32768.0)*100.0
                self.v = (100-abs(speed_x))*(speed_y/100)+speed_y
                self.w = (100-abs(speed_y))*(speed_x/100)+speed_x
                self.r = (self.v+self.w)/2
                self.l = (self.v-self.w)/2
                motor.on(SpeedPercent(self.l),SpeedPercent(self.r))
        s_old = s
        
    # Variant forward function (A button)
    def forward(self):
        self.leds_green()
        motor.on(SpeedPercent(motor_speed_var),SpeedPercent(motor_speed_var))

    # Variant backward function (B button)
    def backward(self):
        self.leds_green()
        motor.on(SpeedPercent(-motor_speed_var),SpeedPercent(-motor_speed_var))

    # Stop function
    def stop(self):
        global speed_x
        global speed_y
        self.leds_orange()
        speed_x = 0
        speed_y = 0
        motor.on(SpeedPercent(0),SpeedPercent(0))
        motor.off()  # Stop motors

    # Variant right turn function (D-pad right button)
    def right(self):
        self.leds_green()
        steer.on_for_rotations(-steeringValue, steeringSpeed, steeringDegrees)

    # Variant left turn function (D-pad left button)
    def left(self):
        self.leds_green()
        steer.on_for_rotations(steeringValue, steeringSpeed, steeringDegrees)

    # Variant speed up function (D-pad up button)
    def speed_up(self):
        global motor_speed_var
        if motor_speed_var <= 90:
            motor_speed_var += 10
        else:
            print('Maximum motor speed reached.')

    # Variant speed down function (D-pad down button)
    def speed_down(self):
        global motor_speed_var
        if motor_speed_var >= 20:
            motor_speed_var -= 10
        else:
            print('Minimum motor speed reached.')

    # Led function (green)
    def leds_green(self):
        leds.set_color('LEFT','GREEN')
        leds.set_color('RIGHT','GREEN')

    # Led function (orange)
    def leds_orange(self):
        leds.set_color('LEFT','ORANGE')
        leds.set_color('RIGHT','ORANGE')

    # Data sending (to log file) function
    def send_log(self):
        data = {'MotoreA': motor_speedA, 'MotoreD': motor_speedD}

        with open('log.json', 'a+') as f:
            f.write(str(data).replace("\'", "\"") + '\n')

    # Log file read function
    def read_log(self):
        d = []
        with open('log_prova.json') as f:
            for line in f:
                d.append(json.loads(line))
            pprint(d)  # d is an array of Python dictionaries, each containing an instance of logged data


    def handle(self):
        global reverse

        self.data = self.request.recv(1024).strip()  # self.request is the TCP socket connected to the client
    
        self.code, self.state = self.data.decode('utf-8').split(',')

        # CONTROLS
        # A button: forward
        # B button: backward
        # D-pad right button: turn right
        # D-pad left button: turn left
        # D-pad up button: speed up (+10%)
        # D-pad down button: speed down (-10%)
        # Left analog stick: move (forward/backward/rotate)
        # Start button: emergency stop
        # Select button: manually send collected data to log

        if (self.code == 'BTN_SOUTH') and (self.state == '1'):
            #print('A button pressed')
            self.forward()
        if (self.code == 'BTN_SOUTH') and (self.state == '0'):
            #print('A button released')
            self.stop()

        if (self.code == 'BTN_EAST') and (self.state == '1'):
            #print('B button pressed')
            reverse = True
            self.backward()
        if (self.code == 'BTN_EAST') and (self.state == '0'):
            #print('B button released')
            self.stop()
            reverse = False

        if (self.code == 'BTN_START') and (self.state == '1'):
            #print('START button pressed')
            self.stop()

        if (self.code == 'BTN_SELECT') and (self.state == '1'):
            #print('SELECT button pressed')
            self.send_log()

        if (self.code == 'ABS_HAT0X') and (self.state == '1'):
            #print('D-pad right button pressed')
            self.right()

        if (self.code == 'ABS_HAT0X') and (self.state == '-1'):
            #print('D-pad left button pressed')
            self.left()

        if (self.code == 'ABS_HAT0Y') and (self.state == '-1'):
            #print('D-pad up button pressed')
            self.speed_up()

        if (self.code == 'ABS_HAT0Y') and (self.state == '1'):
            #print('D-pad down button pressed')
            self.speed_down()

        if (self.code == 'ABS_Y'):
            #print('Left analog stick moved up')
            #print(self.state)
            self.move(float(self.state), 'ABS_Y')

        if (self.code == 'ABS_X'):
            #print('Left analog stick moved right')
            #print(self.state)
            self.move(float(self.state), 'ABS_X')



# Distance checking thread
class UltrasonicThread(Thread):
    def __init__(self, nome):
        Thread.__init__(self)
        self.nome = nome
        print('Thread Ultrasonic avviato')

    def stop(self):
        #self.leds_orange()
        motor.on(SpeedPercent(0),SpeedPercent(0))
        motor.off() 

    def run(self):
        global wall
        global reverse
        period = 0.350
        while True:
            t = time()
            while True:
                if ultrasonic.distance_centimeters < minDistance and not reverse:
                    self.stop()
                    wall = True
                else:
                    wall = False
                if time()-t >= period:
                    break
                else:
                    sleep(period-(time() -t))


class LogThread (Thread):
    def __init__(self, nome):
        Thread.__init__(self)
        self.nome = nome
        print('Thread LogInfo avviato')
    
    def run(self):
        global motor_info
        global motor_info2
        global motor_speedA
        global motor_speedD
        while True:
            sleep(.5)
            motor_speedA.append(motor_infoA.speed)
            motor_speedD.append(motor_infoD.speed)

            

class InfoThread (Thread):
    def __init__(self):
        Thread.__init__(self)
        print('Thread infoSpeed avviato')
    
    def run(self):
        global speed_x
        global speed_y

        while True:
            sleep(0.5)
            print('Speed_x: ',speed_x ,' Speed_y: ',speed_y)



if __name__ == '__main__':
    
    # BRICK INITIALIZATION
    # Brick LEDs
    leds = Leds()

    # Ultrasonic sensor
    ultrasonic = UltrasonicSensor()

    # Drive using two motors
    motor = MoveTank(OUTPUT_A, OUTPUT_D)
    motor_infoA = Motor(OUTPUT_A)
    motor_infoD = Motor(OUTPUT_D)
    steer = MoveSteering(OUTPUT_A, OUTPUT_D)

    # Parameters
    motorSpeed = 30  # Default motor speed (%)
    steeringValue = -100  # Steering value (to be used when turning around); goes from -100 to 100
    steeringSpeed = 30
    steeringDegrees = 0.554  # TODO Find the right value for 90 degrees steering
    minDistance = 20  # Minimum distance (in cm) before the brick starts decelerating or stops to turn around

    wall = False
    reverse = False

    # Log info
    motor_speedA = []
    motor_speedD = []

    
    # SERVER SETTINGS & CREATION
    host = '192.168.43.219'
    port = 12397

    print('Inizializing server...')
    server = socket.TCPServer((host, port), TCPHandler)  # Creates the server, binding to the specified host and port

    try:
        print('Ready')
        readySound = Sound()
        readySound.tone(1000,1)
        ultrasonicThread = UltrasonicThread('Thread Ultrasonic')
        ultrasonicThread.start()
        logThread = LogThread('Thread Log')
        logThread.start()
        server.serve_forever()  # Activates the server, which will keep running until the user stops the program with Ctrl+C (KeyboardInterrupt exception)
    except KeyboardInterrupt:
        print('\n Stopped by user. Data is not being received anymore.')
