import urllib2
import StringIO
import multiprocessing
import multiprocessing.queues
import pygame
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
                url = obj
                stream = urllib2.urlopen(url)
                buff = StringIO.StringIO(stream.read())
                out_queue.put((url, buff))

def start():
    downloader_process.start()

def stop():
    url_queue.put(True)

def load(url, callback):
    if downloader_process.is_alive():
        # if request same url, keep track of multiple callback funcs in case they
        # are different
        if on_load_callbacks.has_key(url):
            on_load_callbacks[url].append(callback)
        else:
            on_load_callbacks[url] = [callback]
        print('requesting async img load ' + url)
        url_queue.put(url)
    else:
        assert(False)

def loadPropImage(url, prop):
    def callback(img):
        prop.image = img

    load(url, callback)

def update():
    if not img_buffer_queue.empty():
        url, buff = img_buffer_queue.get()
        image = pygame.image.load(buff)
        callbacks = on_load_callbacks.pop(url, None)
        if callbacks:
            for callback in callbacks:
                callback(image)

url_queue = multiprocessing.queues.SimpleQueue()
img_buffer_queue = multiprocessing.queues.SimpleQueue()

on_load_callbacks = {}

downloader_process = multiprocessing.Process(None, _worker, "async image load worker", (url_queue, img_buffer_queue))

start()