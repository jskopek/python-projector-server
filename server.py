from flask import Flask
from flask import render_template
from flask_socketio import SocketIO

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def hello():
    return render_template('base.html')

@socketio.on('drawEvent')
def handle_message(message):
    print(message)
