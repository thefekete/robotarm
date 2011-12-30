"""example1.py - demonstrates usage of Al5x with no servo_controller.

With servo_controller == None, the Al5x instance will simply output what it's
doing to stdout. This will continue to run through until the user hits ctrl-C.

"""
from robotarm.al5x import Al5x, AL5D
from robotarm.controllers import Ssc32

if __name__ == '__main__':
    a = Al5x(AL5D, servo_controller=None, parked_state=dict(pos=(0, 10, 2.6),
        grip=-.4), dt=0.010, avg_speed=15)
    try:
        raw_input("Press Enter to continue, ctrl-C to stop")
        c = 0
        while True:
            a.move(dict(pos=(-1, 8, 6 + (c % 5)), grip_angle=0.0))
            a.move(dict(pos=(2, 8, 5 - (c % 5)), grip_angle=0.0))
            c += 1
    except KeyboardInterrupt:
        a.park()
