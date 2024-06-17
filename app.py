import eventlet
eventlet.monkey_patch()  # Ensure compatibility

import socketio
import random
from flask import Flask

import websocket
import json
import pandas as pd

btc = 0
# Initialize Flask app
app = Flask(__name__)

# Initialize SocketIO
sio = socketio.Server()
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app, static_files={
    '/': './templates/'
})

endpoint = 'wss://stream.binance.com:9443/ws/!miniTicker@arr'

#event handler connect
#event decorator
def task2(sid):
    while True:
        sio.sleep(5)
        sio.emit('mult2',{'value': random.randint(0, 100)})

def task(sid):
    global btc
    
    while True:
        #global btc
        sio.sleep(1)
        sio.emit('mult',{'value': random.randint(200, 300)})
        #sio.emit('mult',{'value': float(btc)})
        #print('btc inside',btc)
        #print(type(btc))

@sio.event
def connect(sid, environ):
    print(sid, 'connected')
    sio.start_background_task(background_thread)
    sio.sleep(5)
    sio.start_background_task(task, sid)

    sio.start_background_task(task2, sid)

    #sio.start_background_task(background_thread)



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


def df_import(data):
    global btc
    global times
    #Creating DF
    df_ = pd.DataFrame(data)
    #Filtering BTC USDT
    df_ = df_[df_['s'].str.endswith('BTCUSDT')]
    #Convert to float
    df_.c = df_.c.astype(float)
    #Convert to int - da erro - temos que converter para float
    df_.E = df_.E.astype(float)
    #df_.E = df_.E.astype(int)
    #df_.E = pd.to_datetime(df_['E'],unit='ms')
    #Selecting Columns
    final = df_[['s','E','c']]
    #Print
    print(final.iloc[-1].c)
    btc = final.iloc[-1].c
    times = final.iloc[-1].E
    
    sio.emit('updateData', {'btc': btc, 'times':times})

    print('btc',btc)
    
 

    #socketio.emit('updateData', {'btc': btc})
    #socketio.emit('updateData', {'times':times})
    #print(times)

def on_message(wd,message):
    global out
    out = json.loads(message)
    df_import(out)


def background_thread():
   
    while True:
        ws = websocket.WebSocketApp(endpoint, on_message=on_message)
        ws.run_forever()


