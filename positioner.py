from jstick import *
from al5x import *
from ssc32 import *
import time

class jspos(al5x):
    def __init__(self, beams, servo_controller=nullServo(True),
                 parked_state=None, servo_map=None, avg_speed=15.0,
                 dt=0.007):
        al5x.__init__(self, beams, servo_controller, parked_state,
                      servo_map, avg_speed, dt)
        self.axes = dict()
        self.last_time = time.time()
        self.pos_speed = 4.0
        self.angle_speed = 25

    def update(self, axes, buttons, state):
        dt = time.time() - self.last_time
        self.last_time = time.time()
        #print "dt:", dt, "\t",
        self.axes = dict(axes)

        xyz = [ self.axes[i] for i in range(3) ]
        grip = self.axes[3]
        state['pos'] = tuple(map(
            lambda x,y: x + y*self.pos_speed*dt,
            state['pos'], xyz))
        state['grip_angle'] += self.axes[5]*self.angle_speed*dt
        state['grip'] = grip
        state['wrist_rotate'] += self.axes[4]*self.angle_speed*dt

        if 2 in buttons:
            state['grip_angle'] = 0.0
        if 3 in buttons:
            state['wrist_rotate'] = 0.0
        if 6 in buttons:
            print "Code for park_it here..."
        if 0 in buttons:
            print state

        #print state, "\r",
        return state

if __name__ == '__main__':

    j = jstick()
    arm = al5x(AL5D, parked_state=dict(pos=(0.0, 8.0, -1.0)),
               servo_controller=ssc32('/dev/ttyUSB0'))
    jp = jspos()

    try:
        #next_time = 0.0
        last_time = time.time()
        interval = 0.008
        while True:
            dt = time.time() - last_time
            if dt > interval:
                a, b = j.get_info()
                if 11 in b:
                    raise KeyboardInterrupt
                state = jp.update(a, b, arm.get_state())
                arm.immediate_move(state)
                last_time = time.time()
            sleep(0.000001)
    except:
        arm.park()
        print "Hasta la vista, asshole"
