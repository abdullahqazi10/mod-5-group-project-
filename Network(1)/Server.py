#!/usr/bin/env python3

from socket import *
from _thread import *
import time

clients = {}
addresses = {}

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
        client.send(bytes("Greetings from the cave!"+
                          "Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        start_new_thread( handle_client, (client, ))

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    request = 'Welcome %s! please enter destination IP' % name
    client.send(bytes(request, "utf8"))
    ipadd = client.recv(BUFSIZ).decode("utf8")
    request = 'please enter destination PORT'
    client.send(bytes(request, "utf8"))
    portadd = int(client.recv(BUFSIZ).decode("utf8"))
    print(ipadd + ":" + str(portadd));
    #connect to the requested host
    target = socket(AF_INET, SOCK_STREAM)
    start_new_thread( connect,  (ipadd, portadd, client, target))
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
            del clients[client]
            break

def send_to( msg, socket):
    socket.send(msg)

"""
def send_to_init(msg):  # prefix is for name identification.
    for sock in clients:
        sock.send(msg)

def send_to_other( msg):
    client_socket.send(msg)

client_socket=0
"""

def connect( HOST, PORT, caller, target):
  ADDR = (HOST, PORT)
  #client_socket  = socket(AF_INET, SOCK_STREAM)
  #client_socket.connect(ADDR)
  target.connect(ADDR)
  try:
    start_new_thread( receive, (target, caller ))
  except Exception as e:
    print(e)

def receive(target, caller):
    """Handles receiving of messages."""
    while True:
        try:
            #Receive messages from other and send to caller
            msg = target.recv(BUFSIZ)
            print("target " + str(msg))
            send_to( msg, caller)
        except OSError as e:  # Possibly client has left the chat.
            print(e)
            break

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    start_new_thread(accept_incoming_connections, ())

while 1:
    pass

SERVER.close()
