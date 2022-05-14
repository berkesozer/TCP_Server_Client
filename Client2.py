# This is the client application for Task #2

# We use the socket module for TCP server - client communication.

import socket
from hashlib import sha256
# We need to get the hash of the user typed password.


def main():
	
	serv_addr = ("127.0.0.1", 8088)
	print("-----CLIENT APPLICATION #2-----\n")
	# We prompt the user to enter their username and password 
	username = input("Please type username: ")
	password = input("Please type password: ")
	
	print("\n----------------------------")
	print(f"[+] Connecting to server at: {serv_addr}")
	# A socket object is created to communicate with the server
	cl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# We initiate the connection. 
	
	cl_sock.connect(serv_addr)
	
	print("[+] Sending username to the server. ")
	
	# We send the username to the server and the server will return the SHA256 hash of the correct password, that is mapped with the username.
	# If username is not found, then response string from the server will definitely have the string "[!]" indicating an error, otherwise the response string will definitely have "[+]" at the beginning.
	
	cl_sock.send(username.encode("ascii"))
	
	response = cl_sock.recv(1024).decode("ascii")
	
	if response.split(" ")[0] == "[+]":
		# Now our client application needs to parse the hex encoded hash of the correct password that was received from the Server.
		
		correct_hash = response.split(" ")[1]
		
		# Now we check if the hash of the user typed password is same as the SHA256 hash received from server
		
		user_hash = sha256(password.encode("ascii")).hexdigest()
		
		if user_hash == correct_hash:
			
			# We inform the server that authentication was successfull 
			cl_sock.send("[+]".encode("ascii"))
			
			print("\n[+]	Authentication successfull !")
			# We receive and print the LOGGED IN greeting from the server
			
			response = cl_sock.recv(1024).decode("ascii")
			print(response)
			
			x = input("\nPress ENTER to logout from the server. ")
			
			# We inform the server that we are about to logout 
			cl_sock.send("LOGOUT".encode("ascii"))
			resp = cl_sock.recv(1024).decode("ascii")
			
			print("\nResponse from the server:\n{0}".format(resp))
		
			
		else:
			print("[!] Authentication failed. Wrong password !!! ")
			
			cl_sock.send("[!]".encode("ascii"))
			
		
		
		
		
		
	else: 
	    # This means an error response was received from the server side
		print("\n[!] AUTHENTICATION FAILED ! ")
		print("\nResponse from the server:\n{0}".format(response))
	
	
	print("\n------SESSION TERMINATED -----")
	cl_sock.close()
		
if __name__ == "__main__":
	main()