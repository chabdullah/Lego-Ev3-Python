from time import time
from time import sleep

"""
class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name,)
        print('Elapsed: %.5f seconds' % (time.time() - self.tstart))



with Timer():
   
    # do stuff

    pass
"""

period = 3
while True:
    t = time()

    while True:
        elapsed = time() - t
        if elapsed >=period:
            break
        else:
            sleep(period-elapsed)

    print(elapsed)