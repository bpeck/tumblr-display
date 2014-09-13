from AbstractRootController import AbstractRootController
from controllers.RootModelCommands import NextCommand, PrevCommand, PauseCommand
from pygame.locals import *

class BlogCrawlController(AbstractRootController):
    
    def __init__(self, view):
        self.view = view
        self.period = (view.SCROLL_SPEED * 1000) + (view.DISPLAY_SPEED * 1000)
        self.t = self.period
        self._paused = False

    def update(self, dT):
        # the view is usually not ready while it is waiting for
        # images to finish loading in
        if self.view.isReady() and not self._paused:
            self.t -= dT

            if self.t <= 0:
                self.view.incPost()
                self.t = self.period

    @property
    def paused(self):
        return self._paused

    @paused.setter
    def paused(self, state):
        self._paused = state
        self.t = max(self.t, 0)

    """ Overrides AbstractRootController """
    def handleKeyboardEvent(self, e):
        if e.type == KEYUP:
            if e.key == K_LEFT:
                self.handleCommand(PrevCommand())
            elif e.key == K_RIGHT:
                self.handleCommand(NextCommand())
            elif e.key == K_SPACE:
                self.handleCommand(PauseCommand())

    """ Overrides AbstractRootController """
    def handleMouseEvent(self, e):
        pass

    """ Overrides AbstractRootController """
    def handleCommand(self, command):
        if isinstance(command, NextCommand):
            self.t = 0
        elif isinstance(command, PrevCommand):
            self.view.prevPost()
            self.t = self.period
        elif isinstance(command, PauseCommand):
            self.paused = not self.paused
    
    """ Overrides AbstractRootController """
    def getInfo(self):
        info = {}
        p = float(self.period) / 1000.0
        info['how'] = "Incrementing every %.1f sec." % p
        return info