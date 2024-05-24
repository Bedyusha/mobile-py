import os
import json
import re
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
from kivymd.uix.snackbar import Snackbar
from kivy.uix.button import Button
from kivymd.uix.pickers import MDDatePicker

class ImageButton(ButtonBehavior, Image):
    pass

class PetProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(PetProfileScreen, self).__init__(**kwargs)
        self.name = 'pet_profile'
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=20)  # Увеличен отступ между виджетами

        # Загрузить сохраненный путь к изображению, если он существует
        self.image_path = self.load_image_path()
        self.image = ImageButton(source=self.image_path, size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5})
        # Установить минимальный и максимальный размер изображения
        self.image.size_hint_min = (100, 100)  # Минимальный размер 100x100 пикселей
        self.image.size_hint_max = (300, 300)  # Максимальный размер 500x500 пикселей
        self.image.bind(on_release=self.open_file_chooser)
        self.layout.add_widget(self.image)

        self.info_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), padding=[10, 20, 10, 20], spacing=30)  # Увеличен отступ между виджетами
        self.layout.add_widget(self.info_layout)

        # Загрузить сохраненную информацию о питомце, если она существует
        self.pet_info = self.load_pet_info()

        # Создать метки и текстовые поля для ввода информации о питомце
        self.text_inputs = {}
        self.text_inputs['pet_name'] = self.create_textinput('Кличка питомца:', 'pet_name')
        self.text_inputs['pet_breed'] = self.create_textinput('Порода:', 'pet_breed')
        self.text_inputs['owner_name'] = self.create_textinput('Хозяин:', 'owner_name')

        # Добавить поля для ввода даты рождения
        self.create_label_and_textinput('Дата рождения:', 'pet_birthday')

        # Загрузить и отобразить сохраненную дату рождения
        if 'birth_date' in self.pet_info:
            year, month, day = self.pet_info['birth_date'].split('-')
            self.text_inputs['day'].text = day
            self.text_inputs['month'].text = month
            self.text_inputs['year'].text = year

        self.add_widget(self.layout)

    def save_date(self, instance, the_date, the_time):
        self.pet_info['birth_date'] = str(the_date)
        with open('pet_info.json', 'w') as json_file:
            json.dump(self.pet_info, json_file)
        # Обновить текстовые поля после сохранения даты
        year, month, day = str(the_date).split('-')
        self.text_inputs['day'].text = day
        self.text_inputs['month'].text = month
        self.text_inputs['year'].text = year

    def create_label_and_textinput(self, label_text, info_key):
        # Создать текстовые поля для ввода даты
        if info_key == 'pet_birthday':
            date_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=35)
            self.text_inputs['day'] = self.create_date_input('День', 'day')
            self.text_inputs['month'] = self.create_date_input('Месяц', 'month')
            self.text_inputs['year'] = self.create_date_input('Год', 'year')
            date_layout.add_widget(self.text_inputs['day'])
            date_layout.add_widget(self.text_inputs['month'])
            date_layout.add_widget(self.text_inputs['year'])
            self.info_layout.add_widget(date_layout)
            return date_layout  # Возвращаем layout с полями для ввода даты
        else:
            text_input = MDTextField(text=self.pet_info.get(info_key, ''), hint_text=label_text, size_hint=(1, None), font_size='15sp', mode="rectangle", line_color_normal=get_color_from_hex("#2C2C2C"), line_color_focus=get_color_from_hex("#2C2C2C"))
            text_input.bind(text=self.save_pet_info(info_key))  # Привязать функцию save_pet_info к событию изменения текста
            self.info_layout.add_widget(text_input)
            return text_input

    def create_date_input(self, hint_text, info_key):
        # Создать текстовое поле для ввода даты
        text_input = MDTextField(text=self.pet_info.get(info_key, ''), hint_text=hint_text, size_hint=(None, None), width=60, font_size='15sp', mode="rectangle", line_color_normal=get_color_from_hex("#2C2C2C"), line_color_focus=get_color_from_hex("#2C2C2C"))
        text_input.bind(on_touch_down=self.show_date_picker)  # Привязать функцию show_date_picker к событию изменения фокуса
        return text_input

    def show_date_picker(self, instance, touch):
        if instance.collide_point(*touch.pos):
            date_picker = MDDatePicker()
            date_picker.bind(on_save=self.save_date)
            date_picker.open()


    def validate_and_save_text(self, info_key):
        def save_text(instance, value):
            # Проверить, является ли значение допустимым (только буквы, тире и пробелы)
            if re.match(r'^[a-zA-Zа-яА-Я\s-]*$', value):
                # Сделать первую букву заглавной
                value = value.capitalize()
                # Сохранить значение текстового поля для ввода в информацию о питомце
                self.pet_info[info_key] = value
                # Сохранить информацию о питомце в файле
                with open('pet_info.json', 'w') as f:
                    json.dump(self.pet_info, f)
            else:
                # Очистить текстовое поле, если значение не является допустимым
                instance.text = ''
        return save_text
        
    def create_textinput(self, hint_text, info_key):
        # Создать текстовое поле для ввода
        text_input = MDTextField(text=self.pet_info.get(info_key, ''), hint_text=hint_text, size_hint=(1, None), font_size='15sp', mode="rectangle", line_color_normal=get_color_from_hex("#2C2C2C"), line_color_focus=get_color_from_hex("#2C2C2C"))
        text_input.bind(text=self.validate_and_save_text(info_key))  # Привязать функцию validate_and_save_text к событию изменения текста
        self.info_layout.add_widget(text_input)
        return text_input

    def save_pet_info(self, info_key):
        def save_text(instance, value):
            # Сохранить значение текстового поля для ввода в информацию о питомце
            self.pet_info[info_key] = value
            # Сохранить информацию о питомце в файле
            with open('pet_info.json', 'w') as f:
                json.dump(self.pet_info, f)
        return save_text

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
