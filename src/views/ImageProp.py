from pygame import transform
from pygame import draw as pygame_draw
from pygame import Rect

from Prop import Prop
from anim import AnimManager
from anim.AnimDriver import IterableAnimDriver
from maths.Vect2 import Vect2
from maths import Ease

# a rectangular sprite that displays a photo on screen for a certain amount of time
class ImageProp(Prop):
    STATE_SCROLL_IN, STATE_DISPLAY, STATE_SCROLL_OUT, STATE_DEAD, NUM_STATES = range(5)
    def __init__(self, images, w, h, parent_view_w=None, parent_view_h=None):
        super(ImageProp, self).__init__()
        self.desired_w = parent_view_w
        self.desired_h = parent_view_h
        self.state_listeners = []
        if self.desired_w and self.desired_h:
            scale = min( float(self.desired_w) / float(w), float(self.desired_h) / float(h))
            new_w = int(float(w) * scale)
            new_h = int(float(h) * scale)

            self.frames = []
            for frame in images:
                self.frames.append(transform.smoothscale(frame, (new_w, new_h)))

            self.rect = Rect(0, 0, new_w, new_h)
            self.pos = Vect2((0, -new_h))
        else:
            self.frames = images
            self.rect = Rect(0, 0, w, h)
            self.pos = Vect2((0, -w))

        self._state = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state
        for callback in self.state_listeners:
            callback(self, new_state)

    # debug draw func
    # def draw(self, display_screen, dT=None):
    #     super(ImageProp, self).draw(display_screen, dT)
    #     if self.rect:
    #         dbg_rect = Rect(self.pos[0], self.pos[1], self.rect.w, self.rect.h)
    #         pygame_draw.rect(display_screen, Color("red"), dbg_rect, 1)


    def show(self, scroll_speed=1.0, display_speed=-1.0):
        self.scroll_speed = scroll_speed

        self.state = ImageProp.STATE_SCROLL_IN

        x = (self.desired_w - self.rect.w) * 0.5
        y = (self.desired_h - self.rect.h) * 0.5
        self.pos.x = x
        self.current_move_action = self.moveTo(x, y, self.scroll_speed, Ease.inOutCubic)
        AnimManager.addDriver(self.current_move_action)

        self.current_anim_action = IterableAnimDriver(self.frames, self, 'image', True, Ease.linear)
        AnimManager.addDriver(self.current_anim_action)

    def hide(self):
        self.state = ImageProp.STATE_SCROLL_OUT
        self.current_move_action = self.moveTo(self.pos.x, self.desired_h, self.scroll_speed, Ease.inOutCubic)
        AnimManager.addDriver(self.current_move_action)

    def update(self, dT):
        if self.state == ImageProp.STATE_SCROLL_IN:
            if self.current_move_action.done:
                self.state = ImageProp.STATE_DISPLAY
        elif self.state == ImageProp.STATE_SCROLL_OUT:
            if self.current_move_action.done:
                self.current_anim_action.kill()
            if self.current_anim_action.done:
                self.state = ImageProp.STATE_DEAD

    def onRemove(self):
        self.image = None
        self.frames = []
        self.state_listeners = []
        self.current_move_action = None
        self.current_anim_action = None