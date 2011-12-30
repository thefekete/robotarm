import threading
from time import sleep

class kthread(threading.Thread):
    def __init__(self):
        super(kthread, self).__init__()
        self._stop = threading.Event()

        self.axes_rlock = threading.Lock()

    def axes(self):
        """some docstring"""
        with self.axes_rlock():
            print "Got lock"

    def stop (self):
        self._stop.set()

    def stopped (self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            sleep(0.01)

k = kthread()
k.start()

try:
    while True:
        sleep(0.01)
except KeyboardInterrupt:
    k.stop()
    k.join()
