import eventlet
eventlet.monkey_patch()  # Ensure compatibility

import socketio
import random
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Initialize SocketIO
sio = socketio.Server()
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app, static_files={
    '/': './templates/'
})

#event handler connect
#event decorator
def task2(sid):
    while True:
        sio.sleep(5)
        sio.emit('mult2',{'value': random.randint(0, 100)})

def task(sid):
    while True:
        sio.sleep(5)
        sio.emit('mult',{'numbers': [3, 4]})

@sio.event
def connect(sid, environ):
    print(sid, 'connected')
    sio.start_background_task(task, sid)
    sio.start_background_task(task2, sid)



@sio.event
def disconnect(sid):
    print(sid, 'disconnected')

# Here there was a callback from the server to the client
# In Js in the connect function, inside it ther was the the callback of the function sum
@sio.event
def sum(sid, data):
    result = data['number'][0] + data['number'][1]
    return result

@app.route('/sobre')
def sobre():
    return "eurico"

