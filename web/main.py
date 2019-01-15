import os
from flask import Flask, session, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
from bs4 import BeautifulSoup
import random
import string

# MUST configure paths before any non-main directory paths are used
import path_setup
path_setup.setupPaths()

from app_router import Routes

app = Flask(__name__)
app.secret_key = 'flex'
app.config['SESSION_TYPE'] = 'filesystem'

socketio = SocketIO(app)

appRoutes = Routes( socketio, app )

if __name__ == '__main__':
    socketio.run(app)

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)