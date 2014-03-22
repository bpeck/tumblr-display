import pygame
import sys

import urllib2
from PIL import ImageFile
import multiprocessing
import multiprocessing.queues

# This is a worker function that sits in it's own process
def _worker(in_queue, out_queue):
    done = False
    while not done:
        if not in_queue.empty():
            obj = in_queue.get()
            # if a bool is passed down the queue, set the done flag
            if isinstance(obj, bool):
                done = obj
            else:
                url, w, h = obj
                
                jpg_encoded_str = urllib2.urlopen(url).read()
                parser = ImageFile.Parser()
                parser.feed(jpg_encoded_str)
                pil_image = parser.close() 
                buff = pil_image.tostring()
                
                out_queue.put((url, w, h, buff))

def start():
    downloader_process.start()

def stop():
    url_queue.put(True)

def load(url, w, h, callback):
    if downloader_process.is_alive():
        on_load_callbacks[url] = callback
        #print('requesting async img load ' + url + " (" + str(w) + ", " + str(h) + ")")
        url_queue.put((url, w, h))
    else:
        assert(False)

def loadPropImage(url, w, h, prop):
    def callback(img, w, h):
        prop.image = img
        prop.rect = Rect(0, 0, w, h)

    load(url, w, h, callback)

def createSurface(buff, w, h, callback):
    image = pygame.image.frombuffer(buff, (w, h), "RGB")
    if callback:
        callback(image, w, h)

_ticks_to_wait_in_between_loads = 4
_ticks_to_wait = 0
def update():
    global _ticks_to_wait
    if _ticks_to_wait <= 0:
        if not img_buffer_queue.empty():
            url, w, h, buff = img_buffer_queue.get()
            callback = on_load_callbacks.pop(url, None)
            createSurface(buff, w, h, callback)
            _ticks_to_wait = _ticks_to_wait_in_between_loads
    else:
        _ticks_to_wait -= 1


url_queue = multiprocessing.queues.SimpleQueue()
img_buffer_queue = multiprocessing.queues.SimpleQueue()

on_load_callbacks = {}

downloader_process = multiprocessing.Process(None, _worker, "async image load worker", (url_queue, img_buffer_queue))

start()