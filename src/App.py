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
from web import Backend

SLEEP_TIME = 8

class App(object):
    
    def __init__(self):
        print "Icons made by Icomoon, Freepik is licensed by CC BY 3.0"

        self.done = False
        self.fullscreen = None
        
        self.tick_rate = Settings.TICK_RATE
        self.last_update = get_ticks()

        pygame.display.set_caption(Settings.WINDOW_TITLE)
        
        self.screen_manager = ScreenManager(pygame.display.Info())

        self.setFullscreen(False)

    def setFullscreen(self, fullscreen):
        if fullscreen == self.fullscreen:
            return
        sdl_screen = None
        if fullscreen:
            sdl_screen = pygame.display.set_mode( \
                self.screen_manager.desktop_resolution, pygame.FULLSCREEN)
        else:
            sdl_screen = pygame.display.set_mode( \
                (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT), Settings.WINDOW_FLAGS)

        pygame.mouse.set_visible(not fullscreen)
        self.fullscreen = fullscreen

        self.screen_manager.setSDLScreen(sdl_screen) 

        Backend.start()
    
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
                    elif e.type == KEYDOWN and \
                        e.key == pygame.K_f:
                        self.setFullscreen(not self.fullscreen)
                    elif e.type == KEYDOWN or e.type == KEYUP:
                        self.app_controller.handleKeyboardEvent(e)
                    elif e.type  == MOUSEMOTION or e.type  ==  MOUSEBUTTONDOWN or e.type == MOUSEBUTTONUP:
                        self.app_controller.handleMouseEvent(e)

                if not self.done:
                    t = get_ticks()
                    if self.last_update + self.tick_rate < t:
                        dT = t - self.last_update

                        AsyncImageLoad.update()

                        backend_cmd = Backend.poll()
                        if backend_cmd:
                            print 'recv command from web'
                            self.app_controller.handleCommand(backend_cmd)
                        
                        self.screen_manager.onTick(dT)

                        self.last_update = t

                pygame.time.wait(SLEEP_TIME)
        except:
            import traceback
            traceback.print_exc()
            self.done = True
        finally:
            self.tearDown()

    def tearDown(self):
        print "Tearing down " + Settings.WINDOW_TITLE + "..."
        Backend.stop()
        AsyncImageLoad.stop()
