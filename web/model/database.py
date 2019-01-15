# stopgap solution for our global data; replace with database in the future
class Database:
    # static by default
    rooms = {}
    sockets = {}

    PROBLEMS = ['1. Two Sum', '15. 3Sum', '18. 4Sum']