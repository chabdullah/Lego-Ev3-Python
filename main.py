#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here
#brick.sound.beep()
motorSpeed = 200

# Initialize
motorA = Motor(Port.A)
motorD = Motor(Port.D)
ultrasonic = UltrasonicSensor(Port.S2)
colorSensor1 = ColorSensor(Port.S1)
colorSensor4 = ColorSensor(Port.S4)

# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
motorA.run(motorSpeed)
motorD.run(motorSpeed)

# Play another beep sound.
# This time with a higher pitch (1000 Hz) and longer duration (500 ms).
#brick.sound.beep(1000, 500)


while True:
    while (not any(brick.buttons())) and  not (ultrasonic.distance() < 200) :
        print(ultrasonic.distance())
        wait(10)
    brick.display.clear()    
    if Button.LEFT in brick.buttons():
        brick.light(Color.GREEN)
        motorSpeed = 100
        motorA.run(motorSpeed)
        motorD.run(motorSpeed)
    if Button.RIGHT in brick.buttons():
        brick.light(Color.RED)
        motorSpeed = 500
        motorA.run(motorSpeed)
        motorD.run(motorSpeed)  
    if ultrasonic.distance() < 200:
        motorA.stop()
        motorD.stop()
        #brick.sound.file(SoundFile.CRYING,50)
        wait(50)
        while (ultrasonic.distance() < 200):
            motorA.run_angle(200,-174,Stop.COAST,False)
            motorD.run_angle(200,+174)
        #wait(1000)
        motorSpeed = 200
        motorA.run(motorSpeed)
        motorD.run(motorSpeed)