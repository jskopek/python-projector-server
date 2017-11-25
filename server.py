from time import sleep
import threading
import logging
from websocket_server import WebsocketServer
from Tkinter import *
import json

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-15s) %(message)s')

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad=3
        self._geom='200x200+0+0'
        master.geometry('{0}x{1}+0+0'.format(
            master.winfo_screenwidth()-pad,master.winfo_screenheight()-pad))
        master.bind('<Escape>', self.toggle_geom)
    def toggle_geom(self, event):
        geom=self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom=geom


def socketServerMessageReceived(client, server, message):
    data = json.loads(message)
    logging.debug('socketServerMessageReceived with contents: %s' % message)
    drawOval(master, canvas, pctX=data[0], pctY=data[1], pctSize=data[2])

def drawOval(master, canvas, pctX, pctY, pctSize):
    width = master.winfo_screenwidth()
    height = master.winfo_screenheight()

    oX1 = width * pctX
    oY1 = height * pctY
    oX2 = oX1 + (width * pctSize)
    oY2 = oY1 + (width * pctSize)

    canvas.create_oval(oX1, oY1, oX2, oY2, fill='#000')
    logging.debug('drawOval: Create Oval: oX1=%s oY1=%s oX2=%s oY2=%s' % (oX1, oY1, oX2, oY2))

def socketServer():
    server = WebsocketServer(5002)
    server.set_fn_message_received(socketServerMessageReceived)
    server.run_forever()

t = threading.Thread(name='socketServer', target=socketServer)
t.setDaemon(True)
t.start()

master = Tk()
app = FullScreenApp(master)
canvas = Canvas(master, width=master.winfo_screenwidth(), height=master.winfo_screenheight())
canvas.pack()
mainloop()
