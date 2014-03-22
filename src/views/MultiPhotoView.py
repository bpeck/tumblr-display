from Drawable import Drawable
from Prop import Prop
from image import AsyncImageLoad
from anim import AnimManager
from pygame import Rect
from pygame import transform

from maths.Vect2 import Vect2

class MultiPhotoView(Drawable):
    SCROLL_SPEED = 1.0
    DISPLAY_SPEED = 3.0

    class PhotoProp(Prop):
        STATE_SCROLL_IN, STATE_DISPLAY, STATE_SCROLL_OUT, NUM_STATES = range(4)
        def __init__(self, image, w, h):
            super(PhotoProp, self).__init__()

            prop_aspect = w / h
            screen_aspect = MultiPhotoView.rect.w / MultiPhotoView.rect.h
            if prop_aspect < screen_aspect:
                w, h = MultiPhotoView.rect.h * prop_aspect, MultiPhotoView.rect.h
            else:
                w, h = MultiPhotoView.rect.w, MultiPhotoView.rect.w / prop_aspect
            self.image = transform.smoothscale(image, (w, h))
            self.rect = Rect(0, 0, w, h)

            self.display_time = 0
            self.done = False
            self.rPos = Vect2((0, -w))

        def show(self, scroll_speed, display_speed):
            self.scroll_speed = scroll_speed

            self.state = PhotoProp.STATE_SCROLL_IN        
            self.current_action = self.moveTo(0, (MultiPhotoView.rect.h - self.rect.h) * 0.5, self.scroll_speed)
            AnimManager.addDriver(self.current_action)

        def hide(self):
            self.state = PhotoProp.STATE_SCROLL_OUT
            self.current_action = self.moveTo(0, MultiPhotoView.rect.h, self.scroll_speed)
            AnimManager.addDriver(self.current_action)

        def update(self, dT):
            if self.state == PhotoProp.STATE_SCROLL_IN:
                if self.current_action.done:
                    self.state = PhotoProp.STATE_DISPLAY
            elif self.state == PhotoProp.STATE_SCROLL_OUT:
                if self.current_action.done:
                    self.done = True

    def __init__(self, blogModel, viewableArea):
        MultiPhotoView.rect = Rect(0, 0, viewableArea[0], viewableArea[1])
        self.rModel = blogModel
        self.post = 0

        self.img_queue = []
        self.last_cached_post_idx = self.post
        self.initialized = False

        print "preloading photos"

        self.photoProps = []
        self.preload_images(5)

    def preload_images(self, look_ahead = 0):
        def callback(img, w, h):
            self.img_queue.append((img, w, h))
            if not self.initialized:
                self.initialized = True
                self.setPost(self.post)

        start, end = self.last_cached_post_idx, self.last_cached_post_idx + look_ahead
        print "start, end " + str(start) + ", " + str(end)
        posts = self.rModel.getPosts(self.last_cached_post_idx, self.last_cached_post_idx + look_ahead)
        print "requested " + str(len(posts)) + " posts"
        for post in posts:
            url, w, h = post.getPhoto(0, None, self.rect.h)
            AsyncImageLoad.load(url, w, h, callback)

        self.last_cached_post_idx += look_ahead + 1

    def incPost(self):
        self.setPost(self.post + 1)

    def setPost(self, idx):
        for prop in self.photoProps:
            prop.hide()

        image, w, h = self.img_queue.pop(0)
        
        self.post = idx

        photoProp = MultiPhotoView.PhotoProp(image, w, h)
        photoProp.show(MultiPhotoView.SCROLL_SPEED, MultiPhotoView.DISPLAY_SPEED)
        self.photoProps.append(photoProp)

        if len(self.img_queue) < 5:
            self.preload_images(5)

    def draw(self, rDisplayScreen, dT):
        not_done = []
        for prop in self.photoProps:
            prop.update(dT)
            if not prop.done:
                prop.draw(rDisplayScreen)
                not_done.append(prop)

        self.photoProps = not_done

    