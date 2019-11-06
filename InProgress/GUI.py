import tkinter as tk
from tkinter import *
import socket
import pdb
import vlc
import socket
import time
import subprocess
import sys
import Client as c



HEIGHT = 800
WIDTH = 800
# player=0
root = tk.Tk()  # root window to place everything into
port =-1
ip=-1
cmdline = ['mplayer', '-fps', '25',  '1024', '-']
player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='#00AFF0')
canvas.pack()

frame = tk.Frame(root, bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

portentry = tk.Entry(frame, font=40, text='Enter port number')
portentry.place(relwidth=0.65, relheight=1)



# instruction = tk.Text(frame, state=DISABLED)
# instruction.place(relx=0.15, rely=0.01,relwidth=0.2, relheight=0.05)
#
# instruction.insert("end", "Enter port number\n")


buttonc= tk.Button(root, text="Send", font=40, command= lambda: send())  # passing button to frame
buttonc.place(x = 640,y = 606)



message_frame = tk.Frame(root)
message_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

textentry= tk.Entry(root, font=40, text='write message Here')
textentry.place(relx=0.5, rely=0.85,relwidth=0.55, relheight=0.05, anchor='n')

buttonl=tk.Button(frame, text="Listen", font=40, bg= 'yellow', command= lambda: listen())
buttonl.pack(side=RIGHT)

buttonc= tk.Button(frame, text="Connect", font=40, bg='green', command= lambda: sconnect()) # passing button to frame
buttonc.pack(side=RIGHT)
v = StringVar()

textfield=tk.Label(message_frame, font=40,textvariable=v )


textfield.place(relwidth=1, relheight=1)
# textfield.insert("end","Enter port number in the connect field!\n")
v.set(v.get()+"Enter Ip number in the connect field!\n")


buttond=tk.Button(frame, text="Disconnect", font=40, bg= 'red', command= lambda: disconnectb())
buttond.pack(side=RIGHT)

def opendisplay():

    # cmdline = ['vlc', '--demux', 'h264', '-']
    cmdline = ['mplayer', '-fps', '25',  '1024', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)

def receive(msg):
    v.set(v.get()+msg+"\n")

def send():
    msg=textentry.get()
    c.send(msg)

def video(data):
    player.stdin.write(data)


def server_msg(msg):

    v.set(v.get()+"Server:"+ msg +"\n")

def sconnect():
    global port, ip
    input=portentry.get()
    if(ip==-1):
        ip=portentry.get()
        portentry.delete(0,'end')
        v.set(v.get()+"Input the port address\n" )
    else:
        port=int(portentry.get())
        portentry.delete(0,'end')
        v.set(v.get()+"Wait for instrcution from server\n" )

        if(c.connect2((ip,port))!=-1):
            pass
        else:
            port=-1
            ip=-1



def listen():
    c.accept_con()

def disconnectb():  #when disconnect ic clicked
    port=-1
    ip=-1
    print("Closing connection")
    s.close()
    print("Client disconnected")

root.mainloop()  # run function
