class control():

    currentSpeed = motorSpeed
    print('dentro la classe')
    # TODO Flag to be used as manual start/stop switch; default is False (brick does not move)
    started = False
    #motorSpeed = 30  # Default motor speed (%)

    # FUNCTION DEFINITIONS
    def forward(self):
        started = True  # TODO Delete this?
        #leds.set_color('LEFT','GREEN')
        #leds.set_color('RIGHT','GREEN')
        print('leds are green')
        print('forward')

    def backward(self):
        started = True  # TODO Delete this?
        #leds.set_color('LEFT','GREEN')
        #leds.set_color('RIGHT','GREEN')
        print('leds are green')
        print('backward')

    def stop(self):
        #leds.set_color('LEFT','YELLOW')
        #leds.set_color('RIGHT','YELLOW')
        print('leds are yellow')
        print('stop')

    def turn_right(self):
        #leds.set_color('LEFT','GREEN')
        #leds.set_color('RIGHT','GREEN')
        print('leds are green')
        print('turn right')

    def turn_left(self):
        #leds.set_color('LEFT','GREEN')
        #leds.set_color('RIGHT','GREEN')
        print('leds are green')
        print('turn left')

    def speed_up(self):
        print(self.currentSpeed)
        #if self.motorSpeed <= 90:
        self.currentSpeed = self.currentSpeed + 10
        #else:
        #    print('Maximum motor speed reached.')
        print(self.currentSpeed)

    def speed_down(self):
        print(self.motorSpeed)
        if self.motorSpeed >= 20:
            self.motorSpeed -= 10
        else:
            print('Minimum motor speed reached.')
        print(self.motorSpeed)

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

        if (self.code == 'ABS_HAT0Y') and (self.state == '-1'):
            print('D-pad up button pressed')
            self.speed_up()

        if (self.code == 'ABS_HAT0Y') and (self.state == '1'):
            print('D-pad down button pressed')
            self.speed_down()
