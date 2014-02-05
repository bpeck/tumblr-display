
class ScreenManager(object):
    def __init__(self, rDisplayScreen):
        self.tScreens = []
        self.rDisplayScreen = rDisplayScreen

    def onTick(self, dT):
        for screen in self.tScreens:
            screen.onTick(self.rDisplayScreen, dT)

    def onMouseEvent(self, event):
        for screen in self.tScreens:
            if screen.onMouseEvent(event):
                break

    def onKeyboardEvent(self, event):
        for screen in self.tScreens:
            if screen.onKeyboardEvent(event):
                break

    def getScreen(self, sName):
        for screen in self.tScreens:
            if screen.getName() == sName:
                return screen

        return None

    def pushScreen(self, screen, idx=0):
        idx = max(0, min(len(self.tScreens) - 1, idx))
        self.tScreens.insert(idx, screen)

    def removeScreen(self, screenToRemove):
        self.tScreens.remove(screenToRemove)
