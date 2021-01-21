#!/usr/bin/python

import _thread
import time
import random
import socket

# UDP server(drone status thread)
STATUS_SERVER_ADDR = "0.0.0.0"
STATUS_SERVER_PORT = 8890

DRONE_COMMAND_ADDR   = ("192.168.10.1", 8889)
RETRY_DELAY = 1

BUFFER_SIZE = 1024

STATUS_DISPLAY_INTERVAL = 1
MAX_RETRY = 3

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

def statusDebug():
    while True:
        time.sleep(STATUS_DISPLAY_INTERVAL)
        print("\t\t\t" + str(droneStatus))

def sendCommand(cmd,udpSocket,wait = True):
    COMMAND = str.encode(cmd)
    try:
        sendOK = False
        print("# send " + cmd + " ...")
        udpSocket.sendto(COMMAND, DRONE_COMMAND_ADDR)

        if not wait:
            return

        recvMsg = udpSocket.recvfrom(BUFFER_SIZE)[0].decode("utf-8") 
            
        while not sendOK:
            if recvMsg == "ok":
                print(">> OK")
                break
            elif recvMsg == "error":
                print(">> Error")
                break
            elif recvMsg != "":        
                print(">> " + recvMsg)
                break
            else:
                recvMsg = udpSocket.recvfrom(BUFFER_SIZE)[0].decode("utf-8") 
            time.sleep(RETRY_DELAY)
    except Exception as e:
        print(e)

def udpClient():
    global droneStatus

    COMMAND = str.encode("command")
    TAKEOFF = str.encode("takeoff")
    ENABLE_MPAD = str.encode("mon")

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    



    """ ### COMMANDS LIST ###
    mdirection x=0/1/2  [downward,foward,both]
    rc a b c d [LR,FB,UD,yaw] +-100
    takeoff
    stop
    land
    """

    # 制御コマンドはここから
    # enable dev mode
    sendCommand("command",UDPClientSocket)
    # enable mission pad
    sendCommand("mon",UDPClientSocket)
    sendCommand("mdirection 0",UDPClientSocket)
    # take off
    sendCommand("takeoff",UDPClientSocket)
    #time.sleep(COMMAND_DELAY)

    if droneStatus["mid"] != 1:
        # move left
        sendCommand("left 50",UDPClientSocket)
    if droneStatus["mid"] != 1:
        # move right
        sendCommand("right 100",UDPClientSocket)
    if droneStatus["mid"] != 1:
        sendCommand("left 50",UDPClientSocket)
    if droneStatus["mid"] != 1:
        sendCommand("foward 50",UDPClientSocket)
    if droneStatus["mid"] != 1:
        sendCommand("back 100",UDPClientSocket)

    if droneStatus["mid"] != 1:
        print("cannot find mpad 1")
    else:
        print("found mpad 1")
        sendCommand("rc 0 20 0 0",UDPClientSocket,False)
        print("Waiting for pad2")
        while droneStatus["mid"] != 2:
            pass
    print("Found mpad2")
    # turnoff rc
    sendCommand("rc 0 0 0 0",UDPClientSocket,False)
    sendCommand("land",UDPClientSocket)

    
       

def main():
    try:
        # get and update drone status obj
        _thread.start_new_thread( statusServer,())
        # msg sender thread
        _thread.start_new_thread( udpClient,())
        # print out the current drone status
        _thread.start_new_thread( statusDebug,())
    except:
        print("Error: unable to start thread")

    while 1:
        pass

if __name__ == "__main__":
    main()