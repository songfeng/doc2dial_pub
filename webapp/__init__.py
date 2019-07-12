from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient
import json
import os
from os import sys, path
from pathlib import Path

# Configure file paths for HTMLs, Jinga2 Templates, JavaScripts (JS) and CSS
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to webapp folder
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_STATIC_DATA = os.path.join(APP_STATIC, 'data')
APP_TEMPLATE = os.path.join(APP_ROOT, 'templates')
APP_DATA = os.path.join(APP_ROOT, 'data')
APP_DOMAIN = os.path.join(APP_ROOT, 'domains')

# Load configuration for the demo application
config = None
CONFIG_PATH = 'configs/app-config.{}.json'.format(os.environ['domain'])
with open(path.join(CONFIG_PATH).format(os.environ['domain']), 'r') as f:
    config = json.load(f)

# Connect to backend database (MongoDB)
if 'MONGO_SERVICE_HOST' in os.environ:
    db_uri = os.getenv('MONGO_SERVICE_HOST')
else:
    db_uri = os.environ['dburi']
    
cli = MongoClient(db_uri)
db_ = cli[config['domain_db']['db_name']]

# Create a flask App
socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'RAWEFAwW#$Q$'
    from .main import app as main_blueprint
    app.register_blueprint(main_blueprint)
    socketio.init_app(app)
    return app
