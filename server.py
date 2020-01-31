import socketserver
from ev3dev.ev3 import *


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

    def stop(self):
        motor_left.run_forever(speed_sp=0)
        motor_right.run_forever(speed_sp=0)
        motor_a.run_forever(speed_sp=0)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print("{} wrote:".format(self.client_address[0])) # specifica ip
        self.code, self.state = self.data.decode('utf-8').split(',')

        if (self.code == 'BTN_SOUTH') and (self.state == '1'):
            print('A button pressed')
            self.forward()
        if (self.code == 'BTN_SOUTH') and (self.state == '0'):
            print('A button released')
            self.stop()
        if (self.code == 'BTN_SOUTH') and (self.state == '1'):
            print('A button pressed')
            self.forward()
        # if (self.code == 'BTN_SELECT') and (self.state == '1'):
        #    print('SELECT button pressed')
        #    self.stop()
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    motor_left = LargeMotor('outC')
    motor_right = LargeMotor('outB')
    motor_a = MediumMotor('outA')
    HOST, PORT = "192.168.43.219", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
