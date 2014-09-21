import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 16969                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

while True:
	s.listen(5)                 # Now wait for client connection.
	c, addr = s.accept()     # Establish connection with client. 
	c.send("i'm gay")
