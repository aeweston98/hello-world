# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 22:32:38 2016

@author: anthonyweston
"""

import socket #for socket
import sys #system specific parameters and functions (for exit)


#Address Family : AF_INET (this is IP version 4 or IPv4)
#Type : SOCK_STREAM (this means connection oriented TCP protocol)


#The try statement works as follows.
#First, the try clause (the statement(s) between the try and except keywords) is executed.
#If no exception occurs, the except clause is skipped and execution of the try statement is finished.
#If an exception occurs during execution of the try clause, the rest of the clause is skipped. Then if its type matches the exception named after the except keyword, the except clause is executed, and then execution continues after the try statement.
#If an exception occurs which does not match the exception named in the except clause, it is passed on to outer try statements; if no handler is found, it is an unhandled exception and execution stops with a message as shown above.

try:
    #socket.socket() creates a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print("Failed to create socket. Error code: " + str(msg[0]) + " , Error message : " + msg[1])
    sys.exit() #exits from python, program ended
    
print("Socket Created")

host = "www.google.com"
#must use port 80
port = 80

try:
    remote_ip = socket.gethostbyname(host)
    
except socket.gaierror:
    #host name is invalid (gai = getaddrinfo())
    print("Host name could not be resolved. Exiting")
    sys.exit()

print("The IP adress of " + host + " is " + str(remote_ip))

#connect to remote host, connect is a member function of the socket object
s.connect((remote_ip, port))

print("Socket connected to " + host + " on port " + str(port))

#a request to send, b makes the string a byte-like object
message = b'GET / HTTP/1.1\r\n\r\n'

try:
    s.sendall(message)
except socket.error:
    print("Send failed. Exiting.")
    sys.exit()    

print("Message sent successfully")

reply = s.recv(4096)

print(reply)

s.close()
