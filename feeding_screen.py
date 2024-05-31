import threading
import requests
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

class FeedingScreen(Screen):
    def __init__(self, **kwargs):
        super(FeedingScreen, self).__init__(**kwargs)
        self.name = 'feeding_screen'
        btn = MDRaisedButton(
            text="Уведомление",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.send_notification
        )
        self.add_widget(btn)

    def send_notification(self, *args):
        threading.Thread(target=self.send_request).start()

    def send_request(self):
        # Отправка запроса на сервер
        response = requests.post('http://localhost:5000/notify', data={'message': 'Вы нажали на кнопку!'})
        if response.status_code == 200:
            Clock.schedule_once(lambda dt: self.show_notification(), 0)

    def show_notification(self):
        snackbar = MDSnackbar(MDLabel(text="Вы нажали на кнопку!"))
        snackbar.duration = 2  # Установите продолжительность в 2 секунды
        snackbar.open()
