""" main.py   
Setting up the basic functions & variables 
"""

import pygame, os, random

#pygame.locals import * causes pygame to include only the constants from the imported modules
from pygame.locals import *

from App import App

def main():
    random.seed()

    #centers the pygame window in the middle of the monitor - HANDY :)
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    
    #can pre-set the mixer init arguments: pre_init(frequency=0, size=0, stereo=0, buffer=0) 
    #pygame.mixer.pre_init(44100, -16, 2, 4096)
    
    pygame.init()
    #pygame.mouse.set_visible(0)

    App()
    
if __name__ == '__main__':
    main()
