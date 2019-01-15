import os
from flask import Flask, session, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
from bs4 import BeautifulSoup
import random
import string

from room_service import RoomService

# take this import out later
from database import Database

# Specific endpoints to admin related tasks
class UserEndpoints:
    def __init__( self, socketio, app ):
        self.configureEndpoints( socketio )

    def configureEndpoints( self, socketio ):
        @socketio.on('join')
        def handle_join(data):
            name = data['name']
            room = data['room']
            
            join_room(room)

            RoomService.addSocket( request.sid, {
                'name': name,
                'room': room,
                'code': ''
            } )

            emit('room_info', _get_room_info(room), room=room)
            emit('join_accepted')

            print( RoomService.readSocket() )

        @socketio.on('disconnect')
        def handle_leave():
            sockets = RoomService.readSocket()

            room = sockets[request.sid]['room']
            RoomService.deleteSocket( request.sid )

            emit('room_info', _get_room_info(room), room=room)

            print( RoomService.readSocket() )

        @socketio.on('run')
        def handle_run(data):

            sockets = RoomService.readSocket()
            rooms = RoomService.readRoom()

            name = sockets[request.sid]['name']
            room = sockets[request.sid]['room']

            if data['problem'] != rooms[room]['problem']:
                return

            emit('run', {'name': name, 'room': room}, room=room)
            
            print('%s ran code in room %s' % (name, room))

        # Here and down i get lazy and just reference things directly from the database (change in future)
        @socketio.on('solution_accepted')
        def handle_solution_accepted(data):
            name = Database.sockets[request.sid]['name']
            room = Database.sockets[request.sid]['room']

            if data['problem'] != Database.rooms[room]['problem']:
                return
            
            Database.sockets[request.sid]['code'] = data['code']

            if Database.sockets[request.sid] not in Database.rooms[room]['accepted_players']:
                Database.rooms[room]['accepted_players'].append(Database.sockets[request.sid])

            emit('solution_accepted', {'name': name, 'room': room}, room=room)
            emit('room_info', _get_room_info(room), room=room)

        @socketio.on('solution_declined')
        def handle_solution_declined(data):
            name = Database.sockets[request.sid]['name']
            room = Database.sockets[request.sid]['room']

            if data['problem'] != Database.rooms[room]['problem']:
                return

            emit('solution_declined', {'name': name, 'room': room}, room=room)
            emit('room_info', _get_room_info(room), room=room)

        @socketio.on('next_problem')
        def handle_next_problem(data):
            room = Database.sockets[request.sid]['room']

            Database.rooms[room]['problem'] = random.choice(Database.PROBLEMS)
            Database.rooms[room]['accepted_players'] = []

            emit('room_info', _get_room_info(room), room=room)

def _get_players_in_room(room):
    return [s for s in Database.sockets.values() if s['room'] == room and s['name'] != None]

def _get_room_info(room):
    players = _get_players_in_room(room)
    accepted_players = Database.rooms[room]['accepted_players']

    return {
        'problem': Database.rooms[room]['problem'],
        'players': players,
        'accepted_players': accepted_players
    }