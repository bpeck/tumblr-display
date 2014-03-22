from anim import AnimManager

class AnimDriver(object):
    
    def __init__(self, obj, values, attr, t, ease_func):
        self.start, self.end = values
        self.delta = self.end - self.start
        self.total_time = t * 1000.0
        self.t = 0.0
        self.obj = obj
        self.attr = attr
        self.ease_func = ease_func
        self.done = False

    def update(self, dT):
        value = self.ease_func(self.t, self.start, self.delta, self.total_time)
        self.obj[self.attr] = value

        if self.t >= self.total_time:
            return True

        self.t = min(self.t + dT, self.total_time)

        return False

from maths.Vect2 import Vect2
class Vect2AnimDriver(AnimDriver):
    def __init__(self, src_vec, dest_vec, t, ease_func):
        super(Vect2AnimDriver, self).__init__(src_vec, dest_vec, None, t, ease_func)
        self.start, self.end = Vect2(src_vec), Vect2(dest_vec)
        self.delta = self.end - self.start

    def update(self, dT):
        new_x = self.ease_func(self.t, self.start.x, self.delta.x, self.total_time)
        new_y = self.ease_func(self.t, self.start.y, self.delta.y, self.total_time)

        #if self.start.y < 0:
        #    print str(new_x) + ', ' + str(new_y)

        self.obj.x = new_x
        self.obj.y = new_y

        if self.t >= self.total_time:
            return True

        self.t = min(self.t + float(dT), self.total_time)

        return False