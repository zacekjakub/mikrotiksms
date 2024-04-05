from typing import Union
from librouteros import connect
from fastapi import FastAPI, HTTPException, Request
import os
import subprocess, signal
import threading

app = FastAPI()

# Create a dictionary with users and passwords
users = {
    "user1": "pass3",
    "user2": "pass2",
    "user3": "pass1"

    # Add more users as needed
}

api = connect(
    username='mtuser', # User on MT with sms priviledges
    password='mtpass', # MT user pass
    host='192.168.1.1', # MT addr
)

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate the user based on the provided username and password."""
    if username in users and users[username] == password:
        return True
    return False

@app.get("/")
def read_root():
    return {"status": "Success"}

@app.post("/send/")
def send_sms(
    number: Union[str, None] = None,
    message: Union[str, None] = None,
    type: Union[str, None] = None,
    username: str = None,
    password: str = None
):
    if username is None or password is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    if number is None or message is None:
        return {"status": "Error", "message": "Missing parameters"}

    if type is None:
        type = "class-1"

    script = api.path('tool', 'sms')

    tuple(script('send', **{'port': 'lte1', 'phone-number': number, 'message': message, 'type': type}))

    return {"status": "Success", "number": number, "message": message, "type": type}

@app.route("/receive/", methods=['GET', 'POST'])
def receive_sms(
    request: Request,
    username: str = None,
    password: str = None
):
    if username is None or password is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    script = api.path('tool', 'sms')

    tuple(script('inbox', **{'print': 'message'}))

    return {"status": "Success"}
