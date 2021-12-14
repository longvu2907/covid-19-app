from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder

#load kv file
Builder.load_file('screens/ScreenManager/ScreenManager.kv')

#create screen management
sm = ScreenManager()

#create background for app
class MainBackground(Screen):
  pass

