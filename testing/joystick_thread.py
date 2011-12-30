from __future__ import with_statement # 2.5 bullshit
import pygame, threading
from pygame.locals import *
from time import sleep, time
from datetime import datetime


class jstick(threading.Thread):
    """Threaded class to monitor a joystick for activity"""

    def __init__(self, joystick_no=0):
        super(jstick, self).__init__()
        self._stop = threading.Event()

        self.__axes = dict()
        self.axes_rlock = threading.RLock()
        self.__buttons = dict()
        self.buttons_rlock = threading.RLock()

        # Set up joystick:
        pygame.init()
        self.js_no = joystick_no
        self.stick = pygame.joystick.Joystick(joystick_no)
        self.stick.init()
        self.name = self.stick.get_name()
        
    def stop(self):
        """Requests thread to exit gracefully, follow this with a join()"""
        self._stop.set()

    def stopped(self):
        """Returns whether or not stop() has been called"""
        return self._stop.isSet()

    def axes(self):
        """Get last known axis info as a dictionary"""
        with self.axes_rlock:
            axes = dict(self.__axes)
        return axes

    def buttons(self):
        """Get dictionary of buttons pressed since last call"""
        with self.buttons_rlock:
            buttons = dict(self.__buttons)
            self.__buttons.clear()
        return buttons

    def __set_axes(self, data):
        """Private method using locks to safely update axes dictionary"""
        with self.axes_rlock:
            self.__axes.update(data)

    def __set_buttons(self, data):
        """Private method using locks to safely update buttons dictionary"""
        with self.buttons_rlock:
            self.__buttons.update(data)

    def run(self):
        next_time = 0
        while True:
            sleep(0.001) # yield to other processes
            if self.stopped():
                break
            types = (JOYAXISMOTION, JOYBUTTONUP, JOYBUTTONDOWN)
            if time() > next_time and pygame.event.peek(types):
                next_time = time() + 0.02
                events = pygame.event.get()
                for event in events:
                    if event.type in types and event.joy==self.js_no:
                        if event.type is JOYAXISMOTION:
                            self.__set_axes({event.axis: event.value})
                        elif event.type is JOYBUTTONUP:
                            pass
                        elif event.type is JOYBUTTONDOWN:
                            self.__set_buttons({event.button: True})
        pygame.quit()



if __name__ == '__main__':

    j = jstick()
    j.start()

    try:
        while True:
            a = j.axes()
            b = j.buttons()  
            for i in a: print "%i: %+0.2f    " % (i, a[i]),          
            for i in b: print "Button", i, "pressed."
            print "\r",
            sleep(0.010) # yield to other processes
    except KeyboardInterrupt:
        j.stop()
        print
        print "Waiting for thread to stop...",
        j.join()
        print "Done."
        print "Hasta la vista, asshole"
