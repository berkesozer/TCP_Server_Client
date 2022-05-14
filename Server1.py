# This is the multi threaded server application for Task #1 

# We use the socket module for establishing a TCP connection between the server and client. 


import socket

# The threading module is used for implementing a multi threaded server. 

from threading import * 

# We use a lock object to protect the critical sections of our program, from race conditions. 
resource_lock = Lock()

users = [] # This list stores, the list of users already holding a connection with the server.

# This is the main function that handles a client connected with our server.
# "cs" - is the client socket.# "c_addr" - is address of the client application, connected with the server. 
# "database" - is a Python dictionary containing usernames and passwords. 


def handle_connection(cs, c_addr, database):
	resource_lock.acquire()
	print(f"\t[+] Thread with ID {current_thread().ident}, is serving client with address: {c_addr}")
	resource_lock.release()
	# We receive the username and SHA256 hashed password from the client
	
	data = cs.recv(1024).decode("ascii").split(" ")
	
	# We decode the message and split the username and the password.  
	#      data[0] is the username received from the client, data[1] is the hashed password received from the client.
	
	# Before we test for authentication, we will check if this particular username is already logged in. 
	# Since, multiple login is not allowed, we will respond with an error message if they are already logged in.
	if data[0] in users:
		# This means the given username is already logged in. 
		# First we will send the error message to the client application attempting multiple login. 
		cs.send(f"[!] Error: {data[0]} already logged in.Multiple login attempts are not allowed. ".encode("ascii"))
		# We will close the connection and stop handling it.
		cs.close()
		return
	
	# If the username is not already logged in, then we will test their authenticity.
	try:
		database_pwd = database[data[0]]
		if database_pwd == data[1]:
			# The client was able to successfully login
			cs.send("[+] Authentication successfull ! ".encode("ascii"))
			resource_lock.acquire()
			users.append(data[0])
			resource_lock.release()
			resp = cs.recv(1024).decode("ascii").strip()
			# Finally we implement the logout routine. 
			if resp == "LOGOUT":
				
				cs.send("[+] Thankyou for logging in ! You are being logged out !".encode("ascii"))
				
			
		else:
			cs.send("[!] Authentication Declined ! Wrong password provided !".encode("ascii"))
			cs.close()
			return
		
	except KeyError:
	   cs.send("[!] Username not found ! Authentication Declined !".encode("ascii"))
	   cs.close()
	   return
	   
    
	# We finally close the connection. 
	cs.close()
	
	# We remove the username from the list of logged in users.
	resource_lock.acquire()
	users.remove(data[0])
	resource_lock.release()
	
	
	
	
def get_database(fpath):
	
	database = {}
	with open(fpath, "r") as fObj:
		# Each line of the database contains the username and SHA256 hash of the password for a particular user, separated by space " "
		# We use the split() function to get the username and hash individually from the line.
		# We use strip() function to remove unnecessary white spaces (if any) from the beginning and ending of a string. 
		for line in fObj:
			if len(line) != 0: # If line is not empty
				database[line.split(" ")[0].strip()] = line.split(" ")[1].strip()
			
	return database
			
	
def main():
	
	# We get the database.
	db = get_database("database1.txt")
	
	# We create a server socket for TCP connection. 
	serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# We bind the server to port 8080 on local host (this computer) IP 
	serv_socket.bind(("127.0.0.1", 8080))
	
	print("------SERVER APPLICATION #1------\n")
	
	serv_socket.listen(5)
	
	while True:
		
		# We lock the standard output stream, so that we can safely write to the terminal, without interfering with other threads of the server.
		# After using the resource we will release it.
		
		# We follow this lock release pattern, whenever we use a shared resource. 
		
		resource_lock.acquire() 
		print("\n[+] Server is waiting for a new connection.")
		resource_lock.release() 
		cs, c_addr = serv_socket.accept()
		 
		resource_lock.acquire() 
		
		print(f"[+] Received connection from client {c_addr}")
		resource_lock.release()
		
		# Finally we create a thread to handle a new connection. 
		
		th = Thread(target=handle_connection, args=(cs, c_addr, db))
		
		resource_lock.acquire()
		
		print(f"[+] Thread created for handling connection from client {c_addr}")
		resource_lock.release()
		
		# We start the thread. 
		th.start()
		
		
if __name__== "__main__":
	main()

