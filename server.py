from time import sleep
import threading
import logging
from websocket_server import WebsocketServer
from Tkinter import *
import json

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-15s) %(message)s')

def socketServerMessageReceived(client, server, message):
    data = json.loads(message)
    logging.debug('socketServerMessageReceived with contents: %s' % message)
    drawOval(pctX=data[0], pctY=data[1], pctSize=data[2])

def drawOval(pctX, pctY, pctSize):
    width = 1000
    height = 1000

    oX1 = width * pctX
    oY1 = height * pctY
    oX2 = oX1 + (width * pctSize)
    oY2 = oY1 + (width * pctSize)

    w.create_oval(oX1, oY1, oX2, oY2, fill='#000')
    logging.debug('drawOval: Create Oval: oX1=%s oY1=%s oX2=%s oY2=%s' % (oX1, oY1, oX2, oY2))

def socketServer():
    server = WebsocketServer(5002)
    server.set_fn_message_received(socketServerMessageReceived)
    server.run_forever()

t = threading.Thread(name='socketServer', target=socketServer)
t.setDaemon(True)
t.start()

master = Tk()
w = Canvas(master, width=1000, height=1000)
w.pack()
mainloop()
