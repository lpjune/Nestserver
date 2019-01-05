#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
from tkinter import *
import libclient
from tkinter import messagebox

def kill():
    top.destroy()
    quit()

top = Tk()
defaultc = "command"
bottle = "waiting..."

while True:
    
    sel = selectors.DefaultSelector()
    def create_request(action, value):
        if action == "search":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=value),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(action + value, encoding="utf-8"),
            )


    def start_connection(host, port, request):
        addr = (host, port)
        #print("starting connection to", addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = libclient.Message(sel, sock, addr, request)
        sel.register(sock, events, data=message)

    #Host
    L1 = Label(top, text="Host")
    L1.grid(row=0, column=0)
    E1 = Entry(top, bd = 5)
    E1.insert(END, '130.18.64.135')
    E1.grid(row=0, column=1)

    #Port
    L2 = Label(top, text="Port")
    L2.grid(row=1, column=0)
    E2 = Entry(top, bd = 5)
    E2.insert(END, '65432')
    E2.grid(row=1, column=1)

    #Action
    E3 = "search"

    #Command
    L4 = Label(top, text="Command")
    L4.grid(row=2, column=0)
    E4 = Entry(top, bd = 5)
    E4.insert(END, defaultc)
    E4.grid(row=2, column=1)

    #Activity
    L5 = Label(top, text=bottle)
    L5.grid(row=3,column=1)

    var = IntVar()
    button = Button(top, text="Submit", command=lambda: var.set(1))
    button.grid(row=4, column=1)

    exitb = Button(top, text="Exit", command=kill)
    exitb.grid(row=5, column=2)

    button.wait_variable(var)

    #assignments
    host = E1.get()

    E2 = E2.get()
    port = int(E2)

    action = E3

    value = E4.get()
    defaultc = value
    
    request = create_request(action, value)
    start_connection(host, port, request)
    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    bottle = message.process_events(mask)
                except Exception:
                    #print(
                        #"main: error: exception for",
                        #f"{message.addr}:\n{traceback.format_exc()}",
                    #)
                    #messagebox.showinfo("Error","Traceback Error")
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        #print("caught keyboard interrupt, exiting")
        messagebox.showinfo("Error","Caught keyboard interrupt")
    finally:
        sel.close()

    L5.destroy()


top.mainloop()
