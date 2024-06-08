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

class ImageButton(ButtonBehavior, Image):
    pass

class PetProfileScreen(Screen):
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        app.nav_drawer.set_state("close")
        app.nav_drawer.disabled = False

        # Загрузить информацию о профиле питомца
        self.load_pet_profile()

    def load_pet_profile(self):
        email = MDApp.get_running_app().user_email
        response = requests.get(f'http://localhost:5000/pet_profile?email={email}')
        if response.status_code == 200:
            pet_profile = response.json()
            if pet_profile is not None:
                self.text_inputs['pet_name'].text = pet_profile.get('pet_name', '')
                self.text_inputs['pet_breed'].text = pet_profile.get('pet_breed', '')
                self.text_inputs['owner_name'].text = pet_profile.get('owner_email', '')
            else:
                print("Получен пустой ответ от сервера")
        else:
            print(f"Ошибка запроса: {response.status_code}")

    def __init__(self, **kwargs):
        super(PetProfileScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=20)
        self.text_inputs = {}  # Инициализация словаря для текстовых полей

        self.image = ImageButton(source='cat-defolt.png', size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5})
        self.image.bind(on_release=self.open_file_chooser)
        self.layout.add_widget(self.image)

        self.info_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), padding=[10, 20, 10, 20], spacing=30)
        self.layout.add_widget(self.info_layout)

        self.text_inputs['pet_name'] = self.create_textinput('Кличка питомца:')
        print("Поле 'pet_name' инициализировано")
        self.text_inputs['pet_breed'] = self.create_textinput('Порода:')
        print("Поле 'pet_breed' инициализировано")
        self.text_inputs['owner_name'] = self.create_textinput('Хозяин:')
        print("Поле 'owner_name' инициализировано")

        self.date_picker_input = MDTextField(hint_text='Дата рождения:', size_hint=(1, None), font_size='15sp', mode="rectangle")
        self.date_picker_input.bind(on_touch_down=self.show_date_picker)
        self.info_layout.add_widget(self.date_picker_input)

        self.add_widget(self.layout)

    def create_textinput(self, hint_text):
        text_input = MDTextField(hint_text=hint_text, size_hint=(1, None), font_size='15sp', mode="rectangle")
        self.info_layout.add_widget(text_input)
        return text_input  # Вернуть созданный MDTextField


    def show_date_picker(self, instance, touch):
        if instance.collide_point(*touch.pos):
            date_picker = MDDatePicker()
            date_picker.bind(on_save=self.on_date_select)
            date_picker.open()

    def on_date_select(self, instance, value, date_range):
        self.date_picker_input.text = str(value)

    def open_file_chooser(self, *args):
        self.file_chooser = FileChooserIconView(size_hint=(1, 0.4))
        self.file_chooser.filters = ['*.jpg', '*.png', '*.jpeg', '*.gif']
        self.file_chooser.bind(on_submit=self.load_image)
        self.popup = Popup(title='Выберите изображение', content=self.file_chooser, size_hint=(0.9, 0.9))
        self.popup.open()

    def load_image(self, instance, value, touch):
        if value:
            self.image.source = value[0]
            instance.unbind(on_submit=self.load_image)
            self.popup.dismiss(force=True)
