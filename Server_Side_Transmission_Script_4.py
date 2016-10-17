# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 17:13:47 2016

@author: anthonyweston
"""

import socket
import sys
import _thread


#important to set this value
host = ''
key = "server"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = int(input("Enter port number: "))
shift = int(input("Enter Ceaser Cipher Key: "))

try:
    #bind the socket to a particular ip address and port, all incoming data goes to this port
    s.bind((host, port))
except socket.error as msg:
    msg = str(msg)
    print("Bind Failed. Error : " + msg[1:9] + " , Error message : " + msg[11:])
    
    sys.exit() #exits from python, program ended
    
print("Socket Bind Complete!")

s.listen(5)

print("Socket Now Listening")


def decode(string):
    new_string = string.decode(encoding = "utf-8", errors="strict")
    new_string = decrypt(new_string, shift)
    return new_string


def encode(string):
    new_string = encrypt(string, shift)
    new_string = bytes(new_string, "utf-8")
    return new_string


def password_ver(conn):
    
    print("Received a connection")
    initial = encode("Connected to server. Password Required.")
    conn.send(initial)
    pswrd = conn.recv(1024)
    
    if decode(pswrd) != key:
        response = encode("Invalid password. Try Again")
        conn.send(response)
        pswrd2 = decode(conn.recv(1024))
        
        if decode(pswrd2) != key:
            failed = encode("Invalid password. Connection Closing.")
            conn.send(failed)
            conn.close()
            
        else:
            succeeded = encode("Password Correct.")
            conn.send(succeeded)
            client_info(conn)
    else:
        succeeded = encode("Password Correct.")
        conn.send(succeeded)
        client_info(conn)


def client_info(conn):
    
    action = decode(conn.recv(1024))
    name = decode(conn.recv(1024))
    
    if action == "send":
        client_send(conn, name)
        
    elif action == "get":
        client_get(conn, name)
        
    else:
        conn.close()


def client_send(conn, name):
    
    out = open(name,"w")
    
    
    while True:
        
        data = decode(conn.recv(1024))
        out.write(data)
        
        if not data:
            print("Current Transmission Over. Closing Connection.") 
            break
        
    final = encode("File Transfer Finished! Closing Connection.")
    conn.send(final)
    conn.close()
     
     
def client_get(conn, name):
    file = open(name,"r")
    l = file.read(1024)    
    
    while l:
        try:
            conn.send(encode(l))
            l = file.read(1024)
        except socket.error:
            print("Send failed. Exiting")
            sys.exit()    
            
    conn.close()        


while 1:
    
    conn, addr = s.accept()
    _thread.start_new_thread(password_ver, (conn,))
    

s.close()