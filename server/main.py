import socket 
import threading
import json
from api import getAPIData

from GUI import MainApp
from kivy.core.window import Window
import os

#Config
HEADER = 64
PORT = 5050
SERVERIP = '127.0.0.1'
FORMAT = 'utf-8'
UPDATE_TIME = 3600
THREAD_INIT = 3

#Command
DISCONNECT_MSG = "-DISCONNECT"
SIGNIN_MSG = "-SIGNIN"
SIGNUP_MSG = "-SIGNUP"
GETDATA_MSG = "-GETDATA"
FAILED_MSG = "-FAILED"
SUCCESS_MSG = "-SUCCESS"

#List client
CLIENTS = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVERIP, PORT))

#Get user data
try:
  userData = json.load(open('./data/user.json'))
except:
  userData = {}

#Receive message
def receive(conn):
  messageLength = conn.recv(HEADER).decode(FORMAT)
  if messageLength:
      msg = conn.recv(int(messageLength)).decode(FORMAT)
      return msg
  return None

#Send message
def send(conn, msg):
  message = msg.encode(FORMAT)
  msg_length = len(message)
  send_length = str(msg_length).encode(FORMAT)
  send_length += b' ' * (HEADER - len(send_length))
  conn.send(send_length)
  conn.send(message)

#Handle signin command
def signin(conn, ip, port):
  signinData = json.loads(receive(conn))
  username = signinData["username"]
  password = signinData["password"]

  if username in userData and password == userData[username]:
    #send failed message if wrong username
    send(conn, SUCCESS_MSG)
    ui.mainView.updateList(f"[{ip}:{port}] {SIGNIN_MSG} {SUCCESS_MSG}", 'account', 'green')
  else:
    send(conn, FAILED_MSG)
    ui.mainView.updateList(f"[{ip}:{port}] {SIGNIN_MSG} {FAILED_MSG}", 'account', 'red')


#Handle singout command
def signup(conn, ip, port):
  #get register data from client
  signupData = json.loads(receive(conn))
  username = signupData["username"]
  password = signupData["password"]

  if username in userData:
    #send failed message if username exists
    send(conn, FAILED_MSG)
    ui.mainView.updateList(f"[{ip}:{port}] {SIGNUP_MSG} {FAILED_MSG}", 'account', 'red')
  else:
    #update userData 
    userData[username] = password
    with open('./data/user.json', 'w', encoding=FORMAT) as f:
      json.dump(userData, f, ensure_ascii=False)

    #send success message
    send(conn, SUCCESS_MSG)
    ui.mainView.updateList(f"[{ip}:{port}] {SIGNUP_MSG} {SUCCESS_MSG}", 'account', 'green')


#Handle get data command
def getData(conn, ip, port):
  data = open('./data/covid-data.json', 'r', encoding=FORMAT).read()
  send(conn, data)
  ui.mainView.updateList(f"[{ip}:{port}] {GETDATA_MSG}", 'account', 'green')


def handleClient(conn, addr):
  ip, port = addr

  ui.mainView.updateNumberClients(threading.activeCount() - THREAD_INIT)
  ui.mainView.updateList(f"[{ip}:{port}] connected.", 'account', 'green')

  connected = True
  while connected:
    try:
      msg = receive(conn)
      if msg:
        if msg == DISCONNECT_MSG:
          connected = False
        elif msg == SIGNIN_MSG:
          signin(conn, ip, port)
        elif msg == SIGNUP_MSG:
          signup(conn, ip, port)
        elif msg == GETDATA_MSG:
          getData(conn, ip, port)
    except:
      connected = False

  ui.mainView.updateNumberClients(threading.activeCount() - THREAD_INIT - 1)
  ui.mainView.updateList(f"[{ip}:{port}] disconnected.", 'account', 'red')

  global CLIENTS
  CLIENTS = list(filter(lambda i: i['conn'] != conn, CLIENTS))
  conn.close()

def setInterval(func, time):
  e = threading.Event()
  while not e.wait(time):
    func()

def updateData():
  data = getAPIData()
  with open('./data/covid-data.json', 'w', encoding=FORMAT) as f:
    json.dump(data, f, ensure_ascii=False)

  ui.mainView.updateList('Data updated', 'server')

def closeServer():
  for client in CLIENTS:
    print(client)
    send(client['conn'], DISCONNECT_MSG)
    client['conn'].close()
  
  os._exit(0)

def start():
  updateData()
  updateDataThread = threading.Thread(target=setInterval, args=(updateData, UPDATE_TIME))
  updateDataThread.start()

  server.listen()
  ui.mainView.updateList(f"Server is listening on [{SERVERIP}:{PORT}]", 'server')

  while True:
    conn, addr = server.accept()
    CLIENTS.append({'conn': conn, 'addr': addr})

    thread = threading.Thread(target=handleClient, args=(conn, addr))
    thread.start() 

serverThread = threading.Thread(target=start)
serverThread.start()

ui = MainApp()
Window.bind(on_request_close=lambda _: closeServer())
ui.run()
