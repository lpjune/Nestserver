#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
from tkinter import *
import libserver




top = Tk()
top.title('Server')

def kill():
    top.destroy()
    quit()



sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)

L1 = Label(top, text="Server")
L1.grid(row=0, column=0)
E1 = Entry(top, bd = 5)
E1.insert(END, '130.18.64.135')
E1.grid(row=0, column=1)

L2 = Label(top, text="Port")
L2.grid(row=1, column=0)
E2 = Entry(top, bd = 5)
E2.insert(END, '65432')
E2.grid(row=1, column=1)

var = IntVar()
button = Button(top, text="Submit", command=lambda: var.set(1))
button.grid(row=4, column=1)

exitb = Button(top, text="Exit", command=kill)
exitb.grid(row=5, column=2)

button.wait_variable(var)

host, port = E1.get(), int(E2.get())
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

top.destroy()

try:
    while True:            
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()


top.mainloop()
