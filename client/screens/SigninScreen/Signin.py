from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from utils import *
from screens.ScreenManager.ScreenManager import sm

#load kv file
Builder.load_file('screens/SigninScreen/Signin.kv')

class SigninScreen(Screen):
  username = ObjectProperty()
  password = ObjectProperty()

  def submit(self):
    if signin(self.username.text, self.password.text):
      #sign in success change screen to menu
      sm.current = 'menu'
      sm.transition.direction = "up"
      self.reset()
    else: 
      #show error
      self.username.error = True
      self.username.focus = True
      self.username.helper_text = 'Wrong username or password'
  
  #reset state of screen
  def reset(self):
    sm.remove_widget(self)
    sm.add_widget(SigninScreen(name='signin'))
