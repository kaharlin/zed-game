from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
import planisphere

app = Flask(__name__)

@app.route("/")

def index():
# this is used to "setup" the session with starting values
    session['room_name'] = planisphere.START
    return redirect(url_for("game"))

@app.route("/game", methods=['GET', 'POST'])
def game():
    room_name = session.get('room_name') #grabbing stored room name

    if request.method == "GET":
        if room_name:
            room = planisphere.load_room(room_name) #loads the new room
            return render_template("show_room.html", room=room)
        else:
            # why is there here? do you need it?'
            return render_template("you_died.html")
    else:
        action = request.form.get('action')

        if room_name and action:
            room = planisphere.load_room(room_name) #instantiates the room
            next_room = room.go(action) #doing room.go

            if not next_room:
                session['room_name'] = planisphere.name_room(room) #stores cookie
            else:
                session['room_name'] = planisphere.name_room(next_room) #stores cookie
        return redirect(url_for("game"))
# YOU SHOULD CHANGE THIS IF YOU PUT ON THE INTERNET
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == "__main__":
    app.run()
