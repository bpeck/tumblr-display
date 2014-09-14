from pygame import Rect

from views.ImageView import ImageView
from views.ImageProp import ImageProp
from image import AsyncImageLoad

class BlogView(ImageView):
    SCROLL_SPEED = 1.0
    DISPLAY_SPEED = 4.0
    REWIND_LEN = 5

    def __init__(self, blogModel):
        super(BlogView, self).__init__()

        self.model = blogModel
        self.post = 0

        self.initialized = False
        # we  will hold on to ref of a photo prop that has just been
        # created, and once it reaches display state we trigger a preload
        self.preload_batch_progress = {}
        self.preload_batch_id = 0
        self.preload_after_prop_displays = None
        self.waiting_on_batch = None

        self.img_queue = []
        self.current_img_queue_idx = 0
        self.last_cached_post_idx = self.post

        self.preload_posts(2)

    """ Overrides AbstractRootView """
    def getInfo(self):
        info = {} 
        if self.waiting_on_batch:
            info['status'] = "Fetching additional posts..."
            info['status_desc'] = "There are %d photos left to in this prefetch batch." % self.preload_batch_progress[self.waiting_on_batch]
        else:
            info['status'] = "Displaying post."
            info['status_desc'] = ""
        info['queue_size'] = str(len(self.img_queue))
        info['post_num'] =  self.post
        return info

    def isReady(self):
        return self.waiting_on_batch == None

    def preload_posts(self, look_ahead = 0):
        self.preload_batch_id = (self.preload_batch_id + 1) % 99999
        if not self.waiting_on_batch:
            self.waiting_on_batch = self.preload_batch_id

        def callback(batch_id, images, w, h):
            if len(images) > 0:
                self.img_queue.append((images, w, h))
                if not self.initialized:
                    self.initialized = True
                    self.setPost(self.post)

            self.preload_batch_progress[batch_id] -= 1

            print "BATCH %d PROGRESS: %d REMAIN" % (batch_id, self.preload_batch_progress[batch_id])

            if self.preload_batch_progress[batch_id] <= 0:
                print "FINISHED LOADING BATCH %d" % batch_id
                if self.waiting_on_batch == batch_id:
                    print "...WAS WAITING ON THIS BATCH"
                    self.waiting_on_batch = None

                del self.preload_batch_progress[batch_id]

        start, end = self.last_cached_post_idx, self.last_cached_post_idx + look_ahead
        posts, self.last_cached_post_idx = self.model.getPosts(self.last_cached_post_idx, self.last_cached_post_idx + look_ahead)
        #print "requested " + str(len(posts)) + " posts"

        # load each image in the batch. On the last image of the batch,
        # set the view's ready flag to true
        num_photos_to_load = sum(map(lambda x: x.getNumPhotos(), posts))
        self.preload_batch_progress[self.preload_batch_id] = num_photos_to_load
        for i in range(len(posts)):
            for url in posts[i].getPhotos(None, self.rect.h):
                AsyncImageLoad.load(url, callback, self.preload_batch_id)

        self.last_cached_post_idx += look_ahead + 1

    def preload_needed(self):
        return not self.preload_after_prop_displays and len(self.img_queue) - self.current_img_queue_idx < 5

    def incPost(self):
        return self.setPost(self.post + 1)

    def prevPost(self):
        return self.setPost(self.post - 1)

    def setPost(self, idx):
        if len(self.img_queue) > 0:
            if idx > self.post:
                if self.current_img_queue_idx >= BlogView.REWIND_LEN:
                    self.img_queue.pop(0)
                self.current_img_queue_idx = min(idx, len(self.img_queue)-1, self.current_img_queue_idx + 1, BlogView.REWIND_LEN)
            else:
                self.current_img_queue_idx = max(self.current_img_queue_idx - 1, 0)

            try:
                images, w, h = self.img_queue[self.current_img_queue_idx]
                image_prop = ImageProp(images, w, h, self.rect.w, self.rect.h)
                self.setImage(image_prop, BlogView.SCROLL_SPEED, BlogView.DISPLAY_SPEED)

                self.post = idx
                if self.preload_needed():
                    self.preload_after_prop_displays = image_prop
                return True
            except IndexError:
                print "Bad index! %d" % self.current_img_queue_idx
                return False
        return False

    def onImagePropStateChange(self, image_prop, state):
        if image_prop == self.preload_after_prop_displays and state == ImageProp.STATE_DISPLAY:
            self.preload_posts(5)
            self.preload_after_prop_displays = None
        elif state == ImageProp.STATE_DEAD:    
            image_prop.onRemove()
            self.image_props.remove(image_prop)
    