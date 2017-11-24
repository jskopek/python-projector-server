from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
from Tkinter import *

###### SCREEN
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

master = Tk()
app = FullScreenApp(master)

width = master.winfo_screenwidth()
height = master.winfo_screenheight()

w = Canvas(master, width=width, height=height)
w.pack()

###### SERVER
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def hello():
    return render_template('base.html')

@socketio.on('drawEvent')
def handle_message(message):
    pctX = message[0]
    pctY = message[1]
    pctSize = message[2]

    # w.create_rectangle(0,0,master.winfo_screenwidth(),master.winfo_screenheight(),fill='blue')
    oX1 = width * pctX
    oY1 = height * pctY
    oX2 = oX1 + (width * pctSize)
    oY2 = oY1 + (width * pctSize)
    w.create_oval(oX1, oY1, oX2, oY2, fill='#000')
    print('Create Oval: oX1=%s oY1=%s oX2=%s oY2=%s' % (oX1, oY1, oX2, oY2))

##### SCREEN (pt2)
# mainloop()



