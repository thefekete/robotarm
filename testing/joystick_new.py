import pygame
from pygame.locals import *
from time import sleep, time
from datetime import datetime

class jstick(object):
    def __init__(self, joystick_no=0):
        # Set up joystick:
        pygame.init()
        self.js_no = joystick_no
        self.stick = pygame.joystick.Joystick(joystick_no)
        self.stick.init()
        self.name = self.stick.get_name()

        self.axes = dict()

    def get_info(self):
        buttons = dict()
        types = (JOYAXISMOTION, JOYBUTTONUP, JOYBUTTONDOWN)
        events = pygame.event.get()
        for event in events:
            if event.type in types and event.joy == self.js_no:
                if event.type is JOYAXISMOTION:
                    self.axes.update({event.axis: event.value})
                elif event.type is JOYBUTTONUP:
                    pass
                elif event.type is JOYBUTTONDOWN:
                    buttons.update({event.button: True})
        return dict(self.axes), buttons

if __name__ == '__main__':

    j = jstick()

    now = lambda: datetime.now().microsecond

    try:
        next_time = 0.0
        while True:
            while now() < next_time:
                pass
            next_time = (now() + 15000) % 1000000
            a, b = j.get_info()
            for i in a: print "%i: %+0.2f    " % (i, a[i]),          
            for i in b: print "Button", i, "pressed."
            print "\r",
    except KeyboardInterrupt:
        print "Hata la vista, asshole"
