#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from _thread import *
import sys

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
address = 0
deact = 0

output_file = open("output.h264", 'wb')

def server_output( msg):
    print(msg)

def append_file( msg):
    output_file.write(msg)
    output_file.flush()

def accept_con( ):
    #allows for exactly one connection
    server_output("listening")
    while True:
        global address, caller
        client, client_address = SERVER.accept()
        server_output("%s:%s has connected." % client_address)
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

def file_reader( target):
    f = open('output.h264','rb')
    print('Sending...')
    l = f.read(1024)
    while (l):
        print 'Sending...'
        target.send(l)
        l = f.read(1024)
    f.close()

""" start listening to socket indefinitely, untill quit or empty"""
def receive( socket):
    while True:
        try:
            msg = socket.recv(BUFSIZ)
            if str(msg)[:5] == "b'SYS" or str(msg) == "b''":
                msg = msg.decode("utf8")
                server_output(msg[3:])
                if (msg ==  "" or msg == "SYS{quit}"):
                    server_output("other disconnected")
                    disconnect(socket)
                    break
            elif str(msg)[:5] == "b'MSG'":
                #server_output(msg)
                pass
            else:
                append_file(msg)
        except OSError as e:  # Possibly other has left the chat.
            server_output("receive(): disconnected error")
            print(e)
            break
    output_file.close()

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
            server_output("network not accepted, try another")
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
  if 0:
    while 1:
        try:
            val = input(">")
            send(val, client)
            if val == "{quit}":
                global deact
                deact=1
                server_output("disconnecting...")
                disconnect(client)
                break
        except KeyboardInterrupt:
            send("{quit}", client)
            disconnect(client)
            break
    server_output("disconnected")
    sys.exit()
  else:
    file_reader(client)
    
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
        server_output("Shutting down")
        sys.exit()
while 1:
    pass
