from flask import Flask, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/notify', methods=['POST'])
def notify():
    message = request.form.get('message')
    socketio.emit('notification', message, namespace='/')
    return 'OK', 200

if __name__ == '__main__':
    socketio.run(app)
