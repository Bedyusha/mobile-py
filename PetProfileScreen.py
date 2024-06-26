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
from kivymd.uix.dialog import MDDialog

class ImageButton(ButtonBehavior, Image):
    pass

class PetProfileScreen(Screen):
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        app.nav_drawer.set_state("open")
        app.nav_drawer.disabled = False

        # Загрузить информацию о профиле питомца
        threading.Thread(target=self.load_pet_profile).start()

    def load_pet_profile(self):
        email = MDApp.get_running_app().user_email
        response = requests.get(f'http://localhost:5000/pet_profile?email={email}')
        if response.status_code == 200:
            pet_profile = response.json()
            if pet_profile is not None:
                fields = {
                    'pet_name': self.text_inputs['pet_name'],
                    'pet_weight': self.text_inputs['pet_weight'],
                    'owner_email': self.text_inputs['owner_name'],
                    'pet_birthday': self.date_picker_input,
                    'image_path': self.image, 
                    'pet_type': self.pet_type_spinner  
                }
                for field, widget in fields.items():
                    value = pet_profile.get(field)
                    if value is not None:  # проверить, что значение не None
                        Clock.schedule_once(lambda dt, w=widget, v=value: self.update_widget(w, v))

    def update_widget(self, widget, value):
        if isinstance(widget, Spinner):  # Проверьте, является ли виджет выпадающим списком
            if value in widget.values:  # Проверьте, есть ли значение в списке значений
                widget.text = value  # Установите значение
            else:
                widget.text = ''  # Очистите значение
        elif widget is self.image:
            widget.source = value if value else 'cat-defolt.png'  # Если значение пустое, установите изображение по умолчанию
        else:
            widget.text = str(value) if value else ''  # Если значение пустое, очистите текст

    def save_pet_profile(self, instance):
        # Сохранить профиль питомца в отдельном потоке
        threading.Thread(target=self.save_pet_profile_thread, args=(instance,)).start()

    def save_pet_profile_thread(self, instance):
        email = MDApp.get_running_app().user_email
        pet_name = self.text_inputs['pet_name'].text
        pet_weight_text = self.text_inputs['pet_weight'].text
        if pet_weight_text:  # Проверить, что строка не пустая
            pet_weight = int(pet_weight_text)
        else:
            # Здесь вы можете установить значение по умолчанию или показать сообщение об ошибке
            Clock.schedule_once(lambda dt: self.show_alert_dialog("Ошибка сохранения данных, некоректное значение"))
        owner_email = self.text_inputs['owner_name'].text
        pet_birthday = self.date_picker_input.text
        image_path = self.image.source  # добавить путь к изображению
        pet_type = self.pet_type_spinner.text  # добавить тип питомца

        data = {
            'email': email,
            'pet_name': pet_name,
            'pet_weight': pet_weight,
            'owner_email': owner_email,
            'pet_birthday': pet_birthday,
            'image_path': image_path,  # добавить путь к изображению
            'pet_type': pet_type  # добавить тип питомца
        }

        response = requests.post('http://localhost:5000/save_pet_profile', json=data)
        if response.status_code == 200:
            print("Профиль питомца успешно сохранен!")
            Clock.schedule_once(lambda dt: self.show_alert_dialog("Информация обновлена успешно!"))
        else:
            print(f"Ошибка сохранения профиля питомца: {response.status_code}")
            Clock.schedule_once(lambda dt: self.show_alert_dialog("Ошибка сохранения данных, некоректное значение"))



    def show_alert_dialog(self, text):
        self.dialog = MDDialog(title='Уведомление', text=text, size_hint=(0.8, 1),
                          buttons=[MDRaisedButton(text='ОК', on_release=self.close_dialog)])
        self.dialog.open()
    def close_dialog(self, instance):
        self.dialog.dismiss()

    def clear_fields(self):
        # Очистить текстовые поля
        for text_input in self.text_inputs.values():
            text_input.text = ''
        # Очистить выпадающий список
        self.pet_type_spinner.text = 'Выбирите тип питомца'
        # Очистить изображение
        self.image.source = 'cat-defolt.png'

    def __init__(self, **kwargs):
        super(PetProfileScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=20)
        self.text_inputs = {}  # Инициализация словаря для текстовых полей

        self.image = ImageButton(source='cat-defolt.png', size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5})
        self.image.bind(on_release=self.open_file_chooser)
        self.layout.add_widget(self.image)

        self.info_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), padding=[10, 20, 10, 20], spacing=20)
        self.layout.add_widget(self.info_layout)

        self.pet_type_spinner = Spinner(
            # доступные значения
            values=('Кот', 'Собака'),
            # первоначально выбранное значение
            text='Выберите тип питомца',
            # размер
            size_hint=(1, None),
            height=30
        )
        self.info_layout.add_widget(self.pet_type_spinner)

        self.text_inputs['pet_name'] = self.create_textinput('Кличка питомца:')

        self.text_inputs['pet_weight'] = self.create_textinput('Вес питомца(граммы):')
        self.text_inputs['pet_weight'].input_filter = 'int'

        self.text_inputs['owner_name'] = self.create_textinput('Хозяин:')
        self.text_inputs['owner_name'].readonly = True


        self.date_picker_input = MDTextField(hint_text='Дата рождения питомца:', size_hint=(1, None), font_size='15sp', mode="rectangle")
        self.date_picker_input.bind(on_touch_down=self.show_date_picker)
        self.info_layout.add_widget(self.date_picker_input)

        # Добавить кнопку "Сохранить изменения"
        self.save_button = MDRaisedButton(text='Сохранить изменения', size_hint=(1, None))
        self.save_button.bind(on_release=self.save_pet_profile)
        self.layout.add_widget(self.save_button)

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
