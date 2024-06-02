from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.widget import Widget
from kivymd.uix.button import MDRaisedButton

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"  # Основной цвет - оранжевый
        self.theme_cls.theme_style = "Dark"  # Темный стиль темы

        layout = MDBoxLayout(orientation='vertical', padding=10)  # Добавлены отступы

        toolbar = Label(text="Регистрация", size_hint_y=None, height="48dp")
        layout.add_widget(toolbar)

        email_field = self.create_textinput("Введите ваш email", "email", "email-outline")
        layout.add_widget(email_field)

        # Добавляем отступ между полями для ввода
        layout.add_widget(Widget(size_hint_y=None, height="10dp"))

        password_field = self.create_textinput("Введите пароль", "password", "lock-outline")
        layout.add_widget(password_field)

        # Добавляем отступ между полем для ввода пароля и кнопкой регистрации
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

    def create_textinput(self, hint_text, info_key, icon):
        text_input = MDTextField(
            text='',
            hint_text=hint_text,
            size_hint=(1, None),
            font_size='15sp',
            mode="rectangle",
            icon_right=icon,
            line_color_normal=get_color_from_hex("#2C2C2C"),
            line_color_focus=get_color_from_hex("#2C2C2C")
        )
        text_input.bind(text=self.validate_and_save_text(info_key))
        return text_input
    

    def validate_and_save_text(self, info_key):
        def save_text(instance, value):
            print(f"Saved {info_key}: {value}")
        return save_text

    def on_button_press(self, instance):
        print("Button pressed")

MainApp().run()
