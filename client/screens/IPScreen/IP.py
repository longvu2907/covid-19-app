from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder

import threading
from utils import *
from screens.ScreenManager.ScreenManager import sm

#load kv file
Builder.load_file('screens/IPScreen/IP.kv')

class IPScreen(Screen):
  ip = ObjectProperty()

  #connect to server
  def connect(self):
    try:
      self.dialog.open()
      connectToServer(self.ip.text)
      self.reset()
      sm.current = 'signin'
      sm.transition.direction = "up"
    except:
      self.dialog.dismiss()
      self.ip.error = True
      self.ip.focus = True
      self.ip.helper_text = 'Wrong ip'

  #click submit
  def submit(self):
    self.dialog = MDDialog(
        text="Connecting...",
      )

    #connect to server thread
    connectingThread = threading.Thread(target=self.connect)
    connectingThread.start()
    
  #clear state of screen
  def reset(self):
    self.dialog.dismiss()
    sm.remove_widget(self)
    sm.add_widget(IPScreen(name='ip'))
