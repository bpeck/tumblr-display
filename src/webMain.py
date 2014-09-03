from flask import Flask
import multiprocessing
from web.Backend import Backend

info_queue = multiprocessing.queues.Queue()
command_queue = multiprocessing.queues.SimpleQueue()
flask_app = Flask(__name__)

Backend(command_queue, info_queue, flask_app, host='localhost', port=8000, debug=True)
