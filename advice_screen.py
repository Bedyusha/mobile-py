# advice_screen.py
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton

class AdviceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDRaisedButton(
            text="Советы на особый случай",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        ))
