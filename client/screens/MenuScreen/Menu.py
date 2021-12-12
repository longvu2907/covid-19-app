from kivymd.uix.screen import Screen
from kivy.lang import Builder

from utils import *
from screens.ScreenManager.ScreenManager import sm

Builder.load_file('screens/MenuScreen/Menu.kv')

class MenuScreen(Screen):
  def signout(self):
    sm.current = 'signin'
    sm.transition.direction = 'down'
  def quit(self):
    closeApp()