from Tkinter import *

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

print master.winfo_screenwidth()
print master.winfo_screenheight()

w = Canvas(master, width=800, height=900)
w.pack()

w.create_line(0,0,200,100)
w.create_line(0,100,200,0, fill='red', dash=(4,4))

w.create_rectangle(50,25,150,75,fill='blue')
mainloop()

