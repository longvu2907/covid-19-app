from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_file('components/StatTable/StatTable.kv')

class IconListItem(OneLineIconListItem):
  icon = StringProperty()

#create data table
def StatTable(type, data):
  return MDDataTable(
    size_hint=(0.5, 1),
    use_pagination=True,
    pagination_menu_pos='auto',
    pagination_menu_height=240,
    rows_num=10,
    
    #column
    column_data=[
        ("No", 10),
        (type, 30),
        ("[color=#FFFF32]Cases[/color]", 30),
        ("[color=#FF8800]Active[/color]", 30),
        ("[color=#1EFF7C]Recovered[/color]", 30),
        ("[color=#FF0000]Deaths[/color]", 30),
        ],

    #row
    row_data=[
      (index + 1, 
      value,
      '[color=#FFFF32]NA[/color]' if data[value]['cases'] == None 
        else f"[color=#FFFF32]{format(data[value]['cases'], ',d')}[/color]",
      '[color=#FF8800]NA[/color]' if data[value]['active'] == None 
        else f"[color=#FF8800]{format(data[value]['active'], ',d')}[/color]",
      '[color=#1EFF7C]NA[/color]' if data[value]['recovered'] == None 
        else f"[color=#1EFF7C]{format(data[value]['recovered'], ',d')}[/color]",
      '[color=#FF0000]NA[/color]' if data[value]['deaths'] == None 
        else f"[color=#FF0000]{format(data[value]['deaths'], ',d')}[/color]")
      for index, value in enumerate(data)])

def SearchMenu(caller, data, setItem, icon):
  items = []

  #create item for each data
  for i in data:
      items.append(
        {
          "viewclass": "IconListItem",
          "icon": icon,
          "height": 56,
          "text": i,
          "on_release": lambda x=i: setItem(x),
        }
      )

  #create menu with items
  return MDDropdownMenu(
    caller=caller,
    items=items,
    position="bottom",
    max_height=350,
    width_mult=5)

