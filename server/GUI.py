from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivymd.uix.list import IconLeftWidget, OneLineIconListItem
from kivymd.uix.screen import Screen

from kivy.lang import Builder

from datetime import datetime

Builder.load_file('GUI.kv')

class MainView(Screen):
  active = ObjectProperty()
  displayList = ObjectProperty()
  scrollView = ObjectProperty()

  def updateList(self, text, icon, color = 'yellow'):
    now = datetime.now().strftime("%H:%M:%S")
    color = {'red':'#FF0000', 'yellow':'#FFFF32', 'green':'#1EFF7C'}[color]

    newItem =  OneLineIconListItem(text=f'{now}: [color={color}]{text}[/color]')
    newItem.add_widget(IconLeftWidget(icon=icon))
    self.displayList.add_widget(newItem)
    self.scrollView.scroll_to(newItem)
    self.scrollView.always_overscroll = False

  def updateNumberClients(self, number):
    self.active.text = f'ACTIVE CLIENTS: {number}'

class MainApp(MDApp):
  def build(self):
    #Set title name for app
    self.title = 'Covid-19'
    #Set icon for app
    self.icon = 'assets/icon.png'

    #Set theme
    self.theme_cls.theme_style = "Dark"
    self.theme_cls.primary_palette = "Green"

    self.mainView = MainView()

    return self.mainView
