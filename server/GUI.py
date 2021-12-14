from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.list import IconLeftWidget, OneLineIconListItem
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.lang import Builder

from datetime import datetime

#load kv file
Builder.load_file('GUI.kv')

#custom button
class MyButton(MDFillRoundFlatButton, ThemableBehavior, HoverBehavior):
  #change background color button when hover
  def on_enter(self):
    self.md_bg_color = (0, 1, 0, 1)

  #default background color button
  def on_leave(self):
    self.md_bg_color = (0, 0, 0, 0)

#client screen
class ClientScreen(Screen):
  displayList = ObjectProperty()
  scrollView = ObjectProperty()
  active = ObjectProperty()

  #add client
  def addClient(self, addr):
    ip, port = addr

    #create widget 
    now = datetime.now().strftime("%H:%M:%S")
    newItem =  OneLineIconListItem(text=f'{now}: [color=#FFFF32][{ip}:{port}][/color]')
    newItem.add_widget(IconLeftWidget(icon='account'))
    self.displayList.ids[f'{ip}:{port}'] = newItem

    #add widget to ui
    self.displayList.add_widget(newItem)
    self.scrollView.scroll_to(newItem)
    self.scrollView.always_overscroll = False

  #remove client
  def removeClient(self, addr):
    ip, port = addr

    #remove widget
    self.displayList.remove_widget(self.displayList.ids[f'{ip}:{port}'])

  #update number client
  def updateNumberClients(self, number):
    #update number clients label
    self.active.text = f'ACTIVE CLIENTS: {number}'

#log screen
class LogScreen(Screen):
  active = ObjectProperty()
  displayList = ObjectProperty()
  scrollView = ObjectProperty()
  closeServerBtn = ObjectProperty()

  #update log list
  def updateList(self, text, icon, color = 'yellow'):
    #create widget
    now = datetime.now().strftime("%H:%M:%S")
    color = {'red':'#FF0000', 'yellow':'#FFFF32', 'green':'#1EFF7C'}[color]
    newItem =  OneLineIconListItem(text=f'{now}: [color={color}]{text}[/color]')

    #add widget to ui
    newItem.add_widget(IconLeftWidget(icon=icon))
    self.displayList.add_widget(newItem)
    self.scrollView.scroll_to(newItem)
    self.scrollView.always_overscroll = False

  #update number clients
  def updateNumberClients(self, number):
    #update number clients label
    self.active.text = f'ACTIVE CLIENTS: {number}'

#App
class MainApp(MDApp):
  def __init__(self, closeServer, **kwargs):
    super().__init__(**kwargs)
    self.closeServer = closeServer
    self.listClients = []

  def build(self):
    #Set title name for app
    self.title = 'Covid-19 Server'
    #Set icon for app
    self.icon = 'assets/icon.png'

    #Set theme
    self.theme_cls.theme_style = "Dark"
    self.theme_cls.primary_palette = "Green"

    #create and add screen
    self.logScreen = LogScreen(name='logList')
    self.clientScreen = ClientScreen(name='clientList')
    self.sm = ScreenManager()
    self.sm.add_widget(self.logScreen)
    self.sm.add_widget(self.clientScreen)

    return self.sm

  #update list client
  def updateListClients(self, listClients):
    self.listClients = listClients
    self.clientScreen.updateNumberClients(len(listClients))
    self.logScreen.updateNumberClients(len(listClients))

