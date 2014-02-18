from pygame import Surface
from pygame.sprite import Sprite
from Drawable import Drawable

from anim.AnimDriver import Vect2AnimDriver

from maths import Ease
from maths.Vect2 import Vect2

class Prop(Sprite, Drawable):

    def __init__(self):
        self.rect = None
        self.image = None
        self.rPos = Vect2((0.0, 0.0))
        self.rParent = None
    
    def draw(self, rDisplayScreen):
        if self.image:
            p = self.getWorldPos()
            rDisplayScreen.blit(self.image, (int(p.x), int(p.y)))
    
    @property
    def pos(self):
        return self.rPos

    @pos.setter
    def pos(self, value):
        self.rPos = value

    def getWorldPos(self):
        if self.rParent:
            return self.rPos + self.rParent.getWorldPos()
        else:
            return self.rPos

    def move(self, dx, dy, t, ease_func = Ease.linear):
        dest = self.rPos + Vect2((dx, dy))
        Vect2AnimDriver(self.rPos, dest, t, ease_func)

    def moveTo(self, x, y, t, ease_func = Ease.linear):
        Vect2AnimDriver(self.rPos, Vect2((x, y)), t, ease_func)