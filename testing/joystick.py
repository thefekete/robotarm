import pygame
from pygame.locals import *
from sys import exit
from time import sleep

pygame.init()

event_text = []
joystick_no = 0

stick = pygame.joystick.Joystick(joystick_no)
stick.init()

print stick.get_name()
sleep(2)

while True:

    if pygame.event.peek():
        event = pygame.event.poll()
        if event.type in (JOYAXISMOTION,
                          JOYHATMOTION,
                          JOYBUTTONUP,
                          JOYBUTTONDOWN):
            print event

help(pygame.event)
