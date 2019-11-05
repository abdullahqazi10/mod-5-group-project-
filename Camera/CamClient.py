#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from _thread import *
import picamera
import time

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
address = 0
deact = 0
connection = 0
def accept_con( ):
    #allows for exactly one

    print("listening")
    while True:
        global address, caller,connection
        client, client_address = SERVER.accept()

        connection =client.makefile('wb')
        print("%s:%s has connected." % client_address)
        client.send(bytes("hello", "utf8"))
        address = client_address
        # start_new_thread( handle_client, (client, ))
        handle_client(client)
        break


def handle_client(client):  # Takes client socket as argument.
    #listener thread
    start_new_thread(readData, (client, ))
    receive(client)


def receive( socket):
    """Handles receiving of messages"""
    while True:
        try:
            msg = socket.recv(BUFSIZ).decode("utf8")
            if (msg ==  "" or msg == "{quit}"):# and #not(deact):
              print("other disconnected")
              disconnect(socket)
              break
            # elif deact:
            #   break
            print(msg)
        except OSError:  # Possibly other has left the chat.
            print("receive(): disconnected error")
            break


def send( msg, socket):
    #socket.send(bytes(msg, "utf8"))
    socket.send((msg))
    if msg == "{quit}":
        socket.close()

def disconnect( socket):
    socket.close()

def connect(target):
  global connection
  HOST = input('Enter server IP: ')
  PORT = input('Enter server port: ')
  if not PORT:
      PORT = 33000  # Default value.
  else:
      PORT = int(PORT)
  BUFSIZ = 1024
  ADDR = (HOST, PORT)
  target = socket(AF_INET, SOCK_STREAM)
  target.connect(ADDR)
  connection=target.makefile('wb')
  try:
    #start reading in seperate thread
    start_new_thread( receive, (target, ))
  except Exception as e:
    print(e)
  #start writing in this thread
  readData(target)

def readData(client):
    camera=picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(2)
    camera.start_recording(connection, format='h264', quality=23)
    while camera.recording:
         pass
      # camera.wait_recording(30)

        # val = input(">")
        # camera.wait_recording(30)
        # send(val, client)
        # if val == "{quit}":
        #   global deact
        #   deact=1
        #   print("disconnecting...")
        #   disconnect(client)
        #   break

      # print("disconnected")



while 1:
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

while 1:
  pass
