# This is the client application for Task #1 
# We use the socket module for TCP server - client communication.

import socket
from hashlib import sha256
# We need to get the hash of the user typed password.


def main():
	
	serv_addr = ("127.0.0.1", 8080)
	print("-----CLIENT APPLICATION-----\n")
	# We prompt the user to enter their username and password 
	username = input("Please type username: ")
	password = input("Please type password: ")
	
	print("\n----------------------------")
	print(f"[+] Connecting to server at: {serv_addr}")
	# A socket object is created to communicate with the server
	cl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# We initiate the connection. 
	
	cl_sock.connect(serv_addr)
	
	data = username + " " + sha256(password.encode("ascii")).hexdigest()
	
	# NOTE: We are hashing the password using the SHA256 hash function.
	
	print("[+] Requesting authentication with given credentials. ")
	
	# We send the username and password in the format that can be parsed by the server
	
	cl_sock.send(data.encode("ascii"))
	response = cl_sock.recv(1024).decode("ascii")
	# We decode the response and print it out to the terminal. 
	print("RESPONSE from server: {0}".format(response))
	
	# If authentication was successfull, then the response string from the server will definitly contain a "[+]" symbol at the beginning. 
	# We examine if it is there to programatically check, if the authentication was successfull. 
	
	if response.split(" ")[0] == "[+]":
		print("\n---LOGGED IN---")
		x = input("\nPress ENTER to logout from the server. ")
		
		# We signal the server that we are logging out. 
		cl_sock.send("LOGOUT".encode("ascii"))
		
		resp = cl_sock.recv(1024).decode("ascii")
		
		print("\nResponse from the server:\n{0}".format(resp))
		
		
		
	else:
		print("\n[!] AUTHENTICATION FAILED ! ")
		print("Unable to access services provided by server. ")
	
	
	print("\n------SESSION TERMINATED -----")
	cl_sock.close()
		
if __name__ == "__main__":
	main()