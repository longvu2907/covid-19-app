from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder

import threading
from utils import *
from screens.ScreenManager.ScreenManager import sm

Builder.load_file('screens/IPScreen/IP.kv')

class IPScreen(Screen):
  ip = ObjectProperty()
  def connect(self):
    try:
      connectToServer(self.ip.text)
      self.reset()
      sm.current = 'signin'
      sm.transition.direction = "up"
    except socket.error as exc:
      self.ip.error = True
      self.ip.focus = True
      self.ip.helper_text = 'Wrong ip'

  def submit(self):
    connectingThread = threading.Thread(target=self.connect)
    connectingThread.start()
    
  def reset(self):
    sm.remove_widget(self)
    sm.add_widget(IPScreen(name='ip'))
