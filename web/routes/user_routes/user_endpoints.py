from user_controller import UserController

# Specific endpoints to admin related tasks
class UserEndpoints:
    def __init__( self, socketio, app ):
        self.configure_endpoints( socketio )
        self.user_controller = UserController()

    def configure_endpoints( self, socketio ):
        @socketio.on('join')
        def handle_join(data):
            self.user_controller.handle_join(data)
            
        @socketio.on('disconnect')
        def handle_leave():
            self.user_controller.handle_leave()
            
        @socketio.on('run')
        def handle_run(data):
            self.user_controller.handle_run( data )

        @socketio.on('solution_accepted')
        def handle_solution_accepted(data):
            self.user_controller.handle_solution_accepted( data )

        @socketio.on('solution_declined')
        def handle_solution_declined(data):
            self.user_controller.handle_solution_declined( data )

        @socketio.on('next_problem')
        def handle_next_problem(data):
            self.user_controller.handle_next_problem( data )