#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Initialization

# brick.sound.beep()  # Play a beep sound
# brick.sound.beep(1000, 500)  # Play another beep sound, this time with a higher pitch (1000 Hz) and longer duration (500 ms)

brick.display.clear()
brick.light(Color.RED)  # Brick LED is red during initialization


motorL = Motor(Port.A)  # Left motor
motorR = Motor(Port.D)  # Right motor
ultrasonic = UltrasonicSensor(Port.S2)  # Ultrasonic sensor

motorSpeed = 200  # Motor speed
steeringSpeed = 200  # Steering speed (to be used when turning around)
minDistance = 200  # Minimum distance (in mm) before the brick starts decelerating or stops to turn around
maxSpeed = 400

started = False  # Flag to be used as manual start/stop switch; default is False (brick does not move)

###############################################################################################

while True:
    brick.light(Color.YELLOW)  # Brick LED is yellow when ready (waiting for a button press)

    if any(brick.buttons()):  # If a button is pressed
        started = True  # The start/stop flag is set to True (start)
        brick.light(Color.GREEN)  # Brick LED becomes green
        # Run the motors up to 'motorSpeed' degrees per second:
        motorL.run(motorSpeed)
        motorR.run(motorSpeed)


    while started is True:
        # Check if there is enough space; if not, stop, turn 90 degrees, then start running again
        if ultrasonic.distance() < minDistance:
            # Stop the motors:
            tempSpeed = motorSpeed
            for i in range(1,100):
                tempSpeed = tempSpeed - 1
                motorL.run(tempSpeed)
                motorR.run(tempSpeed)
                #wait(100)
            motorL.stop()              
            motorR.stop()
            # Turn 90 degrees until there is enough space to start running again:
            death = 4

            while ultrasonic.distance() < minDistance:
                #motorL.set_run_settings(maxSpeed, 400)
                #motorR.set_run_settings(maxSpeed, 400)
                motorL.run_angle(steeringSpeed, -174, Stop.COAST, False)
                motorR.run_angle(steeringSpeed, +174)
                death -= 1
                if(death == 0):
                    started = False
                    break
            # Run the motors up to 'motorSpeed' degrees per second:
            if death != 0:
                motorL.run(motorSpeed)
                motorR.run(motorSpeed)

        # If a button is pressed while the brick is running, stop the motors and set 'started' to False (thus exiting the loop and waiting for the next button press)
        if any(brick.buttons()):
            # Stop the motors:
            motorL.stop()
            motorR.stop()
            started = False
