from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton, MDFloatingActionButton, MDRectangleFlatButton

class MainApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(MDRaisedButton(text='MDRaisedButton', pos_hint={'center_x': 0.5}))
        layout.add_widget(MDFlatButton(text='MDFlatButton', pos_hint={'center_x': 0.5}))
        layout.add_widget(MDIconButton(icon='android', pos_hint={'center_x': 0.5}))
        layout.add_widget(MDFloatingActionButton(icon='plus', pos_hint={'center_x': 0.5}))
        layout.add_widget(MDRectangleFlatButton(text='MDRectangleFlatButton', pos_hint={'center_x': 0.5}))
        return layout

MainApp().run()
