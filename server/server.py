from time import sleep
import threading
import logging
from websocket_server import WebsocketServer
from utils import FullScreenApp
from Tkinter import *
from pygame.locals import *
import pygame
import sys
import json
import os

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-15s) %(message)s')

class PyGamePainter(object):
    # set up colors
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
 
    def __init__(self, **kwargs):
        # set up pygame
        pygame.init()


        # set up the window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        screen = pygame.display.Info()
        self.windowSurface = pygame.display.set_mode((screen.current_w, screen.current_h), 0, 32)
        pygame.display.set_caption('Hello world!')

        self.width = self.windowSurface.get_width()
        self.height = self.windowSurface.get_height()
       
        # set up fonts
        basicFont = pygame.font.SysFont(None, 48)

        # set up the text
        text = basicFont.render('Hello world!', True, self.WHITE, self.BLUE)
        textRect = text.get_rect()
        textRect.centerx = self.windowSurface.get_rect().centerx
        textRect.centery = self.windowSurface.get_rect().centery

        # draw the white background onto the surface
        self.windowSurface.fill(self.WHITE)

        # self.drawSurface = pygame.Surface((self.width, self.height))


    def draw_oval(self, pctX, pctY, pctSize, color):
        x = int(self.width * pctX)
        y = int(self.height * pctY)
        size = int(self.width * pctSize)

        color = (int(color[0]), int(color[1]), int(color[2])) if color else self.BLACK

        logging.debug('draw_oval {0},{1},{2}'.format(x, y, size))
        pygame.draw.circle(self.windowSurface, color, (x, y), size, 0)
        # self.windowSurface.blit(self.drawSurface, (0,0))
        pygame.display.update()

    def start(self):
        # draw the window onto the surface
        pygame.display.update()

        # run game loop
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


class TkinterPainter(object):
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

        logging.debug('drawOval: Start')
        self.canvas.create_oval(oX1, oY1, oX2, oY2, fill='#000')
        logging.debug('drawOval: Create Oval: oX1=%s oY1=%s oX2=%s oY2=%s' % (oX1, oY1, oX2, oY2))

    def start(self):
        mainloop()


class SocketServer(object):
    def __init__(self, draw_callback, port=5002, **kwargs):
        self.port = port
        self.server = WebsocketServer(host='0.0.0.0', port=self.port)
        self.server.set_fn_message_received(self.message_received)

        self.draw_callback = draw_callback

    def message_received(self, client, server, message):
        data = json.loads(message)
        logging.debug('message_received with id: %d' % data[4])
        self.draw_callback(pctX=data[0], pctY=data[1], pctSize=data[2], color=data[3])

    def start(self):
        self.server.run_forever()


painter = PyGamePainter()

# initialize a threaded socket server that calls painter draw_oval on event
server = SocketServer(draw_callback=painter.draw_oval)
threaded_server = threading.Thread(name='socketServer', target=server.start)
threaded_server.setDaemon(True)
threaded_server.start()

# start the main tkinter loop
painter.start()
