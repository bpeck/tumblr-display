import pygame
import os

import urllib2
from PIL import ImageFile, Image, ImageSequence
import multiprocessing
import multiprocessing.queues
import subprocess

def _downloadImage(url, worker_id):
    # could be encoded in jpg, gif, etc
    encoded_str = urllib2.urlopen(url).read()

    buffers = []
    w, h = 0, 0

    parser = ImageFile.Parser()
    # decompress to bitmap
    parser.feed(encoded_str)
    pil_image = parser.close()
    w, h = pil_image.size

    if pil_image.format == "GIF" and pil_image.info.has_key('duration'):
        if GIF_SUPPORT:
            scratch_dir = os.path.join('..', '_scratch')
            scratch_name = 'scratch%d' % worker_id
            # save to disk and use gifsicle to explode into frames
            scratch_path = os.path.join(scratch_dir, scratch_name)
            scratch_file = open(scratch_path, 'w')
            scratch_file.write(encoded_str)
            scratch_file.close()

            num_frames = 0
            pil_image = Image.open(scratch_path)
            for i in ImageSequence.Iterator(pil_image):
                num_frames += 1
            pil_image.close()

            cmd = 'gifsicle -w --colors=255 %s | gifsicle -w -U -e -o=%s' % \
                (scratch_path, os.path.join(scratch_dir, scratch_name))
            os.system(cmd)

            try:
                for i in range(num_frames):
                    scratch_file = os.path.join(scratch_dir, '%s.%03d' % \
                        (scratch_name, i))
                    frame = Image.open(scratch_file)
                    frame = frame.convert('RGB')
                    buffers.append(frame.tostring())
                    frame.close()
            except Exception:
                return None, None, None
        else:
            return None, None, None
    else:
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        buff = pil_image.tostring()
        buffers = [buff]
        pil_image.close()

    return w, h, buffers

# This is a worker function that sits in it's own process
def _worker(in_queue, out_queue, worker_id):
    try:
        import setproctitle
        setproctitle.setproctitle("imageWorker")
    except ImportError:
        pass

    done = False
    while not done:
        if not in_queue.empty():
            obj = in_queue.get()
            # if a bool is passed down the queue, set the done flag
            if isinstance(obj, bool):
                print "got a bool down the pipe; shutting down"
                done = True
                import sys
                #sys.exit()
            else:
                url = obj
                
                w, h, buffers = _downloadImage(url, worker_id)
                if w != None:
                    out_queue.put((url, w, h, buffers))
        pygame.time.wait(SLEEP_TIME)

def start():
    downloader_process.start()

def stop():
    print "Stopping async image download worker"
    global worker_done
    url_queue.empty()
    downloader_process.terminate()
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

SLEEP_TIME = 30
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

# detect GIF support
GIF_SUPPORT = True
try:
    subprocess.call(["gifsicle", '--version'])
except OSError:
    GIF_SUPPORT = False

if not os.path.exists('../_scratch'):
    os.mkdir('../_scratch')

worker_done = False
url_queue = multiprocessing.queues.SimpleQueue()
img_buffer_queue = multiprocessing.queues.SimpleQueue()

on_load_callbacks = {}

downloader_process = multiprocessing.Process(None, _worker, \
    "async image load worker", (url_queue, img_buffer_queue, 1))

start()