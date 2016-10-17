# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 16:48:17 2016

@author: anthonyweston
"""

#create socket
import socket
import sys
from Ceaser_Cipher import encrypt, decrypt

try:
    #socket.socket() creates a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print("Failed to create socket. Error code: " + str(msg[0]) + " , Error message : " + msg[1])
    sys.exit() #exits from python, program ended
    
print("Socket Created")

server_ip = "localhost"


port = int(input("Enter port number: "))
shift = int(input("Enter Ceaser Cipher Key: "))

s.connect((server_ip,port))

print("Socket connected to " + server_ip + " on port " + str(port))


def decode(string):
    new_string = string.decode(encoding = "utf-8", errors="strict")
    new_string = decrypt(new_string, shift)
    return new_string


def encode(string):
    new_string = encrypt(string, shift)
    new_string = bytes(new_string, "utf-8")
    return new_string


def password_ver(s):
    print(decode(s.recv(1024)))
    pswrd = encode("Enter server password: ")
    s.send(pswrd)
    
    response = decode(s.recv(1024))

    if response == "Password Correct.":
        print(response)
        send_info(s)
    else:
        print(response)
        pswrd2 = encode("Enter server password: ")
        s.send(pswrd2)
        response = decode(s.recv(1024))
        
        if response == "Password Correct.":
            print(response)
            send_info(s)
        else:
            print(response)
            s.close()
            sys.exit()
        

def send_info(s):
    
    action = encode("Would you like to send (type send) or get (type get) a file? ")
    s.send(action)
    
    old_name = input("What is the name of the file to be copied? ")
    
    new_name = input("What is the name of the file to be created? ")
    
    
    if decode(action) == "get":
        s.send(encode(old_name)
        receive_file(s, str(new_name))
        
    elif decode(action) == "send":
        s.send(encode(new_name))
        send_file(s, str(old_name))

    else:
        s.close()
        sys.exit()


#f = str(input("Please enter the full path of the file you want to send: "))


def send_file(s, cs_name):
    
    to_send = open(cs_name,'r')
    l = to_send.read(1024)
    print("Sending File Contents...")

    while True:
        try:
            s.send(encode(l))
            l = to_send.read(1024)
            
        except socket.error:
            print("Send failed. Exiting")
            sys.exit()
            
        if len(l) < 1:
                s.shutdown(socket.SHUT_WR)
                break

    

    final = decode(s.recv(1024))

    to_send.close()
    print(final)
    
    s.close()
    sys.exit()
    
    
def receive_file(s, cs_name):

#    print(decode(s.recv(1024)))
    
    f = open(cs_name,"w")
    
    while True:
        data = decode(s.recv(1024))
        
        f.write(data)        
        
        if not data:
            break    
        
    print("File Transfer complete. Closing Connection.")
    s.close()
    sys.exit()


password_ver(s)