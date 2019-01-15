from database import Database

# Getters and setters for the data; for now we just use the static data class
class RoomService:
    def __init__( self ):
        pass

    def readRoom( ):
        return Database.rooms

    def readSocket( ):
        return Database.sockets

    def addRoom( roomKey, room ):
        Database.rooms[roomKey] = room

    def addSocket( sid, socket ):
        Database.sockets[sid] = socket

    def deleteSocket( sid ):
        del Database.sockets[sid]