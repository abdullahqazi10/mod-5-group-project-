import tkinter as tk
from tkinter import *
import socket
import pdb
import vlc
import socket
import time

import sys
import Client


HEIGHT = 800
WIDTH = 800

root = tk.Tk()  # root window to place everything into

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='#00AFF0')
canvas.pack()

frame = tk.Frame(root, bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

portentry = tk.Entry(frame, font=40, text='Enter port number')
portentry.place(relwidth=0.65, relheight=1)



# instruction = tk.Text(canvas)
# instruction.place(relx=0.15, rely=0.01,relwidth=0.2, relheight=0.05)
#
# instruction.insert("end", "Enter port number\n")
# instruction.state(DISABLED)

buttonc= tk.Button(root, text="Send", font=40, command= lambda: send(textentry.get()))  # passing button to frame
buttonc.place(relx=0.2, anchor='s',relheight=0.05,relwidth=0.1)


message_frame = tk.Frame(root)
message_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

textentry= tk.Entry(root, font=40, text='write message Here')
textentry.place(relx=0.5, rely=0.85,relwidth=0.55, relheight=0.05, anchor='n')



buttonc= tk.Button(frame, text="Connect", font=40, bg='green', command= lambda: sconnect(portentry.get())) # passing button to frame
buttonc.pack(side=RIGHT)

buttond=tk.Button(frame, text="Disconnect", font=40, bg= 'red', command= lambda: disconnectb())
buttond.pack(side=RIGHT)

def sconnect(portentry):
    print("Button clicked")
    host =' 130.89.88.1'
    s=socket.socket()
    port = portentry.get()
    print(" Attempting to connect to" + port)
    s.connect(('IP',port))

def disconnectb():  #when disconnect ic clicked
    print("Closing connection")
    s.close()
    print("Client disconnected")

root.mainloop()  # run function
