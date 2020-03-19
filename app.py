from flask import Flask, render_template, request, redirect, make_response
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from models.room import Room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}
for room_num in range(100):
    rooms[room_num] = Room(room_num)


@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/enter_room')
def enter_room():
    # Get Username and Gamepin and store in cookie
    username = request.args.get('username')
    gamepin = request.args.get('gamepin')
    if int(gamepin) in rooms:
        if username not in rooms[int(gamepin)].all_users:
            resp = make_response(redirect("/chat"))
            resp.set_cookie('username', username)
            resp.set_cookie('gamepin', gamepin)
            return resp
    else:
        return redirect("/")


@app.route('/ready')
def ready():
    if (int(request.cookies.get('gamepin')) in rooms):
        gamepin = int(request.cookies.get('gamepin'))
        username = request.cookies.get('username')
        return render_template('ready.html', pin=gamepin, username=username)
    else:
        return redirect("/")

@app.route('/chat')
def chat():
    if (int(request.cookies.get('gamepin')) in rooms):
        gamepin = int(request.cookies.get('gamepin'))
        username = request.cookies.get('username')
        return render_template('chat.html', pin=gamepin, username=username)
    else:
        return redirect("/")


# SOCKET IO CONFIGURATIONS -------

@socketio.on("message")
def message_recived(message_content):
    gamepin = int(request.cookies.get('gamepin'))
    username = request.cookies.get('username')
    print(username, "from room ", str(gamepin), "has sent: ", message_content)
    print(gamepin)
    emit("new_message", (username, message_content), room=gamepin)
    print("Sent the message to room ", str(gamepin))

@socketio.on('connect')
def connect():
    gamepin = int(request.cookies.get('gamepin'))
    username = request.cookies.get('username')
    print(username, "has connected to room", int(gamepin))
    rooms[gamepin].remove_user(username)
    rooms[gamepin].add_user(username)
    join_room(gamepin)
    
    emit('users_update',  {'pending_users': [ name for name in rooms[gamepin].pending_users ], \
        'ready_users': [ name for name in rooms[gamepin].ready_users ]}, room=gamepin)
    emit("new_message", ("system", "{} has connected".format(username)))

@socketio.on('disconnecting')
def disconnecting():
    username = request.cookies.get("username")
    gamepin = int(request.cookies.get("gamepin"))
    print(username, "has disconnected from game room", str(gamepin))
    rooms[gamepin].remove_user(username)
    emit("new_message", ("system", "{} has disconnected".format(username)), room=gamepin)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
