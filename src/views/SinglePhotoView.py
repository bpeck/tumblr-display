from Drawable import Drawable
from Prop import Prop
from image import AsyncImageLoad
import urllib2
import StringIO
import pygame

class SinglePhotoView(Drawable):
    def __init__(self, blogModel):
        self.model = blogModel

        url , w, h = self.model.getPosts(0, 0)[0].getPhoto()
        
        self.prop = Prop()

        AsyncImageLoad.loadPropImage(url, self.prop)

    def draw(self, display_screen):
        self.prop.draw(display_screen)

    