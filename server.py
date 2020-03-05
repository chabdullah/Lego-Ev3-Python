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


# TCP HANDLER - It is instantiated once, at the connection to the server
class TCPHandler(socket.BaseRequestHandler):

    # Setup
    global motor_speed  # Default speed for variant forward/backward function
    global motor_speed_log  # Variable used to store the speed value to be logged
    global s_old  # Variable used to store the previous state received from the gamepad (only needed for left analog stick)
    global speed_x  # Current speed on left analog stick x axis
    global speed_y  # Current speed on left analog stick y axis
    global log_thread_started  # Flag to check if the log thread is started

    motor_speed = 30  # Default motor speed
    s_old = 0  # Default (previous) left analog stick state
    speed_x = 0  # Default speed on left analog stick x axis
    speed_y = 0  # Default speed on left analog stick y axis

    # AUXILIARY FUNCTIONS
    # Left analog stick moving function (forward/backward)
    def move(self, s, axis):  # Left analog stick move function
        global button  # Flag necessary for the log function to know which button is being used to move the brick (0 = A/B buttons, 1 = left analog stick)
        global speed_y
        global speed_x
        global s_old
        global l
        global r
        global l_log
        global r_log
        button = 1  # Default move button is left analog stick
        l = 0
        r = 0
        l_log = 0
        r_log = 0
        percent = 15  # Minimum percentage to be reached before activating x axis

        self.leds_green()

        if axis == 'ABS_Y':  # Speed on y axis
            if s > 0:
                reverse = True  # Flag to specific if the brick is moving forward or backward
            if s < 0 and (s - s_old) >= 1500:
                self.stop()
            elif s > 0 and (s - s_old) <= -1500:
                self.stop()
            else:
                speed_y = (-s / 32768.0) * 100.0
                if (-percent < speed_x) and (speed_x < percent):
                    speed_x = 0
                    r = speed_y
                    l = r
                    motor.on(SpeedPercent(speed_y),SpeedPercent(speed_y))
                else:
                    self.v = (100 - abs(speed_x)) * (speed_y / 100) + speed_y
                    self.w = (100 - abs(speed_y)) * (speed_x / 100) + speed_x
                    r = (self.v + self.w) / 2
                    l = (self.v - self.w) / 2
                    motor.on(SpeedPercent(l), SpeedPercent(r))
        else:  # Speed on x axis
            if s < 0 and (s-s_old) >= 1500:
                self.stop()
            elif s > 0 and (s-s_old) <= -1500:
                self.stop()
            else:
                speed_x = (-s / 32768.0) * 100.0
                self.v = (100 - abs(speed_x)) * (speed_y / 100) + speed_y
                self.w = (100 - abs(speed_y)) * (speed_x / 100) + speed_x
                r = (self.v + self.w) / 2
                l = (self.v - self.w) / 2
                motor.on(SpeedPercent(l), SpeedPercent(r))
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
        motor.on(SpeedPercent(motor_speed), SpeedPercent(motor_speed))

    # Variant backward function (B button)
    def backward(self):
        global button
        global motor_speed
        global motor_speed_log
        button = 0

        self.leds_green()
        motor_speed_log = - motor_speed
        motor.on(SpeedPercent(-motor_speed), SpeedPercent(-motor_speed))

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
        motor.on(SpeedPercent(0), SpeedPercent(0))
        motor.off()  # Stop motors

    # Variant right turn function (D-pad right button)
    def right(self):
        self.leds_green()
        steer.on_for_rotations(steering_value, motor_speed, steering_degrees)

    # Variant left turn function (D-pad left button)
    def left(self):
        self.leds_green()
        steer.on_for_rotations(-steering_value, motor_speed, steering_degrees)

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

    def log(self):  # TODO Verificare
        global log_thread_started  # Flag to check if the log thread is started

        if log_thread_started == False:
            log_thread_started = True
            logThread = LogThread('Thread Log')
            logThread.start()
        else:
            log_thread_started = False
            print('Sending log to client...')
            send_log()
            print('Log sent successfully!')
            print()

    # Data sending (to log file) function
    def send_log(self):
        # TODO Definire la funzione di invio del log; dovrebbe essere automatico (non invocata dall'utente premendo X)
        pass

    # Log file read function (here for debug purposes only)
    def read_log(self):
        d = []
        with open('log_prova.json') as f:
            for line in f:
                d.append(json.loads(line))
            pprint(d)  # d is an array of Python dictionaries, each containing an instance of logged data


    def handle(self):
        global reverse  # Flag to check if the brick is moving backwards

        self.data = self.request.recv(1024).strip()  # self.request is the TCP socket connected to the client
    
        self.code, self.state = self.data.decode('utf-8').split(',')  # Received data decoding

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
        # START button: emergency stop
        #
        # Y button: start/stop logging
        # X button: send log to client

        if (self.code == 'BTN_WEST') and (self.state == '1'):
            # print('Y button pressed')
            self.log()

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

        if (self.code == 'BTN_SELECT') and (self.state == '1'):
            # print('SELECT button pressed')
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


class UltrasonicThread(Thread):  # Distance checking thread
    def __init__(self):
        Thread.__init__(self)

    def stop(self):
        leds.set_color('LEFT','ORANGE')  # TODO Verificare
        leds.set_color('RIGHT','ORANGE')
        motor.on(SpeedPercent(0),SpeedPercent(0))
        motor.off() 

    def run(self):
        global wall
        global reverse
        period = 0.350

        while True:
            t = time()
            while True:
                if ultrasonic.distance_centimeters < min_distance and not reverse:
                    self.stop()
                    wall = True  # Flag indicating that there is an obstacle in front of the brick and it cannot be started again until it is removed from there
                else:
                    wall = False

                if time() - t >= period:
                    break
                else:
                    sleep(period - (time() - t))


class LogThread(Thread):
    def __init__(self, nome):
        Thread.__init__(self)
        self.nome = nome
    
    def run(self):
        global button
        global log_thread_started
        global motor_speed_log
        global motor_info_l
        global motor_info_r
        global l_log
        global r_log

        button = 1
        motor_speed_l = []  # A == L
        motor_speed_r = []  # D == R
        motor_target_l = []
        motor_target_r = []
        log_start = 0
        log_finish = 0

        period = 0.150

        log_start = str(datetime.datetime.now())

        print('Logging started...')

        while log_thread_started:  # TODO Verificare (aggiunta temporizzazione)
            t = time()
            motor_speed_l.append(motor_info_l.speed)
            motor_speed_r.append(motor_info_r.speed)

            if button == 1:  # Left analog stick
                motor_target_l.append(l_log)
                motor_target_r.append(r_log)
            else:  # A or B buttons
                motor_target_l.append(motor_speed_log)
                motor_target_r.append(motor_speed_log)

            if time() - t >= period:
                break
            else:
                sleep(period - (time() - t))

        log_finish = str(datetime.datetime.now())

        print('Logging ended.')

        data = {'start': log_start,
                'finish': log_finish,
                'motor_l': motor_speed_l,
                'motor_r': motor_speed_r,
                'target_l': motor_target_l,
                'target_r': motor_target_r
               }

        with open('log.json', 'a+') as f:
            print('Writing log to file...')
            f.write(str(data).replace("\'", "\"") + '\n')
            print('Done!')
            print()


class InfoThread (Thread):  # TODO Verificare
    def __init__(self):
        Thread.__init__(self)
        print('InfoThread started.')
    
    def run(self):
        global speed_x
        global speed_y
        global motor_info_r
        global motor_info_l

        print('R maximum motor speed: ' + motor_info_r.speed + ' deg/s, L maximum motor speed: ' + motor_info_l.speed +' deg/s')

        while True:
            sleep(1)
            print('R motor speed: ' + motor_info_r.speed + ' deg/s, L motor speed: ' + motor_info_l.speed + ' deg/s')


if __name__ == '__main__':

    leds = Leds()  # Brick LEDs
    ultrasonic = UltrasonicSensor()  # Ultrasonic sensor
    motor = MoveTank(OUTPUT_A, OUTPUT_D)  # Drive using two motors (tank mode)
    motor_info_l = Motor(OUTPUT_A)  # Get info from left motor
    motor_info_r = Motor(OUTPUT_D)  # Get info from right motor
    steer = MoveSteering(OUTPUT_A, OUTPUT_D)  # Steer using two motors (tank mode)

    # Parameters
    steering_value = 100  # Steering value (to be used when turning around); goes from -100 to 100
    steering_degrees = 0.554  # Steering degrees value necessary to turn 45 degrees (empirical)
    min_distance = 20  # Minimum distance (in cm) before the brick starts decelerating or stops to turn around

    # Flags
    global log_thread_started
    log_thread_started = False
    wall = False
    reverse = False
    
    # Server settings
    host = '192.168.43.219'
    port = 12397

    # Server initialization
    print('Initializing server...')
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
