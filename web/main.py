import os
from flask import Flask, session, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
from bs4 import BeautifulSoup
import random
import string

app = Flask(__name__)
app.secret_key = 'flex'
app.config['SESSION_TYPE'] = 'filesystem'

socketio = SocketIO(app)

rooms = {}
sockets = {}

PROBLEMS = ['Two Sum', 'Three Sum', 'Four Sum']

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
        'problem': 'Two Sum'
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

@socketio.on('join')
def handle_join(data):
    name = data['name']
    room = data['room']
    
    join_room(room)

    sockets[request.sid] = {
        'name': name,
        'room': room,
        'accepted': False
    }

    players = _get_players_in_room(room)

    emit('room_info', {'players': players, 'problem': 'Two Sum'}, room=room)
    emit('join_accepted')

    print(str(sockets))

@socketio.on('disconnect')
def handle_leave():
    room = sockets[request.sid]['room']
    del sockets[request.sid]

    players = _get_players_in_room(room)
    emit('room_info', {'players': players}, room=room)

    print(str(sockets))

@socketio.on('run')
def handle_run(data):
    name = sockets[request.sid]['name']
    room = sockets[request.sid]['room']

    emit('run', {'name': name, 'room': room}, room=room)
    
    print('%s ran code in room %s' % (name, room))

@socketio.on('solution_accepted')
def handle_solution_accepted(data):
    name = sockets[request.sid]['name']
    room = sockets[request.sid]['room']

    sockets[request.sid]['accepted'] = True

    players = _get_players_in_room(room)

    emit('solution_accepted', {'name': name, 'room': room}, room=room)
    emit('room_info', {'players': players}, room=room)

@socketio.on('solution_declined')
def handle_solution_declined(data):
    name = sockets[request.sid]['name']
    room = sockets[request.sid]['room']

    players = _get_players_in_room(room)

    emit('solution_declined', {'name': name, 'room': room}, room=room)
    emit('room_info', {'players': players}, room=room)

@socketio.on('next_problem')
def handle_next_problem(data):
    room = sockets[request.sid]['room']
    rooms[room]['problem'] = random.choice(PROBLEMS)

    emit('room_info', {'problem': rooms[room]['problem']}, room=room)

def _get_players_in_room(room):
    return [s for s in sockets.values() if s['room'] == room and s['name'] != None]

if __name__ == '__main__':
    socketio.run(app)

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)