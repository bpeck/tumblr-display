from Drawable import Drawable
from Prop import Prop
from image import AsyncImageLoad

class MultiPhotoView(Drawable):
    def __init__(self, blogModel):
        self.rModel = blogModel
        self.post = 0
        self.rProp = Prop()

        self.setPost(self.post)

    def incPost(self):
        self.setPost(self.post + 1)

    def setPost(self, idx):
        url, w, h = self.rModel.getPosts(idx, idx)[0].getPhoto()
        AsyncImageLoad.loadPropImage(url, self.rProp)
        self.post = idx

    def draw(self, rDisplayScreen):
        self.rProp.draw(rDisplayScreen)

    