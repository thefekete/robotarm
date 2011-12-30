from __future__ import with_statement # 2.5 bullshit
import threading
from datetime import datetime
from time import sleep, time

now = lambda: datetime.now().microsecond

class tsleep(threading.Thread):
    def __init__(self, interval=1.0):
        super(tsleep, self).__init__()

        self.interval = interval
        self.rlock = threading.RLock()

    def run(self):
        next_time = now() + self.interval % 1000000
        while now() < next_time:
            sleep(0)
        print "finished sleeping"

    def wait(self):
        self.start()
        self.join()
