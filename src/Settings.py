from collections import namedtuple
import pygame

tSettings = namedtuple('Settings',
    ['WINDOW_TITLE','WINDOW_FLAGS','WINDOW_WIDTH','WINDOW_HEIGHT','TICK_RATE','OAUTH_CONSUMER','SECRET'])

Settings = tSettings(
    WINDOW_TITLE = "TUMBLR FRAME",
    WINDOW_FLAGS = 0,#pygame.NOFRAME,
    WINDOW_WIDTH = 800,
    WINDOW_HEIGHT = 480,
    TICK_RATE = 30,
    OAUTH_CONSUMER = "YOUR OAUTH",
    SECRET = "YOUR SECRET")

