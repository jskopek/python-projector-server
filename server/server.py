from time import sleep
import threading
import logging
from websocket_server import WebsocketServer
from utils import FullScreenApp
from Tkinter import *
import json

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-15s) %(message)s')

class Painter(object):
    def __init__(self, **kwargs):
        self.master = Tk()
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()

        self.fullscreen_manager = FullScreenApp(self.master)
        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()

    def draw_oval(self, pctX, pctY, pctSize):
        oX1 = self.width * pctX
        oY1 = self.height * pctY
        oX2 = oX1 + (self.width * pctSize)
        oY2 = oY1 + (self.width * pctSize)

        self.canvas.create_oval(oX1, oY1, oX2, oY2, fill='#000')
        logging.debug('drawOval: Create Oval: oX1=%s oY1=%s oX2=%s oY2=%s' % (oX1, oY1, oX2, oY2))

    def start(self):
        mainloop()


def socketServerMessageReceived(client, server, message):
    data = json.loads(message)
    logging.debug('socketServerMessageReceived with contents: %s' % message)
    painter.draw_oval(pctX=data[0], pctY=data[1], pctSize=data[2])

def socketServer():
    server = WebsocketServer(5002)
    server.set_fn_message_received(socketServerMessageReceived)
    server.run_forever()

t = threading.Thread(name='socketServer', target=socketServer)
t.setDaemon(True)
t.start()

painter = Painter()
painter.start()
