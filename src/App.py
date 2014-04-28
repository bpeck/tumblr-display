# py imports
import os, sys

# pygame imports
import pygame
from pygame.locals import *
from pygame.time import get_ticks

from Settings import Settings
from UI.ScreenManager import ScreenManager
from UI.MainScreen import MainScreen
from gifTest import gifScreen
from image import AsyncImageLoad

SLEEP_TIME = 8

class App(object):
    
    def __init__(self):
        self.done = False
        
        self.nTickRate = Settings.TICK_RATE
        self.nLastUpdate = get_ticks()

        pygame.display.set_caption(Settings.WINDOW_TITLE)
        screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT), Settings.FULLSCREEN)

        self.rScreenManager = ScreenManager(screen)

        self.rScreenManager.pushScreen(MainScreen())

        self.mainLoop()
    
    def mainLoop(self):
        try:
            while not self.done:
                for e in pygame.event.get():
                    if e.type == QUIT:
                        self.done = True
                        break
                    elif e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                       self.done = True
                    elif e.type == KEYDOWN or e.type == KEYUP:
                        self.rScreenManager.onKeyboardEvent(e)
                    elif e.type  == MOUSEMOTION or e.type  ==  MOUSEBUTTONDOWN or e.type == MOUSEBUTTONUP:
                        self.rScreenManager.onMouseEvent(e)

                if not self.done:
                    t = get_ticks()
                    if self.nLastUpdate + self.nTickRate < t:
                        dT = t - self.nLastUpdate

                        AsyncImageLoad.update()
                        
                        self.rScreenManager.onTick(dT)

                        self.nLastUpdate = t

                pygame.time.wait(SLEEP_TIME)
        except:
            import traceback
            traceback.print_exc()            
        
        self.tearDown()

    def tearDown(self):
        print "Tearing down " + Settings.WINDOW_TITLE
        AsyncImageLoad.stop()
