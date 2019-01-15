
from admin_controller import AdminController

# Specific endpoints to admin related tasks
class AdminEndpoints:
    def __init__( self, socketio, app ):
        self.configure_endpoints( app )
        self.admin_controller = AdminController()

    def configure_endpoints( self, app ):
        @app.route('/', methods=['GET'])
        def index_get():
            return self.admin_controller.index_get()

        @app.route('/create_room', methods=['POST'])
        def create_room_post():
            return self.admin_controller.create_room_post()

        @app.route('/view_room', methods=['POST'])
        def view_room_post():
            return self.admin_controller.view_room_post()

        @app.route('/room/<room>', methods=['GET'])
        def room_get(room):
            return self.admin_controller.room_get( room )
            