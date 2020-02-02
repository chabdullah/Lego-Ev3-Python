#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveSteering
from ev3dev2.motor import SpeedPercent, MoveTank
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.led import Leds
import socketserver as socket

# TCP HANDLER - It is instantiated once per connection to the server
class TCPHandler(socket.BaseRequestHandler): 
    # TODO Flag to be used as manual start/stop switch; default is False (brick does not move)
    started = False

    # FUNCTION DEFINITIONS
    def forward(self):
        started = True  # TODO Delete this?
        leds.set_color('LEFT','GREEN')
        leds.set_color('RIGHT','GREEN')
        motor.on(SpeedPercent(motorSpeed),SpeedPercent(motorSpeed))

    def backward(self):
        started = True  # TODO Delete this?
        leds.set_color('LEFT','GREEN')
        leds.set_color('RIGHT','GREEN')
        motor.on(SpeedPercent(-motorSpeed),SpeedPercent(-motorSpeed))

    def stop(self):
        leds.set_color('LEFT','YELLOW')
        leds.set_color('RIGHT','YELLOW')
        motor.off()  # Stop motors

    def turn_right(self):
        leds.set_color('LEFT','GREEN')
        leds.set_color('RIGHT','GREEN'
        steer.on_for_rotations(-steeringValue, steeringSpeed, steeringDegrees)

    def turn_left(self):
        leds.set_color('LEFT','GREEN')
        leds.set_color('RIGHT','GREEN'
        steer.on_for_rotations(steeringValue, steeringSpeed, steeringDegrees)

    def speed_up(self):
        if motorSpeed <= 90:
            motorSpeed += 10
        else:
            print('Maximum motor speed reached.')
        print(motorSpeed)

    def speed_down(self):
        if motorSpeed >= 20:
            motorSpeed -= 10
        else:
            print('Minimum motor speed reached.')
        print(motorSpeed)

    # TODO Understand what this function does and properly comment it
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print("{} wrote:".format(self.client_address[0])) # specifica ip
        self.code, self.state = self.data.decode('utf-8').split(',')

    motorSpeed = 30  # Default motor speed (%)

    # CONTROLS
    # A button: accelerate
    # B button: reverse
    # D-pad right button: turn right
    # D-pad left button: turn left
    # D-pad up button: speed up (+10%)
    # D-pad down button: speed down (-10%)

        if (self.code == 'BTN_SOUTH') and (self.state == '1'):
            print('A button pressed')
            self.forward()
        if (self.code == 'BTN_SOUTH') and (self.state == '0'):
            print('A button released')
            self.stop()

        if (self.code == 'BTN_EAST') and (self.state == '1'):
            print('B button pressed')
            self.backward()
        if (self.code == 'BTN_EAST') and (self.state == '0'):
            print('B button released')
            self.stop()

        if (self.code == 'ABS_HAT0X') and (self.state == '1'):
            print('D-pad right button pressed')
            self.turn_right()

        if (self.code == 'ABS_HAT0X') and (self.state == '-1'):
            print('D-pad left button pressed')
            self.turn_left()

        if (self.code == 'ABS_HAT0Y') and (self.state == '1'):
            print('D-pad up button pressed')
            self.speed_up()

        if (self.code == 'ABS_HAT0Y') and (self.state == '-1'):
            print('D-pad down button pressed')
            self.speed_down()

        # TODO Again, understand what this does and properly comment it
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())





if __name__ == "__main__":
    
    # BRICK INITIALIZATION
    # Brick LEDs
    leds = Leds()

    # Ultrasonic sensor
    ultrasonic = UltrasonicSensor()

    # Drive using two motors
    motor = MoveTank(OUTPUT_A, OUTPUT_D)
    steer = MoveSteering(OUTPUT_A, OUTPUT_D)

    # Parameters
    motorSpeed = 30  # Default motor speed (%)
    steeringValue = -100  # Steering value (to be used when turning around); goes from -100 to 100
    steeringSpeed = 30
    steeringDegrees = 0.5  # TODO Find the right value for 90 degrees steering
    minDistance = 20  # Minimum distance (in cm) before the brick starts decelerating or stops to turn around

    # TODO Flag to be used as manual start/stop switch; default is False (brick does not move)
    started = False

    
    # SERVER SETTINGS & CREATION
    host = '192.168.43.219'
    port = 9999

    server = socket.TCPServer((host, port), TCPHandler)  # Creates the server, binding to the specified host and port

    try:
        server.serve_forever()  # Activates the server, which will keep running until the user stops the program with Ctrl+C (KeyboardInterrupt exception)
    except KeyboardInterrupt:
        print('\n Stopped by user. Data is not being received anymore.')