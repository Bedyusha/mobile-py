from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.app import MDApp
import requests
from kivymd.uix.button import MDRaisedButton
import threading
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget


class ImageButton(ButtonBehavior, Image):
    pass

class MyWidget(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = True  # Включить многострочный режим
        self.size_hint_y = None  # Отключить автоматическую высоту
        self.height = self.texture_size[1]  # Установить высоту равной высоте содержимого

class FeedingScreen(Screen):
    def on_enter(self):
        # Вызовите функцию load_pet_profile при входе на экран
        threading.Thread(target=self.load_pet_profile).start()

    def load_pet_profile(self):
        email = MDApp.get_running_app().user_email
        response = requests.get(f'http://localhost:5000/pet_profile?email={email}')
        if response.status_code == 200:
            pet_profile = response.json()
            if pet_profile is not None:
                # Используйте Clock.schedule_once для обновления интерфейса в основном потоке
                Clock.schedule_once(lambda dt: self.update_ui(pet_profile))

    def update_ui(self, pet_profile):
        self.text_inputs['image_text'].text = pet_profile['pet_name'] if pet_profile['pet_name'] is not None else "информации нет"
        self.text_inputs['last_feed'].text = pet_profile['last_feed'] if pet_profile['last_feed'] is not None else "информации нет"
        self.image.source = pet_profile['image_path'] if pet_profile['image_path'] is not None else "default_image.png"
        pet_type = pet_profile['pet_type'] if pet_profile['pet_type'] is not None else ""
        pet_birthday = pet_profile['pet_birthday'] if pet_profile['pet_birthday'] is not None else ""

    def __init__(self, **kwargs):
        super(FeedingScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=20)

        # Добавить картинку в верхней части экрана
        self.image = ImageButton(source='cat-defolt.png', size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5})
        self.layout.add_widget(self.image)
        
        self.info_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), padding=[10, 20, 10, 20], spacing=20)
        self.layout.add_widget(self.info_layout)

        # Добавить особое поле ниже картинки
        self.text_inputs = {}  # Инициализация словаря для текстовых полей
        self.text_inputs['image_text'] = self.create_special_text('Кличка питомца')

        # Добавить два текстовых поля
        self.text_inputs['last_feed'] = self.create_special_text('Дата прошлого кормления')

        self.text_inputs['next_feedding'] = self.create_text('Рекомендованое время кормления:', size_hint_y=0.9)
        self.text_inputs['next_feedding'].readonly = True

        self.text_inputs['food'] = self.create_text('Рекомендованое питание:', size_hint_y=0.9)
        self.text_inputs['food'].readonly = True

        self.layout.add_widget(Widget(size_hint_y=0.4))
        # Добавить кнопку "Покормить" в самом низу
        self.save_button = MDRaisedButton(text='Покормить', size_hint=(1, None))
        self.layout.add_widget(self.save_button)

        self.add_widget(self.layout)

    def create_text(self, hint_text, size_hint_y=None):
        text_input = MDTextField(hint_text=hint_text, size_hint=(1, size_hint_y), font_size='20sp', mode="rectangle")
        self.layout.add_widget(text_input)
        return text_input  # Вернуть созданный MDTextField
    
    def create_special_text(self, hint_text):
        text_input = MDTextField(hint_text=hint_text, size_hint=(1, None), font_size='20sp')
        text_input.background_color = (1, 1, 1, 1)  # Изменить цвет фона на белый
        text_input.color = (0, 0, 0, 1)  # Изменить цвет текста на черный
        #text_input.readonly = True  # Сделать поле только для чтения
        self.layout.add_widget(text_input)
        return text_input  # Вернуть созданный TextInput
