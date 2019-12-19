#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Initialization

# TODO Visualizzare un'immagine (tipo logo) o del testo (ad es. nome e cognome studenti) all'avvio
# TODO Similmente, fare un beep/suono di qualche tipo, sempre all'avvio (vedi esempi qui sotto)
# brick.sound.beep()  # Play a beep sound
# brick.sound.beep(1000, 500)  # Play another beep sound, this time with a higher pitch (1000 Hz) and longer duration (500 ms)

brick.display.clear()
brick.light(Color.RED)  # Brick LED is red during initialization
# TODO Provare a vedere se funzionano altri colori per il LED (nella documentazione c'è un elenco più lungo)

motorL = Motor(Port.A)  # Left motor
motorR = Motor(Port.D)  # Right motor
ultrasonic = UltrasonicSensor(Port.S2)  # Ultrasonic sensor

motorSpeed = 200  # Motor speed
steeringSpeed = 200  # Steering speed (to be used when turning around)
minDistance = 200  # Minimum distance (in mm) before the brick starts decelerating or stops to turn around
# TODO Altri parametri di default (bisogna vedere la libreria cosa ci permette di fare, ad es. set_run_settings)

started = False  # Flag to be used as manual start/stop switch; default is False (brick does not move)

###############################################################################################

# TODO Implementare il meccanismo di start/stop tramite la pressione di un pulsante con un'interruzione (ovvero il modo corretto per farlo)

while True:
    brick.light(Color.YELLOW)  # Brick LED is yellow when ready (waiting for a button press)

    if any(brick.buttons()):  # If a button is pressed
        started = True  # The start/stop flag is set to True (start)
        brick.light(Color.GREEN)  # Brick LED becomes green
        # Run the motors up to 'motorSpeed' degrees per second:
        motorL.run(motorSpeed)
        motorR.run(motorSpeed)


    # TODO IMPORTANTE Al Basso piacerebbe temporizzare in maniera precisa il campionamento della distanza (e.g. ogni tot secondi, incluso il tempo di esecuzione delle istruzioni; da capire se c'è qualche funzione nella libreria o va fatto a mano)
    while started is True:
        # Check if there is enough space; if not, stop, turn 90 degrees, then start running again
        if ultrasonic.distance() < minDistance:
            # TODO Inserire un suono quando trova un ostacolo (?), vedi sotto:
            # brick.sound.file(SoundFile.CRYING, 50)
            # TODO Bisognerebbe decelerare in maniera più graduale invece di fermarsi di colpo
            # Stop the motors:
            motorL.stop()
            motorR.stop()
            # Turn 90 degrees until there is enough space to start running again:
            # TODO Qui forse si potrebbe utilizzare la funzione drive(speed, steering) per girare il robot (vedi pag. 38)
            while ultrasonic.distance() < minDistance:
                motorL.run_angle(steeringSpeed, -174, Stop.COAST, False)  # TODO Controllare che i motori siano nell'ordine giusto
                motorR.run_angle(steeringSpeed, +174)
            # Run the motors up to 'motorSpeed' degrees per second:
            motorL.run(motorSpeed)
            motorR.run(motorSpeed)

        # If a button is pressed while the brick is running, stop the motors and set 'started' to False (thus exiting the loop and waiting for the next button press)
        if any(brick.buttons()):
            # Stop the motors:
            motorL.stop()
            motorR.stop()
            started = False


# TODO (actually a silly idea) Se mai implementeremo una funzione di retromarcia, sarà mandatorio metterci il 'beep beep' (tipo quello dei camion in retromarcia, per capirsi)