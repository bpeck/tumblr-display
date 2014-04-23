import pygame
import sys

import urllib2
from PIL import ImageFile, Image
import multiprocessing
import multiprocessing.queues

def _downloadImage(url):
    # could be encoded in jpg, gif, etc
    encoded_str = urllib2.urlopen(url).read()

    buffers = []
    w, h = 0, 0

    parser = ImageFile.Parser()
    # decompress to bitmap
    parser.feed(encoded_str)
    pil_image = parser.close()
    w, h = pil_image.size

    if pil_image.format == "GIF":

        if pil_image.mode == 'P':
            print "Palette"

        pil_image = pil_image.convert("RGB")

        if pil_image.mode == 'P':
            print "Palette still"

        scratch_path = '../_scratch/scratch.gif'
        scratch_file = open(scratch_path, 'w')
        scratch_file.write(encoded_str)
        scratch_file.close()
        scratch_image = Image.open(scratch_path)
        print "num frames: " + str(scratch_image.info['duration'])

        try:
            i = 1
            while(1):
                print "reading frame " + str(i)
                frame = Image.new('RGB', scratch_image.size)
                frame.paste(scratch_image)
                buffers.append(frame.tostring())
                scratch_image.seek(scratch_image.tell() + 1)
                i += 1
        except Exception:
            pass
    else:
        if pil_image.mode == 'RGBA':
            pil_image = pil_image.convert('RGB')
        buff = pil_image.tostring()
        buffers = [buff]

    return w, h, buffers

# This is a worker function that sits in it's own process
def _worker(in_queue, out_queue):
    done = False
    while not done:
        if not in_queue.empty():
            obj = in_queue.get()
            # if a bool is passed down the queue, set the done flag
            if isinstance(obj, bool):
                done = True
                import sys
                sys.exit()
            else:
                url = obj
                
                #try:
                w, h, buffers = _downloadImage(url)
                out_queue.put((url, w, h, buffers))
                #except:
                print "Could not download image at " + url

def start():
    downloader_process.start()

def stop():
    global worker_done
    url_queue.put(True)
    worker_done = True

def load(url, callback):
    if downloader_process.is_alive():
        on_load_callbacks[url] = callback
        #print('requesting async img load ' + url + " (" + str(w) + ", " + str(h) + ")")
        url_queue.put(url)
    else:
        assert(False)

def loadPropImage(url, prop):
    def callback(images, w, h):
        prop.image = images[0]
        prop.rect = Rect(0, 0, w, h)

    load(url, callback)

def createSurfaces(buffers, w, h, callback):
    images = []
    for buff in buffers:
        image = pygame.image.frombuffer(buff, (w, h), "RGB")
        images.append(image)
    if callback:
        callback(images, w, h)

_ticks_to_wait_in_between_loads = 4
_ticks_to_wait = 0
def update():
    if worker_done:
        return

    global _ticks_to_wait
    if _ticks_to_wait <= 0:
        if not img_buffer_queue.empty():
            url, w, h, buffers = img_buffer_queue.get()
            callback = on_load_callbacks.pop(url, None)
            createSurfaces(buffers, w, h, callback)
            _ticks_to_wait = _ticks_to_wait_in_between_loads
    else:
        _ticks_to_wait -= 1


worker_done = False
url_queue = multiprocessing.queues.SimpleQueue()
img_buffer_queue = multiprocessing.queues.SimpleQueue()

on_load_callbacks = {}

downloader_process = multiprocessing.Process(None, _worker, "async image load worker", (url_queue, img_buffer_queue))

start()
