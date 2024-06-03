import hashlib
import re
import requests
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen

class Login_screen(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"

        layout = MDBoxLayout(orientation='vertical', padding=10)

        toolbar = Label(text="Авторизация", size_hint_y=None, height="48dp")
        layout.add_widget(toolbar)

        layout.add_widget(Widget(size_hint_y=None, height="30dp"))

        email_layout = MDBoxLayout(size_hint=(1, None), height="30dp")
        self.email_field = self.create_textinput("Введите ваш email", "email")
        email_layout.add_widget(self.email_field)
        email_icon_button = MDIconButton(icon="email")
        email_layout.add_widget(email_icon_button)
        layout.add_widget(email_layout)

        layout.add_widget(Widget(size_hint_y=None, height="30dp"))

        password_layout = MDBoxLayout(size_hint=(1, None), height="30dp")
        self.password_field = self.create_textinput("Введите пароль", "password", password=True)
        password_layout.add_widget(self.password_field)
        password_icon_button = MDIconButton(icon="eye")
        password_icon_button.bind(on_release=self.toggle_password_visibility_password)
        password_layout.add_widget(password_icon_button)
        layout.add_widget(password_layout)

        layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        login_button = MDRaisedButton(
            text="Войти",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        login_button.bind(on_release=self.on_button_press)
        layout.add_widget(login_button)

        layout.add_widget(Widget())

        return layout

    def create_textinput(self, hint_text, info_key, password=False):
        text_input = MDTextField(
            text='',
            hint_text=hint_text,
            size_hint=(1, None),
            font_size='15sp',
            mode="rectangle",
            line_color_normal=get_color_from_hex("#2C2C2C"),
            line_color_focus=get_color_from_hex("#2C2C2C"),
            password=password
        )
        return text_input

    def hash_password(self, password):
        hash_object = hashlib.sha256()
        hash_object.update(password.encode('utf-8'))
        return hash_object.hexdigest()

    def toggle_password_visibility_password(self, instance):
        self.password_field.password = not self.password_field.password
        instance.icon = "eye-off" if self.password_field.password else "eye"

    def on_button_press(self, instance):
        email = self.email_field.text
        password = self.password_field.text

        hashed_password = self.hash_password(password)
        response = requests.post('http://localhost:5000/login', data={'email': email, 'password': hashed_password})
        if response.status_code == 200:
            self.show_alert_dialog("Успешная авторизация!")
        else:
            self.show_alert_dialog("Ошибка авторизации!")

    def show_alert_dialog(self, text):
        self.dialog = MDDialog(title='Уведомление', text=text, size_hint=(0.8, 1),
                          buttons=[MDRaisedButton(text='ОК', on_release=self.close_dialog)])
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

Login_screen().run()
