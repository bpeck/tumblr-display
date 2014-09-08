import os
from AbstractRootModel import AbstractRootModel
import pytumblr
import PostModel
from Settings import Settings

class BlogModel(AbstractRootModel):

    def __init__(self, account):
        self.client = pytumblr.TumblrRestClient(Settings.OAUTH_CONSUMER, Settings.SECRET)
        self.account = account

        blog_info = self.client.posts(self.account)

        if blog_info.has_key('meta') and blog_info['meta']['status'] != 200:
            raise Exception("Unable to connect to Tumblr API. Did you fill in your API OAUTH/SECRET in Settings.py?")

        self.name = blog_info['blog']['title']
        self.num_posts = blog_info['total_posts']

        self.loaded = set()

        print "Created model for blog " + self.getName()

    """ Overrides AbstractRootModel """
    def getName(self):
        return self.name

    """ Overrides AbstractRootModel """
    def getRootPath(self):
        return self.account

    """ Overrides AbstractRootModel """
    def getInfo(self):
        info = {}
        info['general_desc'] = 'Displaying a Tumblr!'
        info['blog_name'] = self.name
        return info

    def getInfoTemplatePath(self):
        return os.path.join('templates','blogInfo.html')

    def getNumPosts(self):
        return self.num_posts

    def getPosts(self, start=0, end=19, types=['photo', 'video']):
        n = 0
        N = (end + 1) - start

        # print "Getting posts. Start idx %d, end idx %d" % (start, end)

        posts = []
        i = 0
        while n < N:
            grab = min(N - n, 20)
            ps = self.client.posts(self.account, limit=grab, offset= (start + i))

            for p in ps['posts']:
                if p['type'] in types:
                    if p['id'] in self.loaded:
                        # print "DUPE! " + str(p['id'])
                        continue
                    self.loaded.add(p['id'])
                    # print 'post of type ' + p['type'] + '\tid: ' + str(p['id'])
                    posts.append(PostModel.makePostModel(p))
                    n += 1
                i += 1

        post_types = {}
        for post in posts:
            if not post_types.has_key(post.post_type):
                post_types[post.post_type] = 0
            post_types[post.post_type] += 1
        print 'Retrieved %d posts from %s %s' % (len(posts), self.getName(), str(post_types))
        return posts, start + i