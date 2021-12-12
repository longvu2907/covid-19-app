from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder

Builder.load_file('screens/ScreenManager/ScreenManager.kv')

sm = ScreenManager()

class MainBackground(Screen):
  pass

