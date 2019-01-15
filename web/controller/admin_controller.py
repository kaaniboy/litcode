import os
from flask import Flask, session, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
from bs4 import BeautifulSoup
import random
import string

from room_service import RoomService

# Performs the higher level business logic for admin-related endpoints
class AdminController:
    def __init__( self ):
        pass

    def index_get( self ):
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

    def create_room_post( self ):
        room = request.form['room']
        password = request.form['room_password']

        rooms = RoomService.read_room()

        if room in rooms:
            session['message'] = 'The room already exists.'
            return redirect('/')
        
        session.clear()

        RoomService.add_room( room, {
            'password': password,
            'problem': '1. Two Sum',
            'accepted_players': []
        } )

        return redirect('/room/%s' % room)

    def view_room_post( self ):
        room = request.form['room']
        password = request.form['room_password']

        rooms = RoomService.read_room()

        if room in rooms and rooms[room]['password'] == password:
            session.clear()
            return redirect('/room/%s' % room)
        else:
            session['tab'] = 'view_room'
            session['view_room'] = room
            session['message'] = 'Either the room or its password is incorrect.'

            return redirect('/')

    def room_get( self, room ):
        return render_template('room.html', room=room)