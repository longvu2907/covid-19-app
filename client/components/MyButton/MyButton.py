from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.button import MDFillRoundFlatButton

#custom button
class MyButton(MDFillRoundFlatButton, ThemableBehavior, HoverBehavior):
  #change background color button when hover
  def on_enter(self):
    self.md_bg_color = (0, 1, 0, 1)

  #default background color button
  def on_leave(self):
    self.md_bg_color = (0, 0, 0, 0)