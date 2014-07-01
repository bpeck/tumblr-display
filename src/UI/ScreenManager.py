import pygame.display

class ScreenManager(object):
    def __init__(self, display_screen):
        self.screens = []
        self.display_screen = display_screen

    def onTick(self, dT):
        self.display_screen.fill((0,0,0,0))

        for screen in self.screens:
            screen.onTick(self.display_screen, dT)

        pygame.display.update()

    def onMouseEvent(self, event):
        for screen in self.screens:
            if screen.onMouseEvent(event):
                break

    def onKeyboardEvent(self, event):
        for screen in self.screens:
            if screen.onKeyboardEvent(event):
                break

    def getScreen(self, name):
        for screen in self.screens:
            if screen.getName() == name:
                return screen

        return None

    def pushScreen(self, screen, idx=0):
        idx = max(0, min(len(self.screens) - 1, idx))
        self.screens.insert(idx, screen)

    def removeScreen(self, screen_to_remove):
        self.screens.remove(screen_to_remove)
