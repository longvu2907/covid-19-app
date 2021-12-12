from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from utils import *
from screens.ScreenManager.ScreenManager import sm

Builder.load_file('screens/SigninScreen/Signin.kv')

class SigninScreen(Screen):
  username = ObjectProperty()
  password = ObjectProperty()

  def submit(self):
    if signin(self.username.text, self.password.text):
      sm.current = 'menu'
      sm.transition.direction = "up"
      self.reset()
    else: 
      self.username.error = True
      self.username.focus = True
      self.username.helper_text = 'Wrong username or password'
  
  def reset(self):
    sm.remove_widget(self)
    sm.add_widget(SigninScreen(name='signin'))
