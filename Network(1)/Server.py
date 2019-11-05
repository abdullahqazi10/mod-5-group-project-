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

"""
allows for 5 people to connect
Sends the received socket to handle_client
to multithread it
"""
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("SYSYou are connected to the server", "utf8"))
        start_new_thread( handle_client, (client, ))
        global client_list
        client_list.append(client)

"""
Connects caller to target in connect()
allows caller to stop connecting
connect() will multithread receiving the messages
  from the target
handle_client() will receive the messages from the
  caller
"""
def handle_client(client):  # Takes client socket as argument.
    try:
        target = socket(AF_INET, SOCK_STREAM)
        if connect(client, target) == -1:
            print("stopped exetution by client")
            client.close()
            client_list.remove(client)
            return
    except Exception as e:
        print(e)
        client.close()
        return
    
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8") and str(msg) != "b''":
            try:
                print("caller " + str(msg))
                send_to( msg, target)
            except Exception as e:
                send_to(bytes("error", "utf8"), client)
                print(e)
        else:
            try:
                send_to(bytes("SYS{quit}", "utf8"), target)
                client.close()
                client_list.remove(client)
            except:
                print("disconnection is a bit messy")
                break
            break

"""
send msg on socket
"""
def send_to( msg, socket):
    socket.send(msg)

"""
send messages to caller to get the destination
  IP address and port number
allows the caller to stop connecting
returns ADDR
"""
def input_destination( client):
    request = 'SYSplease enter destination IP or next server ip'
    client.send(bytes(request, "utf8"))
    ipadd = client.recv(BUFSIZ).decode("utf8")
    if ipadd == "{quit}":
        print("stop")
        return -1
    request = 'SYSplease enter destination PORT'
    client.send(bytes(request, "utf8"))
    portadd = int(client.recv(BUFSIZ).decode("utf8"))
    print("connect to  " + ipadd + ":" + str(portadd))
    return (ipadd, portadd)

"""
Connects caller to target:
requests destination from caller using input_destination
starts new thread to receive messages from target
if target is unreachable, send message to caller and
  request destination again
"""
def connect( caller, target):
    while 1:
        try:
            ADDR = input_destination(caller)
            if ADDR == -1:
                return -1
            target.connect(ADDR)
            global client_list
            client_list.append(target)
            start_new_thread( receive, (target, caller ))
            return 1
        except Exception as e:
            print(e)
            send_to(bytes("network unreachable", "utf8"), caller)

"""
listens to the socket of target
sends all messages immediately to caller
on connection failure, send {quit} messaget to
  caller
"""
def receive(target, caller):
    while True:
        try:
            msg = target.recv(BUFSIZ)
            if str(msg) == "b'SYS{quit}'" or str(msg) == "b''":
                print("connection to target failed")
                client_list.remove(target)
                if caller in client_list:
                    send_to( bytes("SYS{quit}", "utf8"), caller)
                    caller.close()
                    client_list.remove(caller)
                break
            print("target " + str(msg))
            if caller in client_list:
                send_to( msg, caller)
        except OSError as e:  # Possibly client has left the chat.
            print(e)
            break

"""
stop the server, stop listening to port
stop all active connections
"""
def shutdown():
    print("server shutdown")
    SERVER.close()
    for sock in client_list:
        sock.close()

"""
main function
"""
if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    start_new_thread(accept_incoming_connections, ())

"""
do nothing until all threads are stopped
on shutdown (^C) shut down server correctly
"""
while 1:
    try:
        pass
    except KeyboardInterrupt as e:
        print(e)
        shutdown()
        break
    

