from anim import AnimManager

class Screen(object):
    def __init__(self):
        self.sName = "Screen"
        self.tDrawables = []
        self.tControllers = []

    def getName(self):
        return self.sName

    def onTick(self, rDisplayScreen, dT):
        AnimManager.update(dT)

        for drawable in self.tDrawables:
            drawable.draw(rDisplayScreen)
        
        for controller in self.tControllers:
            controller.update(dT)

    def onMouseEvent(self, event):
        pass

    def onKeyboardEvent(self, event):
        pass

    def insertDrawable(self, drawable, idx=0):
        idx = max(0, min(len(self.tDrawables) - 1, idx))
        self.tDrawables.insert(idx, drawable)

    def removeDrawable(self, drawable):
        self.tDrawables.remove(drawable)