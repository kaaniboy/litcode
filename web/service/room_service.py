from database import Database

# Getters and setters for the data; for now we just use the static data class
class RoomService:
    def __init__( self ):
        pass

    def read_room( ):
        return Database.rooms

    def read_socket( ):
        return Database.sockets

    def read_problems( ):
        return Database.PROBLEMSs

    def add_room( room_key, room ):
        Database.rooms[room_key] = room

    def add_socket( sid, socket ):
        Database.sockets[sid] = socket

    def add_code( sid, code ):
        Database.sockets[sid]['code'] = code

    def add_accepted_user( sid, room ):
        Database.rooms[room]['accepted_players'].append( Database.sockets[sid] )

    def delete_socket( sid ):
        del Database.sockets[sid]