import urllib2
import StringIO
from PIL import ImageFile
import multiprocessing
import multiprocessing.queues
import pygame
from pygame import Rect
import sys

def _worker(in_queue, out_queue):
    sys.stdout.flush()
    done = False
    while not done:
        if in_queue.empty():
            pass
        else:
            obj = in_queue.get()
            # if a bool is passed down the queue, set the done flag
            if isinstance(obj, bool):
                done = obj
            else:
                url, w, h = obj
                print "opening stream at " + url
                jpg_encoded_str = urllib2.urlopen(url).read()
                parser = ImageFile.Parser()
                parser.feed(jpg_encoded_str)
                pil_image = parser.close() 
                buff = pil_image.tostring()
                print "placing in output queue"
                out_queue.put((url, w, h, buff))

def start():
    downloader_process.start()

def stop():
    url_queue.put(True)

def load(url, w, h, callback):
    if downloader_process.is_alive():
        on_load_callbacks[url] = callback
        print('requesting async img load ' + url + " (" + str(w) + ", " + str(h) + ")")
        url_queue.put((url, w, h))
    else:
        assert(False)

def loadPropImage(url, w, h, prop):
    def callback(img, w, h):
        prop.image = img
        prop.rect = Rect(0, 0, w, h)

    load(url, w, h, callback)

def update():
    if not img_buffer_queue.empty():
        url, w, h, buff = img_buffer_queue.get()
        print "found output data " + url + ", " + str(w) + ", " + str(h)
        print len(buff)
        image = pygame.image.frombuffer(buff, (w, h), "RGB")
        print "loaded bugger into memory"
        #image.convert()
        callback = on_load_callbacks.pop(url, None)
        if callback:
            print "callback calling!"
            callback(image, w, h)

url_queue = multiprocessing.queues.SimpleQueue()
img_buffer_queue = multiprocessing.queues.SimpleQueue()

on_load_callbacks = {}

downloader_process = multiprocessing.Process(None, _worker, "async image load worker", (url_queue, img_buffer_queue))

start()