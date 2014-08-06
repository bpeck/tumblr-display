from pygame import Rect

from Drawable import Drawable
from views.ImageProp import ImageProp
from UI.ScreenManager import ScreenManager

class ImageView(Drawable):
    def __init__(self):
        self.rect = ScreenManager.display_screen.get_rect()
        self.image_props = []

    def setImage(self, image_prop, scroll_speed=None, display_speed=None):
        image_prop.state_listeners.append(self.onImagePropStateChange)

        for prop in self.image_props:
            prop.hide()

        image_prop.show(scroll_speed, display_speed)
        self.image_props.append(image_prop)

    def onImagePropStateChange(self, image_prop, state):
        if state == MultiPhotoView.PhotoProp.STATE_DEAD:    
            image_prop.onRemove()
            self.image_props.remove(image_prop)

    def draw(self, display_screen, dT):
        for prop in self.image_props:
            prop.update(dT)
        for prop in self.image_props:
            prop.draw(display_screen)
    