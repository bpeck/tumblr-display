# py imports
import os, sys, traceback

# pygame imports
import pygame
from pygame.locals import *
from pygame.time import get_ticks

from Settings import Settings
from UI.ScreenManager import ScreenManager
from UI.MainScreen import MainScreen
from image import AsyncImageLoad

SLEEP_TIME = 8

class App(object):
    
    def __init__(self):
        self.done = False
        
        self.tick_rate = Settings.TICK_RATE
        self.last_update = get_ticks()

        pygame.display.set_caption(Settings.WINDOW_TITLE)
        sdl_screen = pygame.display.set_mode( \
            (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT), Settings.WINDOW_FLAGS)
        self.screen_manager = ScreenManager(sdl_screen)

        try:
            main_screen = MainScreen()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            self.done = True
        else:
            self.screen_manager.pushScreen(main_screen)
        finally:
            self.mainLoop()
    
    def mainLoop(self):
        try:
            while not self.done:
                for e in pygame.event.get():
                    if e.type == QUIT:
                        self.done = True
                        break
                    elif e.type == KEYDOWN and \
                        (e.key == pygame.K_ESCAPE or e.key == pygame.K_q):
                       self.done = True
                    elif e.type == KEYDOWN or e.type == KEYUP:
                        self.screen_manager.onKeyboardEvent(e)
                    elif e.type  == MOUSEMOTION or e.type  ==  MOUSEBUTTONDOWN or e.type == MOUSEBUTTONUP:
                        self.screen_manager.onMouseEvent(e)

                if not self.done:
                    t = get_ticks()
                    if self.last_update + self.tick_rate < t:
                        dT = t - self.last_update

                        AsyncImageLoad.update()
                        
                        self.screen_manager.onTick(dT)

                        self.last_update = t

                pygame.time.wait(SLEEP_TIME)
        except:
            import traceback
            traceback.print_exc()            
        
        self.tearDown()

    def tearDown(self):
        print "Tearing down " + Settings.WINDOW_TITLE + "..."
        AsyncImageLoad.stop()
