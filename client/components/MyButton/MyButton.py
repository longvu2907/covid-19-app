from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.button import MDFillRoundFlatButton

class MyButton(MDFillRoundFlatButton, ThemableBehavior, HoverBehavior):
  def on_enter(self):
    self.md_bg_color = (0, 1, 0, 1)

  def on_leave(self):
    self.md_bg_color = (0, 0, 0, 0)