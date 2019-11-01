#!/usr/bin/env python3

from socket import *
from _thread import *
import time

client_list = []
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("You are connected to the server", "utf8"))
        start_new_thread( handle_client, (client, ))
        global client_list
        client_list.append(client)

def handle_client(client):  # Takes client socket as argument.
    try:
        """Handles a single client connection."""
        #successfull connection
        #connect to the requested host
        target = socket(AF_INET, SOCK_STREAM)
        if connect(client, target) == -1:
            print("stopped exetution by client")
            #send_to(bytes("{quit}", "utf8"), client)
            client.close()
            client_list.remove(client)
            return
    except Exception as e:
        print(e)
        client.close()
        return
    
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            try:
                print("caller " + str(msg))
                send_to( msg, target)
            except Exception as e:
                send_to(bytes("error", "utf8"), client)
                print(e)
        else:
            send_to(bytes("{quit}", "utf8"), target)
            client.close()
            break

def send_to( msg, socket):
    socket.send(msg)

def input_destination(client):
    request = 'please enter destination IP or next server ip'
    client.send(bytes(request, "utf8"))
    ipadd = client.recv(BUFSIZ).decode("utf8")
    if ipadd == "{quit}":
        print("stop")
        return -1
    request = 'please enter destination PORT'
    client.send(bytes(request, "utf8"))
    portadd = int(client.recv(BUFSIZ).decode("utf8"))
    print("connect to  " + ipadd + ":" + str(portadd))
    return (ipadd, portadd)

def connect( caller, target):
    while 1:
        try:
            ADDR = input_destination(caller)
            if ADDR == -1:
                return -1
            target.connect(ADDR)
            global client_list
            client_list.add(target)
            start_new_thread( receive, (target, caller ))
            return 1
        except Exception as e:
            print(e)
            send_to(bytes("network unreachable", "utf8"), caller)


def receive(target, caller):
    """Handles receiving of messages."""
    while True:
        try:
            #Receive messages from other and send to caller
            msg = target.recv(BUFSIZ)
            if msg.decode("utf8") == "{quit}" or str(msg) == "b''":
                print("connection to target failed")
                target.close()
                client_list.remove(target)
            print("target " + str(msg))
            send_to( msg, caller)
        except OSError as e:  # Possibly client has left the chat.
            print(e)
            break

def shutdown():
    print("server shutdown")
    SERVER.close()
    for sock in client_list:
        sock.close()
    

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    start_new_thread(accept_incoming_connections, ())

while 1:
    try:
        input("")
    except KeyboardInterrupt as e:
        print(e)
        shutdown()
        break
    

