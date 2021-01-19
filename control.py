#!/usr/bin/python

import _thread
import time
import random
import socket

# UDP server(drone status thread)
STATUS_SERVER_ADDR = "192.168.10.2"
STATUS_SERVER_PORT = 8890

RESPONSE_SERVER_ADDR = "192.168.10.2"
RESPONSE_SERVERPORT = 9999

BUFFER_SIZE = 1024

DRONE_COMMAND_ADDR   = ("192.168.10.1", 8889)

# UDP client for command parsing

statusMsg = ""
responseMsg = ""

# Define a function for the thread
def statusServer():
    global statusMsg
    server = socket.socket() 
    server.bind((STATUS_SERVER_ADDR, STATUS_SERVER_PORT)) 
    server.listen(4) 
    client_socket, client_address = server.accept()
    print(client_address, "has connected")
    print("Status server is ready")

    while(True):
        recvieved_data = client_socket.recv(BUFFER_SIZE)
        print("Status " + recvieved_data)

def responseServer():
    global responseMsg
    server = socket.socket() 
    server.bind((RESPONSE_SERVER_ADDR, RESPONSE_SERVERPORT)) 
    server.listen(4) 
    client_socket, client_address = server.accept()
    print(client_address, "has connected")
    print("Response server is ready")

    while(True):
        recvieved_data = client_socket.recv(BUFFER_SIZE)
        print("Response " + recvieved_data)




def udpClient():
    global statusMsg
    global responseMsg

    COMMAND = str.encode("command")
    TAKEOFF = str.encode("takeoff")

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    

    delay = 5
    count = 0
    while count < 5:
        print("Sending command...")
        time.sleep(delay)
        count += 1
        UDPClientSocket.sendto(COMMAND, DRONE_COMMAND_ADDR)
        msgFromServer = UDPClientSocket.recvfrom(BUFFER_SIZE)
        time.sleep(1)
        UDPClientSocket.sendto(TAKEOFF, DRONE_COMMAND_ADDR)

# Create two threads as follows
try:
   _thread.start_new_thread( statusServer, () )
   _thread.start_new_thread( responseServer, () )
   _thread.start_new_thread( udpClient, () )
except:
   print("Error: unable to start thread")

while 1:
   pass