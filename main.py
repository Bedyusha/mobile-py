import os
import json
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.text import LabelBase
from kivy.core.window import Window

# LabelBase.register(name='Roboto',
#                    fn_regular='Roboto-Thin.ttf',
#                    fn_bold='Roboto-Medium.ttf')

class ImageButton(ButtonBehavior, Image):
    pass

class PetProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(PetProfileScreen, self).__init__(**kwargs)
        self.name = 'pet_profile'
        self.layout = BoxLayout(orientation='horizontal')
        self.info_layout = BoxLayout(orientation='vertical', size_hint=(0.6, 1))
        self.layout.add_widget(self.info_layout)

        # Загрузить сохраненный путь к изображению, если он существует
        self.image_path = self.load_image_path()
        self.image = ImageButton(source=self.image_path, size_hint=(None, None), size=(200, 200), pos_hint={'top': 1, 'left': 1})
        # Установить минимальный и максимальный размер изображения
        self.image.size_hint_min = (100, 100)  # Минимальный размер 100x100 пикселей
        self.image.size_hint_max = (300, 300)  # Максимальный размер 500x500 пикселей
        self.image.bind(on_release=self.open_file_chooser)
        self.layout.add_widget(self.image)

        # Загрузить сохраненную информацию о питомце, если она существует
        self.pet_info = self.load_pet_info()

        # Создать метки и текстовые поля для ввода информации о питомце
        self.create_label_and_textinput('Кличка питомца:', 'pet_name')
        self.create_label_and_textinput('Возраст:', 'pet_age')
        self.create_label_and_textinput('Порода:', 'pet_breed')
        self.create_label_and_textinput('Хозяин:', 'owner_name')

        self.add_widget(self.layout)

    def create_label_and_textinput(self, label_text, info_key):
        # Создать метку
        label = MDLabel(text=label_text, size_hint=(1, 1))
        self.info_layout.add_widget(label)

        # Создать текстовое поле для ввода
        text_input = TextInput(text=self.pet_info.get(info_key, ''), size_hint=(1, 1), background_color=(0.3, 0.3, 0.3, 1), foreground_color=(1, 1, 1, 1))
        text_input.bind(text=self.save_pet_info(info_key))
        self.info_layout.add_widget(text_input)
        
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
    
class MainApp(MDApp):
    def build(self):
        Window.size = (400, 700) 
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        # Создаем список для Navigation Drawer
        self.nav_drawer = MDNavigationDrawer()
        list_drawer = MDList()
        button_names = ['Профиль питомца', 'Button 2', 'Button 3', 'Button 4', 'Button 5', 'Вернуться на главную страницу']
        buttons = [OneLineListItem(text=name) for name in button_names]
        for button in buttons:
            list_drawer.add_widget(button)
        self.nav_drawer.add_widget(list_drawer)

        # Создаем ScreenManager и добавляем в него экран
        sm = ScreenManager()
        screen = Screen(name='screen')
        screen.add_widget(MDRaisedButton(
            text="Hello, World",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        ))

        # Добавляем кнопку для переключения темы
        theme_button = MDIconButton(icon="lightbulb-on-outline",
                                     pos_hint={"right": 1, "top": 1},
                                     on_release=self.switch_theme)
        screen.add_widget(theme_button)

        # Привязываем первую кнопку в списке к переключению на экран профиля питомца
        def switch_to_pet_profile(*args):
            sm.current = 'pet_profile'
        
        buttons[0].bind(on_release=switch_to_pet_profile)

        # Привязываем кнопку "Вернуться на главную страницу" к переключению на главный экран
        def switch_to_main_screen(*args):
            sm.current = 'screen'
        
        buttons[-1].bind(on_release=switch_to_main_screen)

        sm.add_widget(screen)

        pet_profile_screen = PetProfileScreen()
        sm.add_widget(pet_profile_screen)

        # Создаем MDNavigationLayout и добавляем в него ScreenManager и NavigationDrawer
        nav_layout = MDNavigationLayout()
        nav_layout.add_widget(sm)
        nav_layout.add_widget(self.nav_drawer)
        
        return nav_layout

    def switch_theme(self, *args):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        self.nav_drawer.md_bg_color = get_color_from_hex("#2C2C2C") if self.theme_cls.theme_style == "Dark" else get_color_from_hex("#c3c3c3")

MainApp().run()
