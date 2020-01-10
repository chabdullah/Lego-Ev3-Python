#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from time import sleep

def stopFunction(motor,button,started):
    if button.any():
        motor.off()
        started = False

# INITIALIZATION

# Brick LED is red during initialization
leds = Leds()
leds.set_color("LEFT", "RED")
leds.set_color("RIGHT", "RED")

# Ultrasonic sensor
ultrasonic = UltrasonicSensor()

# Drive using two motors
motor = MoveTank(OUTPUT_A, OUTPUT_D)
steer = MoveSteering(OUTPUT_A, OUTPUT_D)

# Buttons
button = Button()

# Parameters
motorSpeed = 30  # Motor speed (%)
steeringValue = -100  # Steering value (to be used when turning around); goes from -100 to 100
steeringSpeed = 30
steeringDegrees = 0.5
minDistance = 20  # Minimum distance (in cm) before the brick starts decelerating or stops to turn around
# _maxSpeed = 400

# Flag to be used as manual start/stop switch; default is False (brick does not move)
started = False

while True:
    # Brick LED is yellow when ready (waiting for a button press)
    leds.set_color('LEFT','YELLOW')
    leds.set_color('RIGHT','YELLOW')

    if button.any():
        started = True
        leds.set_color('LEFT','GREEN')
        leds.set_color('RIGHT','GREEN')
        motor.on(SpeedPercent(motorSpeed),SpeedPercent(motorSpeed))

    while started is True:
        if ultrasonic.distance_centimeters < minDistance:
            motor.off()  # Stop motors
            death = 4
            while ultrasonic.distance_centimeters < minDistance:
                steer.on_for_rotations(steeringValue, steeringSpeed, steeringDegrees)
                death -= 1
                if(death == 0):
                    started = False
                    break
            # Run the motors up to 'motorSpeed' degrees per second:
            if death != 0:
                motor.on(SpeedPercent(motorSpeed),SpeedPercent(motorSpeed))