#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from _thread import *
import sys
from view.ViewTUI import *

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)

"""
handle messages starting with 'SYS'
"""
def server_output( msg):
    f_output_server(msg)

"""
handle chat messages
"""  
def client_output( msg):
    f_output_client(msg)

"""
listen to certain port for 1 connection
"""
def accept_con( ):
    #allows for exactly one connection
    server_output("listening")
    while True:
        client, client_address = SERVER.accept()
        server_output("%s:%s has connected." % client_address)
        client.send(bytes("hello", "utf8"))
        handle_client(client)
        break

"""
start reading from connection (different thread)
  and reading from (cmd)input
"""
def handle_client(client):
    #reads input
    start_new_thread(readData, (client, ))
    #listens to connection in parallel thread
    receive(client)

"""
start listening to socket indefinitely, untill quit or empty
"""
def receive( socket):
    while True:
        try:
            msg = socket.recv(BUFSIZ)
            if str(msg)[:5] == "b'SYS" or str(msg) == "b''":
                msg = msg.decode("utf8")
                server_output(msg[3:])
                if (msg ==  "" or msg == "SYS{quit}"):
                    server_output("other disconnected, ^C to return to menu")
                    disconnect(socket)
                    break
            elif str(msg)[:5] == "b'MSG'":
                #server_output(msg)
                pass
            else:
                #append_file(msg)
                if (msg != "{quit}"):
                    client_output(msg)
        except OSError as e:  # Possibly other has left the chat.
            server_output("receive(): disconnected error")
            print(e)
            break
            
    sys.exit()

"""
send message on socket
"""
def send( msg, socket):
    socket.send(bytes(msg, "utf8"))

def disconnect( socket):
    socket.close()

"""
connect to target IP, keeps going till connected
"""
def connect(target):
    going = 1
    while going:
        HOST = f_input('Enter server IP: ')
        PORT = f_input('Enter server port: ')
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

"""
read imput from commandline
"""
def readData(client):
    while 1:
        try:
            val = f_input(">")
            send(val, client)
            if val == "{quit}":
                server_output("disconnecting...")
                disconnect(client)
                break
        except KeyboardInterrupt:
            try:
                send("{quit}", client)
                disconnect(client)
            except:
                pass
            break
    server_output("disconnected")
    
"""
main thread, sets client to calling or recieving
"""
while 1:
    try:
        choice = f_input("what to do? 1=connect, 2=listen, 3=die")
        if choice == "1":
            target=0
            connect(target)
        elif choice == "2":
            SERVER.bind(ADDR)
            SERVER.listen(1)
            # start_new_thread( accept_con, ())
            accept_con()
        elif choice == "3":
            sys.exit()
            break
    except KeyboardInterrupt:
        server_output("Shutting down")
        break

"""
do nothing until all threads are finished
"""
while 1:
    pass
