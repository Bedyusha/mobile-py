from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
import requests
import re

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"  # Основной цвет - оранжевый
        self.theme_cls.theme_style = "Dark"  # Темный стиль темы

        layout = MDBoxLayout(orientation='vertical', padding=10)  # Добавлены отступы

        toolbar = Label(text="Регистрация", size_hint_y=None, height="48dp")
        layout.add_widget(toolbar)

        self.email_field = self.create_textinput("Введите ваш email", "email", "email-outline")
        layout.add_widget(self.email_field)

        # Добавляем отступ между полями для ввода
        layout.add_widget(Widget(size_hint_y=None, height="10dp"))

        self.password_field = self.create_textinput("Введите пароль", "password", "lock-outline", password=True)
        layout.add_widget(self.password_field)

        # Добавляем отступ между полем для ввода пароля и полем для подтверждения пароля
        layout.add_widget(Widget(size_hint_y=None, height="10dp"))

        self.confirm_password_field = self.create_textinput("Подтвердите пароль", "confirm_password", "lock-outline", password=True)
        layout.add_widget(self.confirm_password_field)

        # Добавляем отступ между полем для подтверждения пароля и кнопкой регистрации
        layout.add_widget(Widget(size_hint_y=None, height="10dp"))

        register_button = MDRaisedButton(
            text="Зарегистрироваться",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        register_button.bind(on_release=self.on_button_press)
        layout.add_widget(register_button)

        # Добавляем виджет внизу, чтобы сдвинуть содержимое вверх
        layout.add_widget(Widget())

        return layout

    def create_textinput(self, hint_text, info_key, icon, password=False):
        text_input = MDTextField(
            text='',
            hint_text=hint_text,
            size_hint=(1, None),
            font_size='15sp',
            mode="rectangle",
            icon_right=icon,
            line_color_normal=get_color_from_hex("#2C2C2C"),
            line_color_focus=get_color_from_hex("#2C2C2C"),
            password=password  # добавляем аргумент password
        )
        return text_input

    def on_button_press(self, instance):
        email = self.email_field.text
        password = self.password_field.text
        confirm_password = self.confirm_password_field.text

        # Проверка формата электронной почты
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.show_alert_dialog("Неверный формат электронной почты!")
            return

        # Проверка надежности пароля
        if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[a-zA-Z]", password):
            self.show_alert_dialog("Пароль должен быть не менее 8 символов и содержать хотя бы 1 букву и 1 цифру!")
            return

        if password == confirm_password:
            response = requests.post('http://localhost:5000/register', data={'email': email, 'password': password})
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

MainApp().run()
