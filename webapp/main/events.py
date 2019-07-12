from flask import session
from flask_socketio import emit, join_room, leave_room
# from eventlet import sleep
import datetime
from .. import socketio
from .const import *
from .data import (get_crowd_data_db, insert_crowd_info, get_chatdata)
import time


def get_message(role, text):
    # if role == USER:
    #     text = add_tag(text)
    if role == AGENT:
        return '<div><b class="blue-text">{0}: </b>{1}</div>'.format(role, text)
    else:
        return "<div<b>{0}: </b>{1}</div>".format(role, text)


@socketio.on('disconnect', namespace='/chat')
def on_disconnect():
    print("@@@ Client disconnected", str(datetime.datetime.utcnow()))


@socketio.on('connect', namespace='/chat')
def on_connect():
    print("@@@ Client connected", str(datetime.datetime.utcnow()))


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    task_id = session.get(TASK_ID)
    role = session.get(ROLE)
    username = session.get(USERNAME)
    print('##join', role, username, task_id)
    insert_crowd_info(session)
    session[TURN] = 0
    join_room(task_id)
    history = get_chatdata(session)
    if history:
        # session[TURN] = history[-1][TURN]
        for ele in history:
            emit('status', {MSG: get_message(ele[ROLE], ele[MSG]),
                            ROLE: ele[ROLE], MODE:'human'}, room=session[TASK_ID])
        emit('left', {})


@socketio.on('text', namespace='/chat')
def text(message):
    coll = get_crowd_data_db(session)
    role = session.get(ROLE)
    mode = session.get(MODE)
    msg = message[MSG].strip()
    if msg:
        session[TURN] = session.get(TURN) + 1
        emit('message', {MSG: get_message(role, msg), ROLE: role, MODE: mode},
             room=session.get(TASK_ID))


@socketio.on('left', namespace='/chat')
def left(message):
    # db_crowd = get_crowd_data_db(session)
    task_id = session.get(TASK_ID)
    role = session.get(ROLE)
    leave_room(task_id)
    # insert_chatdata(db_chat, session, {MSG: '#END'})
    insert_crowd_info(session)
    # emit('status', {MSG: role + ' has left the conversation.'}, room=task_id)
