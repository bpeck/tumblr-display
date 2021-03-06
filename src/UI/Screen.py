from anim import AnimManager

class Screen(object):
    def __init__(self):
        self.name = "Screen"
        self.drawables = []
        self.controllers = []

    def clearDisplay(self):
        for i in range(len(self.controllers)):
            self.controllers.pop()
        for i in range(len(self.drawables)):
            self.drawables.pop()

    def onDisplayChange(self, display_screen):
        pass

    def getName(self):
        return self.name

    def onTick(self, display_screen, dT):
        AnimManager.update(dT)

        for drawable in self.drawables:
            drawable.draw(display_screen, dT)
        
        for controller in self.controllers:
            controller.update(dT)

    def onMouseEvent(self, event):
        pass

    def onKeyboardEvent(self, event):
        pass

    def insertDrawable(self, drawable, idx=0):
        idx = max(0, min(len(self.drawables) - 1, idx))
        self.drawables.insert(idx, drawable)

    def removeDrawable(self, drawable):
        self.drawables.remove(drawable)

    def addController(self, controller):
        self.controllers.append(controller)

    def removeController(self, controller):
        self.controllers.remove(controller)