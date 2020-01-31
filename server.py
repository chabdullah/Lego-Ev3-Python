import socketserver
from ev3dev.ev3 import *
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, MoveSteering
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    

    def forward(self):
        motor_left.run_forever(speed_sp=450)
        motor_right.run_forever(speed_sp=450)

    def backward(self):
        motor_left.run_forever(speed_sp=-450)
        motor_right.run_forever(speed_sp=-450)

    def stop(self):
        motor_left.run_forever(speed_sp=0)
        motor_right.run_forever(speed_sp=0)

    def turn_right(self):
        steer.on_for_rotations(-steeringValue, steeringSpeed, steeringDegrees)

    def turn_left(self):
        steer.on_for_rotations(steeringValue, steeringSpeed, steeringDegrees)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print("{} wrote:".format(self.client_address[0])) # specifica ip
        self.code, self.state = self.data.decode('utf-8').split(',')

        if (self.code == 'BTN_SOUTH') and (self.state == '1'):
            print('A button pressed')
            self.forward()
            """ while True:
                print('sono nel ciclo')
                if ultrasonic.distance_centimeters < minDistance:
                    print('oh no un ostacolo!')
                    self.stop()  # Stop motors
                if (self.code == 'BTN_SOUTH') and (self.state == '0'):
                    print('riparto')
                    break """
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
            print('Right button pressed')
            self.turn_right()
        if (self.code == 'ABS_HAT0X') and (self.state == '-1'):
            print('Left button pressed')
            self.turn_left()
        # if (self.code == 'BTN_SELECT') and (self.state == '1'):
        #    print('SELECT button pressed')
        #    self.stop()
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    motor_left = LargeMotor('outD')
    motor_right = LargeMotor('outA')
    steer = MoveSteering(OUTPUT_A, OUTPUT_D)

    # Parameters
    motorSpeed = 30  # Motor speed (%)
    steeringValue = -100  # Steering value (to be used when turning around); goes from -100 to 100
    steeringSpeed = 30
    steeringDegrees = 0.5
    minDistance = 20  # Minimum distance (in cm) before the brick starts decelerating or stops to turn around
    # _maxSpeed = 400

    ultrasonic = UltrasonicSensor()


    HOST, PORT = "192.168.43.219", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()