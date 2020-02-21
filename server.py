#!/usr/bin/env python3
from __future__ import division  # Better divisions
from threading import Thread  # Multi-threading
import socketserver as socket  # Data transmission
from time import sleep, time  # Sleeping (to avoid laggs) and timing
import datetime
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
    global motor_speed  # Default speed for variant forward/backward function
    global motor_speed_log
    global s_old  # Variable used to store the previous state received from the gamepad (only needed for left analog stick)
    global speed_x  # Current speed on left analog stick x axis
    global speed_y  # Current speed on left analog stick y axis
    global log_thread_started

    motor_speed = 30
    s_old = 0
    speed_x = 0
    speed_y = 0
    
    # Auxiliary function definitions

    # Left analog stick moving function (forward/backward)
    def move(self, s, axis):
        global button
        global speed_y
        global speed_x
        global s_old
        global l
        global r
        global l_log
        global r_log
        button = 1
        l = 0
        r = 0
        l_log = 0
        r_log = 0
        percent = 15  # Minimum percentage to be reached before activating x axis

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
                if (-percent < speed_x) and (speed_x < percent):
                    speed_x = 0
                    r = speed_y
                    l = r
                    motor.on(SpeedPercent(speed_y),SpeedPercent(speed_y))
                else:
                    self.v = (100-abs(speed_x))*(speed_y/100)+speed_y
                    self.w = (100-abs(speed_y))*(speed_x/100)+speed_x
                    r = (self.v+self.w)/2
                    l = (self.v-self.w)/2
                    motor.on(SpeedPercent(l),SpeedPercent(r))
        else:  # velocità su X
            if s<0 and (s-s_old)>=500:
                self.stop()
            elif s>0 and (s-s_old)<=-500:
                self.stop()
            else:
                speed_x = (-(s)/32768.0)*100.0
                self.v = (100-abs(speed_x))*(speed_y/100)+speed_y
                self.w = (100-abs(speed_y))*(speed_x/100)+speed_x
                r = (self.v+self.w)/2
                l = (self.v-self.w)/2
                motor.on(SpeedPercent(l),SpeedPercent(r))
        s_old = s
        l_log = l
        r_log = r
        
    # Variant forward function (A button)
    def forward(self):
        global button
        global motor_speed
        global motor_speed_log
        button = 0
        self.leds_green()
        motor_speed_log = motor_speed
        motor.on(SpeedPercent(motor_speed),SpeedPercent(motor_speed))

    # Variant backward function (B button)
    def backward(self):
        global button
        global motor_speed
        global motor_speed_log
        button = 0
        self.leds_green()
        motor_speed_log = - motor_speed
        motor.on(SpeedPercent(-motor_speed),SpeedPercent(-motor_speed))

    # Stop function
    def stop(self):
        global motor_speed_log
        global l_log
        global r_log
        global speed_x
        global speed_y
        motor_speed_log = 0
        l_log = 0
        r_log = 0
        speed_x = 0
        speed_y = 0
        self.leds_orange()
        motor.on(SpeedPercent(0),SpeedPercent(0))
        motor.off()  # Stop motors

    # Variant right turn function (D-pad right button)
    def right(self):
        self.leds_green()
        steer.on_for_rotations(-steeringValue, motor_speed, steeringDegrees)

    # Variant left turn function (D-pad left button)
    def left(self):
        self.leds_green()
        steer.on_for_rotations(steeringValue, motor_speed, steeringDegrees)

    # Variant speed up function (D-pad up button)
    def speed_up(self):
        global motor_speed
        if motor_speed <= 90:
            motor_speed += 10
            print('Motor speed: ', motor_speed, '%')
        else:
            print('Maximum motor speed reached.')

    # Variant speed down function (D-pad down button)
    def speed_down(self):
        global motor_speed
        if motor_speed >= 20:
            motor_speed -= 10
            print('Motor speed: ', motor_speed, '%')
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
        pass

    # Log file read function
    def read_log(self):
        d = []
        with open('log_prova.json') as f:
            for line in f:
                d.append(json.loads(line))
            pprint(d)  # d is an array of Python dictionaries, each containing an instance of logged data


    def handle(self):
        global reverse
        global log_thread_started

        self.data = self.request.recv(1024).strip()  # self.request is the TCP socket connected to the client
    
        self.code, self.state = self.data.decode('utf-8').split(',')

        # CONTROLS
        #
        # A button: forward
        # B button: backward
        # D-pad right button: turn right
        # D-pad left button: turn left
        # D-pad up button: speed up (+10%)
        # D-pad down button: speed down (-10%)
        #
        # Left analog stick: move (forward/backward/rotate)
        #
        # Start button: emergency stop
        #
        # Y button: start/stop logging
        # X button: send log to client

        if (self.code == 'BTN_WEST') and (self.state == '1'):
            # print('Y button pressed')
            if log_thread_started == False:
                log_thread_started = True
                logThread = LogThread('Thread Log')
                logThread.start()
            else:
                log_thread_started = False

        if (self.code == 'BTN_NORTH') and (self.state == '1'):
            # print('X button pressed')
            send_log()

        if (self.code == 'BTN_SOUTH') and (self.state == '1'):
            # print('A button pressed')
            self.forward()
        if (self.code == 'BTN_SOUTH') and (self.state == '0'):
            # print('A button released')
            self.stop()

        if (self.code == 'BTN_EAST') and (self.state == '1'):
            # print('B button pressed')
            reverse = True
            self.backward()
        if (self.code == 'BTN_EAST') and (self.state == '0'):
            # print('B button released')
            self.stop()
            reverse = False

        if (self.code == 'BTN_START') and (self.state == '1'):
            # print('START button pressed')
            self.stop()

        if (self.code == 'ABS_HAT0X') and (self.state == '1'):
            # print('D-pad right button pressed')
            self.right()

        if (self.code == 'ABS_HAT0X') and (self.state == '-1'):
            # print('D-pad left button pressed')
            self.left()

        if (self.code == 'ABS_HAT0Y') and (self.state == '-1'):
            # print('D-pad up button pressed')
            self.speed_up()

        if (self.code == 'ABS_HAT0Y') and (self.state == '1'):
            # print('D-pad down button pressed')
            self.speed_down()

        if (self.code == 'ABS_Y'):
            # print('Left analog stick moved along y axis')
            self.move(float(self.state), 'ABS_Y')

        if (self.code == 'ABS_X'):
            # print('Left analog stick moved along x axis')
            self.move(float(self.state), 'ABS_X')



# Distance checking thread
class UltrasonicThread(Thread):
    def __init__(self):  # def __init__(self, nome):
        Thread.__init__(self)
        # self.nome = nome
        # print('Thread Ultrasonic avviato')

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


class LogThread(Thread):
    def __init__(self, nome):
        Thread.__init__(self)
        self.nome = nome
    
    def run(self):
        global button
        global log_thread_started
        global motor_speed_log
        global motor_infoA
        global motor_infoD
        global l_log
        global r_log
        button = 1
        motor_speedA = []
        motor_speedD = []
        motor_targetA = []
        motor_targetD = []
        log_start = 0
        log_finish = 0

        log_start = str(datetime.datetime.now())

        print('Logging started...')

        while log_thread_started:
            motor_speedA.append(motor_infoA.speed)
            motor_speedD.append(motor_infoD.speed)
            if button == 1:  # Left analog stick
                motor_targetA.append(l_log)
                motor_targetD.append(r_log)
            else:  # A or B buttons
                motor_targetA.append(motor_speed_log)
                motor_targetD.append(motor_speed_log)
            sleep(0.1)

        log_finish = str(datetime.datetime.now())

        print('Logging ended.')

        data = {'start' : log_start,
                'finish' : log_finish,
                'motor_A': motor_speedA,
                'motor_D': motor_speedD,
                'target_A' : motor_targetA,
                'target_D' : motor_targetD}

        with open('log.json', 'a+') as f:
            print('Writing log to file...')
            f.write(str(data).replace("\'", "\"") + '\n')
            print('Done!')
            print()

            

class InfoThread (Thread):
    def __init__(self):
        Thread.__init__(self)
        print('InfoThread started.')
    
    def run(self):
        global speed_x
        global speed_y
        max_speed_infoA = Motor(OUTPUT_A)
        max_speed_infoD = Motor(OUTPUT_D)

        while True:
            sleep(1)
            #print('Speed_x: ',speed_x ,' Speed_y: ',speed_y)
            print('max speed A:', max_speed_infoA.max_speed, 'max speed D:', max_speed_infoD.max_speed)


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
    steeringValue = -100  # Steering value (to be used when turning around); goes from -100 to 100
    steeringDegrees = 0.554
    minDistance = 20  # Minimum distance (in cm) before the brick starts decelerating or stops to turn around

    # Flags
    global log_thread_started

    log_thread_started = False
    wall = False
    reverse = False
    
    # Sserver settings
    host = '192.168.43.219'
    port = 12397

    # Server initialization
    print('Inizializing server...')
    server = socket.TCPServer((host, port), TCPHandler)  # Creates the server, binding to the specified host and port

    # Secondary threads initialization
    print('Initializing threads...')
    ultrasonicThread = UltrasonicThread()
    ultrasonicThread.start()
    # infoThread = InfoThread()
    # infoThread.start()
    
    print('Ready.')
    print()
    readySound = Sound()
    readySound.tone(1000, 3)

    server.serve_forever()  # Activates the server, which will keep running until the user stops the program with Ctrl+C (KeyboardInterrupt exception)