#!/usr/bin/python

import _thread
import time
import random
import socket

# UDP server(drone status thread)
STATUS_SERVER_ADDR = "0.0.0.0"
STATUS_SERVER_PORT = 8890

DRONE_COMMAND_ADDR   = ("192.168.10.1", 8889)

BUFFER_SIZE = 1024

COMMAND_DELAY = 1

droneStatus = {
    "mid" : -100,
    "x" : -100,
    "y" : -100,
    "z" : -100,
    "h" : -100,
    "baro" : -100,
    "time" : -100,
    "agx" : -100,
    "agy" : -100,
    "agz" : -100,
    "pitch" : -100,
    "roll" : -100,
    "yaw" : -100,
    "vgx" : -100,
    "vgy" : -100,
    "vgz" : -100,
    "templ" : -100,
    "temph" : -100,
    "tof" : -100,
    "bat" : -100
}


# Define a function for the thread
def statusServer():
    global droneStatus
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind((STATUS_SERVER_ADDR, STATUS_SERVER_PORT)) 
    print("Status server is ready")

    while(True):
        try:
            recvData = server.recvfrom(BUFFER_SIZE)[0].decode("utf-8")
            # break down data in to object
            tmpParams = recvData.split(";")
            for param in tmpParams:
                pairVal = param.split(":")
                if pairVal[0] != "mpry" and len(pairVal) > 1:
                    droneStatus[pairVal[0]] = float(pairVal[1])
        except Exception as e:
            print("analyzer" + e)




def udpClient():
    global droneStatus

    COMMAND = str.encode("command")
    TAKEOFF = str.encode("takeoff")
    ENABLE_MPAD = str.encode("mon")

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def sendCommand(cmd,udpSocket):
        COMMAND_FLAG = str.encode("command")
        COMMAND = str.encode(cmd)
        try:
            print("# send COMMAND flag...")
            while True:
                udpSocket.sendto(COMMAND_FLAG, DRONE_COMMAND_ADDR)
                recvMsg = udpSocket.recvfrom(BUFFER_SIZE)[0].decode("utf-8") 
                if recvMsg == "ok":
                    print(">> OK")
                    break

            while True:
                print("# send " + cmd + " ...")
                udpSocket.sendto(COMMAND, DRONE_COMMAND_ADDR)
                recvMsg = udpSocket.recvfrom(BUFFER_SIZE)[0].decode("utf-8") 
                if recvMsg == "ok":
                    print(">> OK")
                    break
            # print(droneStatus)
        except Exception as e:
            print(e)
    

    # 制御コマンドはここから
    sendCommand("mon",UDPClientSocket)
    while droneStatus["mid"] != 5:
        time.sleep(COMMAND_DELAY)
        print(droneStatus)
        #pass
    sendCommand("moff",UDPClientSocket)
       

# Create two threads as follows
try:
   _thread.start_new_thread( statusServer, () )
   _thread.start_new_thread( udpClient, () )
except:
   print("Error: unable to start thread")

while 1:
   pass