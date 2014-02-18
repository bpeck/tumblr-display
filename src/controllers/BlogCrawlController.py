class BlogCrawlController(object):
    
    def __init__(self, view):
        self.view = view
        self.period = 2000
        self.t = self.period

    def update(self, dT):
        self.t = self.t - dT
        if self.t <= 0:
            if self.view.initialized:
                self.view.incPost()
            self.t = self.period