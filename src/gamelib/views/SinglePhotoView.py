from Drawable import Drawable
from Prop import Prop
from image import AsyncImageLoad
import urllib2
import StringIO
import pygame

class SinglePhotoView(Drawable):
    def __init__(self, blogModel):
        self.rModel = blogModel

        url , w, h = self.rModel.getPosts(0, 0)[0].getPhoto()
        
        self.rProp = Prop()

        AsyncImageLoad.loadPropImage(url, self.rProp)

    def draw(self, rDisplayScreen):
        self.rProp.draw(rDisplayScreen)

    