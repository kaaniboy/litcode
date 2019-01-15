import os
from flask import Flask, session, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
from bs4 import BeautifulSoup
import random
import string

# Specific endpoints to admin related tasks
class AdminEndpoints:
    def __init__( self, socketio, app ):
        self.configureEndpoints( app )

    def configureEndpoints( self, app ):
        @app.route('/', methods=['GET'])
        def index_get():
            create_room = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

            view_room = ''
            if 'view_room' in session:
                view_room = session['view_room']
            
            create_tab = True

            if 'tab' in session and session['tab'] == 'view_room':
                create_tab = False
            
            message = ''
            if 'message' in session:
                message = session['message']
            
            return render_template('index.html', create_room=create_room, view_room=view_room, message=message, create_tab=create_tab)

        @app.route('/create_room', methods=['POST'])
        def create_room_post():
            room = request.form['room']
            password = request.form['room_password']

            if room in rooms:
                session['message'] = 'The room already exists.'
                return redirect('/')
            
            session.clear()

            rooms[room] = {
                'password': password,
                'problem': '1. Two Sum',
                'accepted_players': []
            }

            return redirect('/room/%s' % room)

        @app.route('/view_room', methods=['POST'])
        def view_room_post():
            room = request.form['room']
            password = request.form['room_password']

            if room in rooms and rooms[room]['password'] == password:
                session.clear()
                return redirect('/room/%s' % room)
            else:
                session['tab'] = 'view_room'
                session['view_room'] = room
                session['message'] = 'Either the room or its password is incorrect.'

                return redirect('/')

        @app.route('/room/<room>', methods=['GET'])
        def room_get(room):
            return render_template('room.html', room=room)