import socket
import json
import threading
import os
from time import sleep

from screens.ScreenManager.ScreenManager import sm

#Config
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'

#Command
DISCONNECT_MSG = "-DISCONNECT"
SIGNIN_MSG = "-SIGNIN"
SIGNUP_MSG = "-SIGNUP"
GETDATA_MSG = "-GETDATA"
FAILED_MSG = "-FAILED"
SUCCESS_MSG = "-SUCCESS"

#Init socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

MSG_QUEUE = []

#Receive message
def receive(screenManager):
  global client
  global RECEIVE_THREAD
  while True:
    try:
      messageLength = client.recv(HEADER).decode(FORMAT)
      if messageLength:
          msg = client.recv(int(messageLength)).decode(FORMAT)
          if (msg == DISCONNECT_MSG):
            #create new connect when disconnect from server
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            MSG_QUEUE.clear()
            #create new thread to receive msg
            RECEIVE_THREAD = threading.Thread(target=receive, args=(sm,))

            #return to ip screen
            screenManager.current = 'ip'
            return None
          MSG_QUEUE.append(msg)
    except:
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      MSG_QUEUE.clear()
      RECEIVE_THREAD = threading.Thread(target=receive, args=(sm,))

      screenManager.current = 'ip'
      return None

#receive message thread
RECEIVE_THREAD = threading.Thread(target=receive, args=(sm,))

#connect to server with ip
def connectToServer(ip):
  client.connect((ip, PORT))
  RECEIVE_THREAD.start()

#Send message
def send(msg):
  message = msg.encode(FORMAT)
  msg_length = len(message)
  send_length = str(msg_length).encode(FORMAT)
  send_length += b' ' * (HEADER - len(send_length))
  client.send(send_length)
  client.send(message)

#Signin command
def signin(username, password):
  if username == '' or password == '': 
    return False

  send(SIGNIN_MSG)
  send(json.dumps({"username":username,"password":password}))

  #delay to update MSG_QUEUE
  sleep(0.1)

  if MSG_QUEUE.pop(0) == SUCCESS_MSG:
    return True
  else:
    return False

#Signup command
def signup(username, password):
  if username == '' or password == '': 
    return False

  send(SIGNUP_MSG)
  send(json.dumps({"username":username,"password":password}))

  #delay to update MSG_QUEUE
  sleep(0.1)

  if MSG_QUEUE.pop(0) == SUCCESS_MSG:
    return True
  else:
    return False

#Get data command
def getData():
  send(GETDATA_MSG)

  #delay to update MSG_QUEUE
  sleep(0.1)

  return json.loads(MSG_QUEUE.pop(0))

def closeApp():
  #send disconnect message
  send(DISCONNECT_MSG)
  
  #close app
  os._exit(0)
