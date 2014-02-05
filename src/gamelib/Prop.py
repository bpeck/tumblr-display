from pygame import Surface
from pygame.sprite import Sprite
from Drawable import Drawable

from maths.Vect2 import Vect2

class Prop(Sprite, Drawable):

    def __init__(self):
        self.rect = None
        self.image = None
        self.rPos = Vect2([0.0, 0.0])
        self.rParent = None
    
    def draw(self, rDisplayScreen):
        if self.image:
            p = self.getWorldPos()
            rDisplayScreen.blit(self.image, (int(p[0]), int(p[1])))
    
    def getPos(self):
        return self.rPos

    def getWorldPos(self):
        if self.rParent:
            return self.rPos + self.rParent.rPos
        else:
            return self.rPos
