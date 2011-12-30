from al5x import Al5x, AL5D
from ssc32 import Ssc32

if __name__ == '__main__':

    a = Al5x(AL5D, parked_state=dict(pos=(0,10,2.6), grip=-.4),
             dt=0.010, avg_speed=15,
             servo_controller=Ssc32('/dev/ttyUSB0'))
    try:
        c = 0
        while True:
            a.move(dict(pos=(-1,8,6+(c%5)), grip_angle=0.0))
            a.move(dict(pos=(2,8,5-(c%5)), grip_angle=0.0))
            c += 1
    except KeyboardInterrupt:
        a.park()
