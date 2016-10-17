# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 23:42:09 2016

@author: anthonyweston
"""

#creating a server

import socket
import sys
import _thread

HOST = '' #symbolic name respresenting all available interfaces
PORT = 8888 #arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket Created")

try:
    #bind the socket to a particular ip address and port, all incoming data goes to this port
    s.bind((HOST, PORT))
except socket.error as msg:
    msg = str(msg)
    print("Bind Failed. Error : " + msg[1:9] + " , Error message : " + msg[11:])
    
    sys.exit() #exits from python, program ended
    
print("Socket Bind Complete")

s.listen(10) #number of requests that can wait in line for a response at any time
print("Socket Now Listening")


def clientthread(conn):
    conn.send(b"Welcome to server. Type something and hit enter\n")
    
    while True:

    
        data = conn.recv(1024)
        reply = bytes("OK... " + data.decode(encoding = "utf-8",errors = "strict"), "utf-8")
        if not data:
            break
    
        conn.sendall(reply)

    conn.close()
    
while 1:
    ###wait to accept a connection?
    conn, addr = s.accept()
    #display client information
    print("Connected with " + addr[0] + ":" + str(addr[1]))    

    _thread.start_new_thread(clientthread, (conn,))

s.close()