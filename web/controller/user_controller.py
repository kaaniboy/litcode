import os
from flask import Flask, session, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
from bs4 import BeautifulSoup
import random
import string

from room_service import RoomService

# performs the higher-level business logic for user-related endpoints
class UserController:
    def __init__( self ):
        pass

    # public endpoint functions

    def handle_join( self, data ):
        name = data['name']
        room = data['room']
        
        join_room(room)

        RoomService.add_socket( request.sid, {
            'name': name,
            'room': room,
            'code': ''
        } )

        emit('room_info', self._get_room_info(room), room=room)
        emit('join_accepted')

        print( RoomService.read_socket() )

    def handle_leave( self ):
        sockets = RoomService.read_socket()

        room = sockets[request.sid]['room']
        RoomService.delete_socket( request.sid )

        emit('room_info', self._get_room_info(room), room=room)

        print( RoomService.read_socket() )

    def handle_run( self, data ):
        sockets = RoomService.read_socket()
        rooms = RoomService.read_room()

        name = sockets[request.sid]['name']
        room = sockets[request.sid]['room']

        if data['problem'] != rooms[room]['problem']:
            return

        emit('run', {'name': name, 'room': room}, room=room)
        
        print('%s ran code in room %s' % (name, room))

    def handle_solution_accepted( self, data ):
        rooms = RoomService.read_room()
        sockets = RoomService.read_socket()

        name = sockets[request.sid]['name']
        room = sockets[request.sid]['room']

        if data['problem'] != rooms[room]['problem']:
            return
        
        RoomService.add_code( request.sid, data['code'] )

        if sockets[request.sid] not in rooms[room]['accepted_players']:
            RoomService.add_accepted_user( request.sid, room )

        emit('solution_accepted', {'name': name, 'room': room}, room=room)
        emit('room_info', self._get_room_info(room), room=room)

    def handle_solution_declined( self, data ):
        sockets = RoomService.read_socket()
        rooms = RoomService.read_room()

        name = sockets[request.sid]['name']
        room = sockets[request.sid]['room']

        if data['problem'] != rooms[room]['problem']:
            return

        emit('solution_declined', {'name': name, 'room': room}, room=room)
        emit('room_info', self._get_room_info(room), room=room)

    def handle_next_problem( self, data ):
        sockets = RoomService.read_socket()
        rooms = RoomService.read_room()

        room = sockets[request.sid]['room']

        rooms[room]['problem'] = random.choice( RoomService.read_problems() )
        rooms[room]['accepted_players'] = []

        emit('room_info', self._get_room_info(room), room=room)

    # private functions
    def _get_players_in_room(self,room):
        sockets = RoomService.read_socket()
        return [s for s in sockets.values() if s['room'] == room and s['name'] != None]

    def _get_room_info(self,room):
        rooms = RoomService.read_room()
        players = self._get_players_in_room(room)
        accepted_players = rooms[room]['accepted_players']

        return {
            'problem': rooms[room]['problem'],
            'players': players,
            'accepted_players': accepted_players
        }