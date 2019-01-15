import os
from flask import Flask, session, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
from bs4 import BeautifulSoup
import random
import string

from admin_endpoints import AdminEndpoints
from user_endpoints import UserEndpoints

# Hooks up the app to the endpoint files that we want to use
class Routes:
    def __init__( self, socketio, app ):
        self.userEndpoints = UserEndpoints( socketio, app )
        self.adminEndpoints = AdminEndpoints( socketio, app )