from Drawable import Drawable
from Prop import Prop
from image import AsyncImageLoad
from anim import AnimManager
from anim.AnimDriver import IterableAnimDriver
from pygame import Rect
from pygame import transform
from pygame import draw as Draw
from pygame import Color

from maths.Vect2 import Vect2
from maths import Ease

class MultiPhotoView(Drawable):
    SCROLL_SPEED = 1.0
    DISPLAY_SPEED = 3.0

    # a rectangular sprite that displays a photo on screen for a certain amount of time
    class PhotoProp(Prop):
        STATE_SCROLL_IN, STATE_DISPLAY, STATE_SCROLL_OUT, NUM_STATES = range(4)
        def __init__(self, images, w, h, state_listener):
            super(MultiPhotoView.PhotoProp, self).__init__()

            self.state_listeners = []
            if state_listener:
                self.state_listeners.append(state_listener)

                scale = min( float(MultiPhotoView.rect.w) / float(w), float(MultiPhotoView.rect.h) / float(h))
                new_w = int(float(w) * scale)
                new_h = int(float(h) * scale)

                self.frames = []
                for frame in images:
                    self.frames.append(transform.smoothscale(frame, (new_w, new_h)))

                self.rect = Rect(0, 0, new_w, new_h)
                self.rPos = Vect2((0, -new_w))
            else:
                self.frames = images
                self.rect = Rect(0, 0, w, h)
                self.rPos = Vect2((0, -w))

            self.display_time = 0
            self.done = False

            self._state = None

        @property
        def state(self):
            return self._state

        @state.setter
        def state(self, new_state):
            self._state = new_state
            for listener in self.state_listeners:
                listener.onPhotoPropStateChange(self, new_state)

        def draw(self, rDisplayScreen, dT=None):
            super(MultiPhotoView.PhotoProp, self).draw(rDisplayScreen, dT)
            if self.rect:
                dbg_rect = Rect(self.rPos[0], self.rPos[1], self.rect.w, self.rect.h)
                Draw.rect(rDisplayScreen, Color("red"), dbg_rect, 1)


        def show(self, scroll_speed, display_speed):
            self.scroll_speed = scroll_speed

            self.state = MultiPhotoView.PhotoProp.STATE_SCROLL_IN

            x = (MultiPhotoView.rect.w - self.rect.w) * 0.5
            y = (MultiPhotoView.rect.h - self.rect.h) * 0.5
            self.rPos.x = x
            self.current_move_action = self.moveTo(x, y, self.scroll_speed, Ease.outBounce)
            AnimManager.addDriver(self.current_move_action)

            self.current_anim_action = IterableAnimDriver(self.frames, self, 'image', True, Ease.linear)
            AnimManager.addDriver(self.current_anim_action)

        def hide(self):
            self.state = MultiPhotoView.PhotoProp.STATE_SCROLL_OUT
            self.current_move_action = self.moveTo(self.rPos.x, MultiPhotoView.rect.h, self.scroll_speed, Ease.outExpo)
            AnimManager.addDriver(self.current_move_action)

        def update(self, dT):
            if self.state == MultiPhotoView.PhotoProp.STATE_SCROLL_IN:
                if self.current_move_action.done:
                    self.state = MultiPhotoView.PhotoProp.STATE_DISPLAY
            elif self.state == MultiPhotoView.PhotoProp.STATE_SCROLL_OUT:
                if self.current_move_action.done:
                    self.done = True
                    self.current_anim_action.kill()

    def __init__(self, blogModel, viewableArea):
        MultiPhotoView.rect = Rect(0, 0, viewableArea[0], viewableArea[1])
        self.rModel = blogModel
        self.post = 0
        # while the view isn't ready, the controller will not
        # ask it to increment posts. So during an image load
        # we will hold on the current post until the batch is done 
        # processing in
        self.ready = False
        self.initialized = False
        # we  will hold on to ref of a photo prop that has just been
        # created, and once it reaches display state we trigger a preload
        self.preload_after_prop_displays = None

        self.img_queue = []
        self.last_cached_post_idx = self.post

        self.photoProps = []
        self.preload_images(5)

    def isReady(self):
        return self.ready

    def preload_images(self, look_ahead = 0):
        self.ready = False
        def callback(images, w, h):
            self.img_queue.append((images, w, h))
            if not self.initialized:
                self.initialized = True
                self.setPost(self.post)
        def lastInBatchCallback(images, w, h):
            callback(images, w, h)
            self.ready = True

        start, end = self.last_cached_post_idx, self.last_cached_post_idx + look_ahead
        print "start, end " + str(start) + ", " + str(end)
        posts, self.last_cached_post_idx = self.rModel.getPosts(self.last_cached_post_idx, self.last_cached_post_idx + look_ahead)
        #print "requested " + str(len(posts)) + " posts"

        # load each image in the batch. On the last image of the batch,
        # set the view's ready flag to true
        num_photos = sum(map(lambda x: x.getNumPhotos(), posts))
        photo_num = 0
        for i in range(len(posts)):
            for url in posts[i].getPhotos(None, self.rect.h):
                fCallback = callback
                if photo_num == num_photos - 1:
                    fCallback = lastInBatchCallback
                AsyncImageLoad.load(url, fCallback)
                photo_num += 1


        self.last_cached_post_idx += look_ahead + 1

    def preload_needed(self):
        return not self.preload_after_prop_displays and len(self.img_queue) < 5

    def incPost(self):
        self.setPost(self.post + 1)

    def setPost(self, idx):
        for prop in self.photoProps:
            prop.hide()

        images, w, h = self.img_queue.pop(0)
        
        self.post = idx

        photoProp = MultiPhotoView.PhotoProp(images, w, h, self)
        if self.preload_needed():
            self.preload_after_prop_displays = photoProp

        photoProp.show(MultiPhotoView.SCROLL_SPEED, MultiPhotoView.DISPLAY_SPEED)
        self.photoProps.append(photoProp)

    def onPhotoPropStateChange(self, photo_prop, state):
        if photo_prop == self.preload_after_prop_displays and state == MultiPhotoView.PhotoProp.STATE_DISPLAY:
            self.preload_images(5)
            self.preload_after_prop_displays = None

    def draw(self, rDisplayScreen, dT):
        not_done = []
        for prop in self.photoProps:
            prop.update(dT)
            if not prop.done:
                prop.draw(rDisplayScreen)
                not_done.append(prop)

        self.photoProps = not_done

    