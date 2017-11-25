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


class SocketServer(object):
    def __init__(self, draw_callback, port=5002, **kwargs):
        self.port = port
        self.server = WebsocketServer(self.port)
        self.server.set_fn_message_received(self.message_received)

        self.draw_callback = draw_callback

    def message_received(self, client, server, message):
        data = json.loads(message)
        logging.debug('message_received with contents: %s' % message)
        self.draw_callback(pctX=data[0], pctY=data[1], pctSize=data[2])

    def start(self):
        self.server.run_forever()


painter = Painter()

# initialize a threaded socket server that calls painter draw_oval on event
server = SocketServer(draw_callback=painter.draw_oval)
threaded_server = threading.Thread(name='socketServer', target=server.start)
threaded_server.setDaemon(True)
threaded_server.start()

# start the main tkinter loop
painter.start()
