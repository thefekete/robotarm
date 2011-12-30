import threading

rlock = threading.RLock()

with rlock:
    print "Got Lock"
