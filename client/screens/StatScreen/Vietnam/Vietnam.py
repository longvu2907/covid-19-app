from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty

from kivy.lang import Builder

from utils import *
from screens.ScreenManager.ScreenManager import sm
from components.StatTable.StatTable import StatTable, SearchMenu

Builder.load_file('screens/StatScreen/Vietnam/Vietnam.kv')

class VietnamStat(Screen):
  dataTable = ObjectProperty()
  search = ObjectProperty()
  updateTime = ObjectProperty()

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.vietnamData = []
    self.menuItems = []

  def setItem(self, textItem):
    #get data from country menu
    self.searchMenu.items = self.menuItems
    self.search.text = textItem
    #hide menu
    self.searchMenu.dismiss()

    #show all results if choice is World
    if (textItem == 'Vietnam'):
      self.dataTables.row_data = self.rowData
      return

    #show result
    self.dataTables.row_data = [(
      1, 
      textItem,
      '[color=#FFFF32]NA[/color]' if self.vietnamData[textItem]['cases'] == None 
        else f"[color=#FFFF32]{format(self.vietnamData[textItem]['cases'], ',d')}[/color]",
      '[color=#FF8800]NA[/color]' if self.vietnamData[textItem]['active'] == None 
        else f"[color=#FF8800]{format(self.vietnamData[textItem]['active'], ',d')}[/color]",
      '[color=#1EFF7C]NA[/color]' if self.vietnamData[textItem]['recovered'] == None 
        else f"[color=#1EFF7C]{format(self.vietnamData[textItem]['recovered'], ',d')}[/color]",
      '[color=#FF0000]NA[/color]' if self.vietnamData[textItem]['deaths'] == None 
        else f"[color=#FF0000]{format(self.vietnamData[textItem]['deaths'], ',d')}[/color]")]
    #add dump row cause bug of kivymd 0.14
    self.dataTables.row_data.append(('','','','','',''))

  def resetTextField(self):
    self.search.text = ''

  def filter(self):
    #return if search bar not focus
    if not self.search.focus: return

    #get search input
    input = self.search.text
    menuItems = self.menuItems
    itemsFiltered = []

    #filter data
    for item in menuItems:
      if input.lower() in item["text"].lower(): 
        itemsFiltered.append(item)
    if len(itemsFiltered) == 0:
      itemsFiltered.append({
          "viewclass": "IconListItem",
          "icon": "magnify",
          "height": 56,
          "text": "No result"
      })
    self.searchMenu.items = itemsFiltered
    self.searchMenu.dismiss()
    self.searchMenu.open()

  def on_enter(self):
    #get covid data from server
    data = getData()

    #pop time updated data  
    updateTime = data.pop('last updated', None)

    #get vietname data
    self.vietnamData = {'Vietnam':{
      'cases': data['Vietnam']['cases'],
      'active': data['Vietnam']['active'],
      'recovered': data['Vietnam']['recovered'],
      'deaths': data['Vietnam']['deaths'],
    }}
    for i in data['Vietnam']['provinces']:
      self.vietnamData[i] = data['Vietnam']['provinces'][i]

    #create search country menu
    self.searchMenu = SearchMenu(self.search, self.vietnamData, self.setItem, 'city')
    self.menuItems = self.searchMenu.items

    #create table data
    self.dataTables = StatTable('Province', self.vietnamData)
    self.rowData = self.dataTables.row_data

    #add to screen
    self.dataTable.add_widget(self.dataTables)

    #update time updated data
    self.updateTime.text = f"Last Updated: {updateTime}"

  #reset state of screen
  def reset(self):
    sm.remove_widget(self)
    sm.add_widget(VietnamStat(name='vietnamStat'))
