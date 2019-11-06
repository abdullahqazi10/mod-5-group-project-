#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM, gethostname, gethostbyname
from _thread import *
import sys
# import view.ViewTUI as ui
import GUI

TUI = 0
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER=0

"""
handle messages starting with 'SYS'
"""
def server_output( msg):
    GUI.server_msg(msg)

"""
handle messages starting with 'MSG'
"""
def client_output( msg):
    GUI.receive(msg)

"""
listen to certain port for 1 connection
"""
def accept_con( ):
    global SERVER
    #allows for exactly one connection
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(1)

    server_output("listening")
    while True:
        client, client_address = SERVER.accept()
        server_output("%s:%s has connected." % client_address)
        client.send(bytes("SYSyou are connected to " + gethostname(), "utf8"))
        handle_client(client)
        break

"""
start reading from connection (different thread)
  and reading from (cmd)input
"""
def handle_client(client):
    #reads input
    start_new_thread(receive, (client, ))
    #listens to connection in parallel thread

    readData(client)


"""
start listening to socket indefinitely, untill quit or empty
"""
def receive( socket):
    GUI.opendisplay()


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
            elif  str(msg)[:5] == "b'MSG":
                client_output(msg.decode("utf8")[3:])
                pass
            else:
                GUI.video(msg)
                # if (str(msg) != "b'{quit}'"):
                #     client_output(msg.decode("utf8"))
                # else:
                #     server_output("other disconnected")
                #     disconnect(socket)
                #     break
        except OSError as e:  # Possibly other has left the chat.
            server_output("receive(): disconnected error")
            print(e)
            break

    sys.exit()

"""
send message on socket
"""
def send( msg):#replaced socket with caller

    CALLER.send(bytes(msg, "utf8"))

def disconnect( socket):
    socket.close()

"""
connect to target IP, keeps going till connected
"""
def connect(target):
    going = 1
    while going:
        HOST = ui.f_input('Enter server IP: ')
        PORT = ui.f_input('Enter server port: ')
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
let GUI connect
"""
def connect2(addr):
    target = socket(AF_INET, SOCK_STREAM)
    try:
        target.connect(addr)
    except OSError:
        server_output("network not accepted, try another")
        return -1
    try:
        #start reading in seperate thread
        start_new_thread( receive, (target, ))
    except Exception as e:
        print(e)
        return -1
    readData(target)
    # start_new_thread(receive, (target, ))
    return 1

"""
read imput from commandline
"""
CALLER = 0
def readData(client):
    global CALLER
    CALLER = client
    while TUI:
        if data_input_handler("") == -1:
            break
    if TUI:
        server_output("disconnected")

"""
send data from input to socket
"""
def data_input_handler( msg):
    try:
        if TUI:
            msg = ui.f_input(">")
        if msg == "{quit}":
            server_output("disconnecting...")
            send("SYS{quit}", CALLER)
            disconnect(CALLER)
            return -1
        print("gona send it anyway")
        send("MSG"+msg, CALLER)

    except KeyboardInterrupt:
        try:
            send("SYS{quit}", CALLER)
            disconnect(CALLER)
        except:
            pass
        return -1
    send(msg, CALLER)

def record(client):

    print("recording")
    connection=CALLER.makefile('wb')
    camera=picamera.PiCamera()
    # try:
    camera.resolution = (640, 480)
    camera.framerate = 24
        # a=open("a", 'w+')
    camera.start_preview()
    time.sleep(2)
    camera.start_recording(connection,format='h264')
    while True:
        camera.wait_recording(30)
    camera.stop_recording()

"""
main thread, sets client to calling or recieving
"""
# while 1:
#     try:
#         choice = ui.f_input("what to do? 1=connect, 2=listen, 3=die")
#         if choice == "1":
#             target = 0
#             connect(target)
#         elif choice == "2":
#
#             # start_new_thread( accept_con, ())
#             accept_con()
#         elif choice == "3":
#             sys.exit()
#             break
#     except KeyboardInterrupt:
#         server_output("Shutting down")
#         break
#
# """
# do nothing until all threads are finished
# """
# while 1:
#     pass
