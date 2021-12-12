import kivy
import kivymd
from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.window import Window

#Import Screen
from screens.ScreenManager.ScreenManager import sm, MainBackground
from screens.IPScreen.IP import IPScreen
from screens.SigninScreen.Signin import SigninScreen
from screens.SignupScreen.Signup import SignupScreen
from screens.MenuScreen.Menu import MenuScreen
from screens.StatScreen.Global.Global import GlobalStat
from screens.StatScreen.Vietnam.Vietnam import VietnamStat

#Import client utils
from utils import *

#Config user behaviour
Config.set('input', 'mouse', 'mouse,disable_multitouch')

class MainApp(MDApp):
  def build(self):
    #Set title name for app
    self.title = 'Covid-19'
    #Set icon for app
    self.icon = 'assets/icon.png'

    #Set theme
    self.theme_cls.theme_style = "Dark"
    self.theme_cls.primary_palette = "Green"

    #Add screen to screen manager
    sm.add_widget(IPScreen(name='ip'))
    sm.add_widget(SigninScreen(name='signin'))
    sm.add_widget(SignupScreen(name='signup'))
    sm.add_widget(MenuScreen(name='menu'))
    sm.add_widget(GlobalStat(name='globalStat'))
    sm.add_widget(VietnamStat(name='vietnamStat'))

    #Set main background
    mainBackground = MainBackground()
    mainBackground.add_widget(sm)

    return mainBackground


if __name__ == '__main__':
  #Send disconnect message when user close app
  Window.bind(on_request_close=lambda _: closeApp())

  MainApp().run()

