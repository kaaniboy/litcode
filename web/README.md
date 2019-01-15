# Litcode

# Web Server File documentation

- /routes : Sets up the endpoints that the server should react to; should only declare them, not perform any operations
- /controller : Performs the heavy lifting of acting upon the data and changing application state; does not interact directly with the database
- /services : Direction communication line with the server; controllers use services to retrieve data, relay post requests, etc
