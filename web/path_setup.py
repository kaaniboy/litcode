import sys

def setupPaths():
    sys.path.append( './routes' )
    sys.path.append( './routes/user_routes' )
    sys.path.append( './routes/admin_routes' )
    sys.path.append( './service' )
    sys.path.append( './model' )
    sys.path.append( './controller' )