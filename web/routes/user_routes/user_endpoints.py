import os
from flask import Flask, session, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
from bs4 import BeautifulSoup
import random
import string

# pretend these are global!
rooms = {}
sockets = {}

PROBLEMS = ['1. Two Sum', '15. 3Sum', '18. 4Sum']

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

            sockets[request.sid] = {
                'name': name,
                'room': room,
                'code': ''
            }

            emit('room_info', _get_room_info(room), room=room)
            emit('join_accepted')

            print(str(sockets))

        @socketio.on('disconnect')
        def handle_leave():
            room = sockets[request.sid]['room']
            del sockets[request.sid]

            emit('room_info', _get_room_info(room), room=room)

            print(str(sockets))

        @socketio.on('run')
        def handle_run(data):
            name = sockets[request.sid]['name']
            room = sockets[request.sid]['room']

            if data['problem'] != rooms[room]['problem']:
                return

            emit('run', {'name': name, 'room': room}, room=room)
            
            print('%s ran code in room %s' % (name, room))

        @socketio.on('solution_accepted')
        def handle_solution_accepted(data):
            name = sockets[request.sid]['name']
            room = sockets[request.sid]['room']

            if data['problem'] != rooms[room]['problem']:
                return
            
            sockets[request.sid]['code'] = data['code']

            if sockets[request.sid] not in rooms[room]['accepted_players']:
                rooms[room]['accepted_players'].append(sockets[request.sid])

            emit('solution_accepted', {'name': name, 'room': room}, room=room)
            emit('room_info', _get_room_info(room), room=room)

        @socketio.on('solution_declined')
        def handle_solution_declined(data):
            name = sockets[request.sid]['name']
            room = sockets[request.sid]['room']

            if data['problem'] != rooms[room]['problem']:
                return

            emit('solution_declined', {'name': name, 'room': room}, room=room)
            emit('room_info', _get_room_info(room), room=room)

        @socketio.on('next_problem')
        def handle_next_problem(data):
            room = sockets[request.sid]['room']

            rooms[room]['problem'] = random.choice(PROBLEMS)
            rooms[room]['accepted_players'] = []

            emit('room_info', _get_room_info(room), room=room)

def _get_players_in_room(room):
    return [s for s in sockets.values() if s['room'] == room and s['name'] != None]

def _get_room_info(room):
    players = _get_players_in_room(room)
    accepted_players = rooms[room]['accepted_players']

    return {
        'problem': rooms[room]['problem'],
        'players': players,
        'accepted_players': accepted_players
    }