""" main.py   
Setting up the basic functions & variables 
"""

import pygame, os, random
# include only the constants from the imported modules
from pygame.locals import *

from controllers.AppController import AppController
from App import App

from models.BlogModel import BlogModel
from views.BlogView import BlogView
from controllers.BlogCrawlController import BlogCrawlController

def main():
    try:
        import setproctitle
        setproctitle.setproctitle("pyTumblrDisplay")
    except ImportError:
        pass

    random.seed()

    #centers the pygame window in the middle of the monitor - HANDY :)
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    
    #can pre-set the mixer init arguments: pre_init(frequency=0, size=0, stereo=0, buffer=0) 
    #pygame.mixer.pre_init(44100, -16, 2, 4096)
    
    pygame.init()
    #pygame.mouse.set_visible(0)

    app = App()
    app_controller = AppController(app)

    model = BlogModel('rekall')
    view = BlogView(model)
    controller = BlogCrawlController(view)

    app_controller.setRoot(model, view, controller)
    app.app_controller = app_controller
    app.mainLoop()
    
if __name__ == '__main__':
    main()
