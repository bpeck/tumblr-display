import pygame.display


class ScreenManager(object):
    display_screen = None

    def __init__(self, display_info):    
        self.screens = []
        self.desktop_resolution = (display_info.current_w, display_info.current_h)
    
    def setScreen(self, screen):
        ScreenManager.display_screen = screen

        for screen in self.screens:
            screen.onDisplayChange(ScreenManager.display_screen)

    def onTick(self, dT):
        if ScreenManager.display_screen:
            ScreenManager.display_screen.fill((0,0,0,0))

            for screen in self.screens:
                screen.onTick(ScreenManager.display_screen, dT)

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
