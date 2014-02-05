import PostModel

class BlogModel(object):

    def __init__(self, client, account):
        self.client = client
        self.sAccount = account

        blog_info = client.posts(self.sAccount)

        self.sName = blog_info['blog']['title']
        self.nNumPosts = blog_info['total_posts']

    def getName(self):
        return self.sName

    def getNumPosts(self):
        return self.nNumPosts

    def getPosts(self, start=0, end=19):
        n = 0
        N = (end + 1) - start
        posts = []
        while n < N:
            grab = min(N - n, 20)
            ps = self.client.posts(self.sAccount, limit=grab, offset= (start + n))

            for p in ps['posts']:
                posts.append(PostModel.MakePostModel(p))

            n += len(ps)

        return posts