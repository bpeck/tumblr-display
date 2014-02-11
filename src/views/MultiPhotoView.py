from Settings import Settings
from Drawable import Drawable
from Prop import Prop
from image import AsyncImageLoad

from maths.Vect2 import Vect2

class MultiPhotoView(Drawable):
    def __init__(self, blogModel):
        self.rModel = blogModel
        self.post = 0
        self.rProp1 = Prop()
        self.rProp2 = Prop()
        self.main_prop = self.rProp1
        self.second_prop = self.rProp2

        self.img_queue = []
        self.last_cached_post_idx = self.post
        self.initialized = False

        self.preload_images(5)

    def preload_images(self, look_ahead = 0):
        def callback(img):
            self.img_queue.append(img)
            if not self.initialized:
                print 'INIT Q'
                self.initialized = True
                self.setPost(self.post)

        posts = self.rModel.getPosts(self.last_cached_post_idx, self.last_cached_post_idx + look_ahead)
        for post in posts:
            url, w, h = post.getPhoto(0, None, Settings.WINDOW_HEIGHT)
            AsyncImageLoad.load(url, callback)

        self.last_cached_post_idx = self.last_cached_post_idx + look_ahead + 1

    def incPost(self):
        self.setPost(self.post + 1)

    def setPost(self, idx):
        h = Settings.WINDOW_HEIGHT

        self.main_prop.image = self.img_queue.pop(0)
        print len(self.img_queue)
        self.post = idx

        self.main_prop.pos = Vect2((0.0, -h))
        self.main_prop.moveTo(0, 0, 2.0)

        self.second_prop.moveTo(0, h, 2.0)

        if self.main_prop == self.rProp1:
            self.main_prop = self.rProp2
            self.second_prop = self.rProp1
        else:
            self.main_prop = self.rProp1
            self.second_prop = self.rProp2

        if len(self.img_queue) == 1:
            self.preload_images(10)

    def draw(self, rDisplayScreen):
        self.main_prop.draw(rDisplayScreen)
        self.second_prop.draw(rDisplayScreen)

    