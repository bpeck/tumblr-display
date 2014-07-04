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
        self._kill = False
        self._skip = False

    def kill(self):
        self._kill = True

    def skip(self):
        self._skip = True

    def update(self, dT):
        if self._kill:
            return True
        if self._skip:
            self.obj[self.attr] = self.end
            return True

        value = self.ease_func(self.t, self.start, self.delta, self.total_time)
        self.obj[self.attr] = value

        if self.t >= self.total_time:
            return True

        self.t = min(self.t + dT, self.total_time)

        return False

    def onRemove(self):
        self.obj = None
        self.attr = None

from maths.Vect2 import Vect2
class Vect2AnimDriver(AnimDriver):
    def __init__(self, src_vec, dest_vec, t, ease_func):
        super(Vect2AnimDriver, self).__init__(src_vec, dest_vec, None, t, ease_func)
        self.start, self.end = Vect2(src_vec), Vect2(dest_vec)
        self.delta = self.end - self.start

    def update(self, dT):
        if self._kill:
            return True
        if self._skip:
            self.obj = self.end
            return True

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


class IterableAnimDriver(AnimDriver):
    def __init__(self, iterable, obj, attr, loop, ease_func):
        # 30 fps
        t = 1
        if len(iterable) > 1:
            t = float(len(iterable)) * (1.0 / 30.0)

        super(IterableAnimDriver, self).__init__(obj, (0, len(iterable)-1), attr, t, ease_func)
        self.iterable = iterable
        self.delta = float(len(iterable)-1)
        self.loop = loop

    def update(self, dT):
        if self._kill:
            return True
        if self._skip:
            self.obj[self.attr] = self.iterable[self.end]
            return True

        new_idx = int(self.ease_func(self.t, self.start, self.delta, self.total_time))
        # clamp index to valid values
        new_idx = max(0, min(len(self.iterable), new_idx))

        self.obj.__dict__[self.attr] = self.iterable[new_idx]

        if self.t >= self.total_time:
            if self.loop:
                self.t = 0
                return False
            else:
                return True

        self.t = min(self.t + float(dT), self.total_time)
        return False

    def onRemove(self):
        super(IterableAnimDriver, self).onRemove()
        self.iterable = None