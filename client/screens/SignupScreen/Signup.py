from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
from components.MyButton.MyButton import MyButton
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from utils import *
from screens.ScreenManager.ScreenManager import sm

Builder.load_file('screens/SignupScreen/Signup.kv')

class SignupScreen(Screen):
  username = ObjectProperty()
  password = ObjectProperty()
  confirmPassword = ObjectProperty()

  def submit(self):
    if self.confirmPassword.text != self.password.text:
      self.confirmPassword.error = True
      self.confirmPassword.focus = True
      self.confirmPassword.helper_text = 'Password not match'
      return

    if signup(self.username.text, self.password.text):
      self.username.text = ''
      self.password.text = ''
      self.confirmPassword.text = ''
      self.dialog = MDDialog(
        text="Success",
        buttons=[
            MyButton(
              text="Sign In",
              on_release=lambda _: self.gotoSignin()
            )
        ],
      )
      self.dialog.open()
    else:
      self.username.error = True
      self.username.focus = True
      self.username.helper_text = 'Username exists'
  
  def gotoSignin(self):
    sm.current = 'signin'
    sm.transition.direction = 'right'
    if hasattr(self, 'dialog'): self.dialog.dismiss()
    self.reset()

  def reset(self):
    sm.remove_widget(self)
    sm.add_widget(SignupScreen(name='signup'))
