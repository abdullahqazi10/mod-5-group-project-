import tkinter as tk
from tkinter import *
import socket
import pdb
import socket
import time
import subprocess
import sys
import Client as c
from _thread import *


HEIGHT = 800
WIDTH = 800
# player=0
root = tk.Tk()  # root window to place everything into
port =-1
ip=-1
# cmdline = ['mplayer', '-fps', '25',  '1024', '-']
# player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
player=0
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='#00AFF0')
canvas.pack()

frame = tk.Frame(root, bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

portentry = tk.Entry(frame, font=40, text='Enter port number')
portentry.place(relwidth=0.65, relheight=1)

def server_msg(msg):
    #v.set(v.get()+"Server:"+ msg +"\n")
    textfield.config(state=NORMAL)
    textfield.insert(END, "Server: " + msg + "\n", 'bluecolor')
    textfield.see(END)
    textfield.config(state=DISABLED)

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

textfield = Text(message_frame, height=50, width=90, state=DISABLED)
scroll=Scrollbar(message_frame)
scroll.config(command=textfield.yview)
textfield.configure(yscrollcommand=scroll.set)
textfield.pack(side=LEFT)
scroll.pack(side=RIGHT, fill=Y)


textfield.place(relwidth=1, relheight=1)
# textfield.insert("end","Enter port number in the connect field!\n")
server_msg("enter Ip number in the connect field!\n")


buttond=tk.Button(frame, text="Disconnect", font=40, bg= 'red', command= lambda: disconnectb())
buttond.pack(side=RIGHT)

def opendisplay():
    global player
    # cmdline = ['vlc', '--demux', 'h264', '-']
    cmdline = ['mplayer', '-fps', '25',  '1024', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)

def receive(msg):
    #v.set(v.get()+msg+"\n")
    textfield.config(state=NORMAL)
    textfield.insert(END, msg+"\n", 'greencolor')
    textfield.see(END)
    textfield.config(state=DISABLED)

def send():
    msg=textentry.get()
    c.send(msg)

def video(data):
    global player
    player.stdin.write(data)




def sconnect():
    global port, ip
    input=portentry.get()
    if(ip==-1):
        ip=portentry.get()
        portentry.delete(0,'end')
        server_msg("Input the port address\n" )
    else:
        port=int(portentry.get())
        portentry.delete(0,'end')
        server_msg("Wait for instrcution from server\n" )

        if(c.connect2((ip,port))!=-1):
            pass
        else:
            port=-1
            ip=-1



def listen():
    start_new_thread(c.accept_con,())
    receive("Listening.")

def stopPlayer():
    global player
    player.terminate()

def disconnectb():  #when disconnect ic clicked
    port=-1
    ip=-1
    print("Closing connection")
    c.disconnect2()
    stopPlayer()
    print("Client disconnected")

root.mainloop()  # run function
