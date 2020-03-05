import datetime as datetime  # For time intervals
import numpy as np
import matplotlib.pyplot as plt


def read_log():
    with open('./log.json', 'r') as f:
        # Data reading
        data = f.read()
        data = data.split('\n')
        data.pop(-1)

        for i, reading in enumerate(data):
            info = eval(reading)

            # Data
            motor_l = info['motor_A']
            motor_r = info['motor_D']
            target_l = (np.array(info['target_A']) * 1050) / 100
            target_r = (np.array(info['target_D']) * 1050) / 100

            # Start/finish times
            start = info['start']
            start = start.split(' ')[1]
            finish = info['finish']
            finish = finish.split(' ')[1]

            # Logging time interval
            s = datetime.datetime.strptime(start.split(',')[0], '%H:%M:%S.%f')
            f = datetime.datetime.strptime(finish.split(',')[0], '%H:%M:%S.%f')
            interval = (f-s).total_seconds() * 10

            # Plot time sample
            time_sample = range(len(motor_l))

            # Figure creation
            plt.cla()
            fig, (ax1, ax2) = plt.subplots(2, sharex=True)

            # Log data plotting
            ax1.set(xlim=(0, interval))
            ax2.set(xlim=(0, interval))
            ax1.plot(time_sample, motor_l, c='black', label='Left motor')
            ax2.plot(time_sample, motor_r, c='black', label='Right motor')
            ax1.plot(time_sample, target_l, c='r', label='Left motor target speed')
            ax2.plot(time_sample, target_r, c='r', label='Right motor target speed')

            # Plot labels
            ax1.set(ylabel='deg/s')
            ax2.set(xlabel='ms\n\nLogging start time: ' + start + ', logging finish time: ' + finish, ylabel='deg/s')

            # Figure saving
            fig.legend()
            fig.tight_layout()
            fig.savefig('./plots/' + start.replace(':', '-') + '.png')  # Replaces ':' character to avoid naming issues under Windows


read_log()
