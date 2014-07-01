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
        self._pos = Vect2((0.0, 0.0))
        self.parent = None
    
    def draw(self, display_screen, dT=None):
        if self.image:
            p = self.getWorldPos()
            display_screen.blit(self.image, (int(p.x), int(p.y)))
    
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    def getWorldPos(self):
        if self.parent:
            return self.pos + self.parent.getWorldPos()
        else:
            return self.pos

    def move(self, dx, dy, t, ease_func = Ease.linear):
        dest = self.pos + Vect2((dx, dy))
        return Vect2AnimDriver(self.pos, dest, t, ease_func)

    def moveTo(self, x, y, t, ease_func = Ease.linear):
        return Vect2AnimDriver(self.pos, Vect2((x, y)), t, ease_func)