#!/bin/sh
uwsgi --http :8000 --wsgi-file webMain.py --callable flask_app --catch-exceptions & python main.py
