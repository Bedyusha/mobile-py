from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
import requests
import re
import hashlib
from kivy.uix.screenmanager import ScreenManager, Screen

class Registration_screen(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"  # Основной цвет - оранжевый
        self.theme_cls.theme_style = "Dark"  # Темный стиль темы

        layout = MDBoxLayout(orientation='vertical', padding=10)  # Добавлены отступы

        toolbar = Label(text="Регистрация", size_hint_y=None, height="48dp")
        layout.add_widget(toolbar)

        layout.add_widget(Widget(size_hint_y=None, height="30dp"))

        email_layout = MDBoxLayout(size_hint=(1, None), height="30dp")
        self.email_field = self.create_textinput("Введите ваш email", "email")
        email_layout.add_widget(self.email_field)
        email_icon_button = MDIconButton(icon="email")
        email_layout.add_widget(email_icon_button)
        layout.add_widget(email_layout)

        # Увеличиваем отступ между полями для ввода
        layout.add_widget(Widget(size_hint_y=None, height="30dp"))

        password_layout = MDBoxLayout(size_hint=(1, None), height="30dp")
        self.password_field = self.create_textinput("Введите пароль", "password", password=True)
        password_layout.add_widget(self.password_field)
        password_icon_button = MDIconButton(icon="eye")
        password_icon_button.bind(on_release=self.toggle_password_visibility_password)
        password_layout.add_widget(password_icon_button)
        layout.add_widget(password_layout)

        # Увеличиваем отступ между полем для ввода пароля и полем для подтверждения пароля
        layout.add_widget(Widget(size_hint_y=None, height="30dp"))

        confirm_password_layout = MDBoxLayout(size_hint=(1, None), height="30dp")
        self.confirm_password_field = self.create_textinput("Подтвердите пароль", "confirm_password", password=True)
        confirm_password_layout.add_widget(self.confirm_password_field)
        confirm_password_icon_button = MDIconButton(icon="eye")
        confirm_password_icon_button.bind(on_release=self.toggle_password_visibility_confirm)
        confirm_password_layout.add_widget(confirm_password_icon_button)
        layout.add_widget(confirm_password_layout)

        # Увеличиваем отступ между полем для подтверждения пароля и кнопкой регистрации
        layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        register_button = MDRaisedButton(
            text="Зарегистрироваться",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        register_button.bind(on_release=self.on_button_press)
        layout.add_widget(register_button)

        # Добавляем виджет внизу, чтобы сдвинуть содержимое вверх
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
            password=password  # добавляем аргумент password
        )
        return text_input

    def toggle_password_visibility_password(self, instance):
        self.password_field.password = not self.password_field.password
        instance.icon = "eye-off" if self.password_field.password else "eye"

    def toggle_password_visibility_confirm(self, instance):
        self.confirm_password_field.password = not self.confirm_password_field.password
        instance.icon = "eye-off" if self.confirm_password_field.password else "eye"

    def hash_password(self, password):
        hash_object = hashlib.sha256()
        hash_object.update(password.encode('utf-8'))
        return hash_object.hexdigest()

    def on_button_press(self, instance):
        email = self.email_field.text
        password = self.password_field.text
        confirm_password = self.confirm_password_field.text

        # Проверка формата электронной почты
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.show_alert_dialog("Неверный формат электронной почты!")
            return

        # Проверка надежности пароля
        if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[a-zA-Zа-яА-Я]", password):
            self.show_alert_dialog("Пароль должен быть не менее 8 символов и содержать хотя бы 1 букву (английскую или русскую) и 1 цифру!")
            return

        if password == confirm_password:
            hashed_password = self.hash_password(password)  # Хеширование пароля
            response = requests.post('http://localhost:5000/register', data={'email': email, 'password': hashed_password})
            if response.status_code == 200:
                self.show_alert_dialog("Успешная регистрация!")
            else:
                self.show_alert_dialog("Ошибка регистрации!")
        else:
            self.show_alert_dialog("Пароли не совпадают!")

    def show_alert_dialog(self, text):
        self.dialog = MDDialog(title='Уведомление', text=text, size_hint=(0.8, 1),
                          buttons=[MDRaisedButton(text='ОК', on_release=self.close_dialog)])
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

Registration_screen().run()