"""example3.py - complex usage of Al5x with SSC-32 connected on /dev/ttyUSB0.

This will continue to run through until the user hits ctrl-C.

"""
from robotarm.al5x import Al5x, AL5D
from robotarm.controllers import Ssc32

s = Ssc32('/dev/ttyUSB0')
s.trim(2, 0.025)
s.trim(3, -0.025)

r = Al5x(AL5D, servo_controller=s)
r.max_speed = 30
r.acceleration = 75
r.update_interval = 0.005

r.parked_state = dict(pos=[0, 8, 3], gripper_angle=0.0,
                grip=0.0, wrist_rotate=0.0)

states = [
    dict(pos=[3, 8, 1], gripper_angle=0,
                wrist_rotate=-80),
    dict(pos=[3, 8, 1], gripper_angle=0,
                grip=0.28, wrist_rotate=-80),
    {'pause': .5},
    dict(pos=[3, 8, 6], gripper_angle=0,
                wrist_rotate=-80),
    dict(pos=[-3, 8, 6], gripper_angle=0,
                wrist_rotate=80),
    dict(pos=[-3, 8, 3], gripper_angle=0,
                wrist_rotate=80),
    dict(pos=[-3, 8, 3], gripper_angle=0,
                grip=0.0, wrist_rotate=80),
    {'pause': .5},
    dict(pos=[-3, 8, 6], gripper_angle=0,
                wrist_rotate=80),
    dict(pos=[3, 8, 6], gripper_angle=0.0,
                wrist_rotate=-80)]

try:
    r.park()
    while True:
        raw_input("Press Enter to continue")
        for i in states:
            if 'pause' in i:
                sleep(i['pause'])
            else:
                r.move(i)

except KeyboardInterrupt:
    r.park()
