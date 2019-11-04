#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from _thread import *

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
address = 0
deact = 0

def accept_con( ):
    #allows for exactly one connection
    print("listening")
    while True:
        global address, caller
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("hello", "utf8"))
        address = client_address
        # start_new_thread( handle_client, (client, ))
        handle_client(client)
        break

""" start reading from connection and reading from (cmd) input"""
def handle_client(client):
    #listens to connection in parallel thread
    start_new_thread(readData, (client, ))
    #reads input
    receive(client)
    
""" start listening to socket indefinitely, untill quit or empty"""
def receive( socket):
    while True:
        try:
            msg = socket.recv(BUFSIZ).decode("utf8")
            if (msg ==  "" or msg == "{quit}"):# and #not(deact):
                print("other disconnected")
                disconnect(socket)
                break
            # elif deact:
            #     break
            print(msg)
        except OSError:  # Possibly other has left the chat.
            print("receive(): disconnected error")
            break

""" send message on socket"""
def send( msg, socket):
    socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        socket.close()

def disconnect( socket):
    socket.close()

""" connect to target IP, keeps going till connected"""
def connect(target):
    going = 1
    while going:
        HOST = input('Enter server IP: ')
        PORT = input('Enter server port: ')
        if not PORT:
            PORT = 33000  # Default value.
        else:
            PORT = int(PORT)
        BUFSIZ = 1024
        ADDR = (HOST, PORT)
        target = socket(AF_INET, SOCK_STREAM)
        try:
            target.connect(ADDR)
        except OSError:
            print("network not accepted, try another")
            continue
        try:
            #start reading in seperate thread
            start_new_thread( receive, (target, ))
        except Exception as e:
            print(e)
        #start writing in this thread
        going = 0
        readData(target)

""" read imput from commandline"""
def readData(client):
    while 1:
        try:
            val = input(">")
            send(val, client)
            if val == "{quit}":
                global deact
                deact=1
                print("disconnecting...")
                disconnect(client)
                break
        except KeyboardInterrupt:
            send("{quit}", client)
            disconnect(client)
            break
    print("disconnected")
""" main thread, sets client to calling or recieving"""
while 1:
    try:
        choice = input("what to do? 1=connect, 2=listen, 3=die")
        if choice == "1":
            target=0
            connect(target)
        elif choice == "2":
            SERVER.bind(ADDR)
            SERVER.listen(1)
            # start_new_thread( accept_con, ())
            accept_con()
        elif choice == "3":
            break
    except KeyboardInterrupt:
        print("Shutting down")
        break
while 1:
    pass
