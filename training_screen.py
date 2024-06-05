import threading
import requests
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

class TrainingScreen(Screen):
    def __init__(self, **kwargs):
        super(TrainingScreen, self).__init__(**kwargs)
        self.name = 'training_screen'


