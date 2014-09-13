import os
import multiprocessing
import multiprocessing.queues
import Queue

import json

import tornado.ioloop
import tornado.web
import tornado.template

import web

from controllers.RootModelCommands import GetInfoCommand, NextCommand, PauseCommand, PrevCommand, SetModelRootCommand, SetModelTypeCommand

HOST = 'localhost'
PORT = 8000

def parseCommandString(http_args):
    if not http_args.has_key('command'):
        return None

    if http_args['command'] == 'next':
        return NextCommand()
    elif http_args['command'] == 'prev':
        return PrevCommand()
    elif http_args['command'] == 'pause':
        return PauseCommand()
    elif http_args['command'] == 'set_root':
        if http_args.has_key('root_path'):
            return SetModelRootCommand(http_args['root_path'])
        else:
            return None
    elif http_args['command'] == 'set_model':
        if http_args.has_key('model_type') and http_args.has_key('root_path'):
            return SetModelTypeCommand(http_args['model_type'], http_args['root_path'])
        else:
            return None

static_path = os.path.realpath(os.path.normpath(os.path.join(web.__file__, '..')))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_argument('action', None) == 'refresh-info':
            info = {}
            try:
                command_queue.put(GetInfoCommand())
                template_filename, info_context = info_queue.get(True, 5)
                info['html'] = self.render_string(template_filename, **info_context)                    
            except Queue.Empty:
                info['html'] = "<p><strong>Could not refresh. Please try again.</storng></p>"
            finally:
                info['success'] = True
                info['content_type'] = 'application/json'
                self.write(json.dumps(info))
        else:
            self.render(os.path.join(static_path, "templates", "index.html"), static_url=self.static_url, ip=HOST, port=str(PORT))

    def post(self):
        data = json.loads(self.request.body)
        cmd = parseCommandString(data)
        if cmd:
            command_queue.put(cmd)
            print "Parsed a [%s] command" % cmd.desc
        else:
            print "Could not parse a command from " + str(data)

class ShutdownHandler(tornado.web.RequestHandler):
    def get(self):
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.add_callback(lambda x: x.stop(), ioloop)

def _worker(command_queue, info_queue):
    print "Starting up web interface worker"
    application = tornado.web.Application(\
        [(r"/", MainHandler), (r"/shutdown", ShutdownHandler)], \
        static_path = os.path.join(static_path, 'static'))
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()

def stop():
    while not command_queue.empty():
        command_queue.get()
    
    if web_backend_process:
        import urllib2
        urllib2.urlopen('http://%s:%d/shutdown' % (HOST, PORT))
        print "Asked Tornado to stop."

def start():
    global web_backend_process
    if web_backend_process and web_backend_process.pid != None:
        stop()
    web_backend_process = multiprocessing.Process(group=None, target=_worker, \
        name="web_interface", args=[command_queue, info_queue])
    web_backend_process.start()

def poll():
    if not command_queue.empty():
        return command_queue.get()
    else:
        return None

info_queue = multiprocessing.queues.Queue()
command_queue = multiprocessing.queues.SimpleQueue()
web_backend_process = None

if __name__ == '__main__':
    start()
