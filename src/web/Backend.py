import multiprocessing
import multiprocessing.queues
import Queue
from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import jsonify

from controllers.RootModelCommands import GetInfoCommand, NextCommand, PrevCommand, SetModelRootCommand, SetModelTypeCommand

HOST = 'localhost'
PORT = 8000

def parseCommandString(http_args):
    if not http_args.has_key('command'):
        return None

    if http_args['command'] == 'next':
        return NextCommand()
    elif http_args['command'] == 'prev':
        return PrevCommand()
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

class Backend(object):
    def __init__(self, command_queue, info_queue, flask_app=None, host='localhost', port=8000, debug=True):
        self.host = host
        self.port = port
        self.debug = debug
        self.command_queue = command_queue
        self.info_queue = info_queue
        self.flask_app = flask_app or Flask('web')
        flask_app.add_url_rule('/', "handleRequest", self.handleRequest, methods=['GET', 'POST'])
        flask_app.add_url_rule('/shutdown', "handleShutdownRequest", self.handleShutdownRequest, methods=['GET', 'POST'])
    
    def handleRequest(self):
        ret = ""
        # handle AJAX command POST request
        if request.method == 'POST':            
            cmd = parseCommandString(request.json)
            if cmd:
                self.command_queue.put(cmd)
                print "Parsed a [%s] command" % cmd.desc
            else:
                print "Could not parse a command from " + str(request.json)
        else:
            # handle AJAX info GET request
            if request.args.get('action', None) == 'refresh-info':
                info = {}
                try:
                    self.command_queue.put(GetInfoCommand())
                    template_filename, info_context = self.info_queue.get(True, 5)
                    info['html'] = render_template(template_filename, **info_context)                    
                except Queue.Empty:
                    info['html'] = "<p><strong>Could not refresh. Please try again.</storng></p>"
                finally:
                    return jsonify(info)
            else:
                return render_template('index.html', ip=self.host, port=self.port)

        return ret

    def handleShutdownRequest(self):
        self.shutdownServer()
        return 'Server shut down.'

    def shutdownServer(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

def _worker(command_queue, info_queue):
    print "Starting up web interface worker"
    b = Backend(command_queue, info_queue, HOST, PORT)
    b.flask_app.run(host=b.host, port=b.port, debug=b.debug, use_reloader=False)
    print "Web interface worker stopped."

def stop():
    while not command_queue.empty():
        command_queue.get()
    if web_backend_process:
        import urllib2
        urllib2.urlopen('http://%s:%d/shutdown' % (HOST, PORT))

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
