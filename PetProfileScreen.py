import os
import json
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField


class ImageButton(ButtonBehavior, Image):
    pass

class PetProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(PetProfileScreen, self).__init__(**kwargs)
        self.name = 'pet_profile'
        self.layout = BoxLayout(orientation='vertical', padding=10)

        # Загрузить сохраненный путь к изображению, если он существует
        self.image_path = self.load_image_path()
        self.image = ImageButton(source=self.image_path, size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5})
        # Установить минимальный и максимальный размер изображения
        self.image.size_hint_min = (100, 100)  # Минимальный размер 100x100 пикселей
        self.image.size_hint_max = (300, 300)  # Максимальный размер 500x500 пикселей
        self.image.bind(on_release=self.open_file_chooser)
        self.layout.add_widget(self.image)

        self.info_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), padding=[10, 20, 10, 20])
        self.layout.add_widget(self.info_layout)

        # Загрузить сохраненную информацию о питомце, если она существует
        self.pet_info = self.load_pet_info()

        # Создать метки и текстовые поля для ввода информации о питомце
        self.text_inputs = {}
        self.text_inputs['pet_name'] = self.create_label_and_textinput('Кличка питомца:', 'pet_name')
        self.text_inputs['pet_age'] = self.create_label_and_textinput('Возраст:', 'pet_age')
        self.text_inputs['pet_breed'] = self.create_label_and_textinput('Порода:', 'pet_breed')
        self.text_inputs['owner_name'] = self.create_label_and_textinput('Хозяин:', 'owner_name')

        # Создать кнопку "Сохранить"
        save_button = MDRaisedButton(text="Сохранить", pos_hint={"center_x": 0.5}, size_hint=(None, None), size=(300, 50))
        save_button.bind(on_release=self.save_all_info)
        self.layout.add_widget(save_button)

        self.add_widget(self.layout)

    def create_label_and_textinput(self, label_text, info_key):
        # Создать метку
        label = MDLabel(text=label_text, size_hint=(1, None), height=30)
        self.info_layout.add_widget(label)

        # Создать текстовое поле для ввода
        text_input = MDTextField(text=self.pet_info.get(info_key, ''), size_hint=(1, None), height=30, mode="rectangle", line_color_normal=get_color_from_hex("#2C2C2C"), line_color_focus=get_color_from_hex("#2C2C2C"))
        self.info_layout.add_widget(text_input)
        return text_input
    
    def save_all_info(self, *args):
        # Сохранить информацию из всех текстовых полей
        for info_key, text_input in self.text_inputs.items():
            self.pet_info[info_key] = text_input.text

        # Сохранить информацию о питомце в файле
        with open('pet_info.json', 'w') as f:
            json.dump(self.pet_info, f)

    def load_pet_info(self):
        # Загрузить информацию о питомце из файла, если он существует
        if os.path.exists('pet_info.json'):
            with open('pet_info.json', 'r') as f:
                return json.load(f)
        # Вернуть пустой словарь, если файл не существует
        return {}

    def open_file_chooser(self, *args):
        self.file_chooser = FileChooserIconView(size_hint=(1, 0.4))
        self.file_chooser.bind(on_submit=self.load_image)
        self.popup = Popup(title='Выберите изображение', content=self.file_chooser, size_hint=(0.9, 0.9))
        self.popup.open()

    def load_image(self, instance, value, touch):
        if value:
            self.image.source = value[0]
            # Сохранить путь к изображению
            self.save_image_path(value[0])
            instance.unbind(on_submit=self.load_image)
            self.popup.dismiss(force=True)

    def save_image_path(self, path):
        # Сохранить путь к изображению в файле
        with open('image_path.json', 'w') as f:
            json.dump({'image_path': path}, f)

    def load_image_path(self):
        # Загрузить путь к изображению из файла, если он существует
        if os.path.exists('image_path.json'):
            with open('image_path.json', 'r') as f:
                data = json.load(f)
                return data['image_path']
        # Вернуть путь к изображению по умолчанию, если файл не существует
        return 'cat-defolt.png'
