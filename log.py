import matplotlib.pyplot as plt
import json
import numpy as np
import os

def read_log():
    command = "sshpass -p scp 'maker' robot@ev3dev.local:/home/robot/Lego-v3/log.json ./"
    os.system(command)

    with open("./log.json", "r") as f:
        data = f.read()
        data = data.split("\n")
        data.pop(-1)
        for i, misurazione in enumerate(data):
            info = eval(misurazione)
            motoreA = info['motor_A']
            motoreD = info['motor_D']
            targetA = (np.array(info['target_A'])*1050)/100
            targetD = (np.array(info['target_D'])*1050)/100
            start = info['start']
            start = start.split(" ")[1]
            finish = info['finish']
            finish = finish.split(" ")[1]
            time_sample = range(len(motoreA))

            plt.cla()
            fig, (ax1, ax2) = plt.subplots(2, sharex=True)
            ax1.plot(time_sample,motoreA, c="black", label="Motore A")
            ax2.plot(time_sample,motoreD, c="black", label="Motore D")
            ax1.plot(time_sample,targetA, c="r", label="Velocita' target A")
            ax2.plot(time_sample,targetD, c="r", label="Velocita' target D")
            ax1.set(ylabel="grad/sec")
            ax2.set(xlabel="time \n Start: "+start+ " finish: "+finish, ylabel="grad/sec")
            fig.legend()
            fig.tight_layout()
            fig.savefig("./plots/"+start+".png")



read_log()
print("Plotted")