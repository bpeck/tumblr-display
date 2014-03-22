from collections import namedtuple

tSettings = namedtuple('Settings',
    ['WINDOW_TITLE','FULLSCREEN','WINDOW_WIDTH','WINDOW_HEIGHT','TICK_RATE','OAUTH_CONSUMER','SECRET'])

Settings = tSettings(
    WINDOW_TITLE = "TUMBLR FRAME",
    FULLSCREEN = False,
    WINDOW_WIDTH = 640,
    WINDOW_HEIGHT = 480,
    TICK_RATE = 30,
    OAUTH_CONSUMER = "0cz1o8HFTAIFOdOPn2P15LAPBQHBzUtVBF6mwvh7u50p7EmJBf",
    SECRET = "rOD0rcJWdqTP4qEbYgn5jmLO7kKOWJk9GB4vRcXZeWmErMzR7K")
