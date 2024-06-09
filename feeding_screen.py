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
from datetime import datetime, timedelta

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
        pet_weight = pet_profile['pet_weight'] if pet_profile['pet_weight'] is not None else 0
        last_feed = pet_profile['last_feed'] if pet_profile['last_feed'] is not None else None
        # Вызовите функцию calculate_feed в основном потоке
        Clock.schedule_once(lambda dt: self.calculate_feed(pet_type, pet_weight, pet_birthday))
        self.calculate_next_feed(last_feed)

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

        self.save_button = MDRaisedButton(text='Покормить', size_hint=(1, None))
        self.save_button.bind(on_release=self.feed_pet)
        self.layout.add_widget(self.save_button)

        self.add_widget(self.layout)

    def create_text(self, hint_text, size_hint_y=None):
        text_input = MDTextField(hint_text=hint_text, size_hint=(1, size_hint_y), font_size='15sp', mode="rectangle")
        self.layout.add_widget(text_input)
        return text_input  # Вернуть созданный MDTextField
    
    def create_special_text(self, hint_text):
        text_input = MDTextField(hint_text=hint_text, size_hint=(1, None), font_size='20sp')
        text_input.background_color = (1, 1, 1, 1)  # Изменить цвет фона на белый
        text_input.color = (0, 0, 0, 1)  # Изменить цвет текста на черный
        #text_input.readonly = True  # Сделать поле только для чтения
        self.layout.add_widget(text_input)
        return text_input  # Вернуть созданный TextInput
        
    def calculate_feed(self, pet_type, pet_weight, pet_birthday):
        # Преобразование веса из грамм в килограммы
        pet_weight_kg = pet_weight / 1000

        birthday = datetime.strptime(pet_birthday, '%Y-%m-%d')
        now = datetime.now()
        pet_age_months = (now.year - birthday.year) * 12 + now.month - birthday.month
        print(pet_type,pet_weight,pet_age_months)
        # Определение типа и количества корма на основе веса и возраста кота
        if pet_type == 'Кот':
            if pet_age_months < 12:  # Для котят
                if pet_age_months <= 2:
                    amount_dry = 30 + (pet_weight_kg - 1) * 10  # 30-40 г
                    amount_wet = 170 + (pet_weight_kg - 1) * 40  # 170-210 г
                elif pet_age_months <= 4:
                    amount_dry = 35 + (pet_weight_kg - 2) * 15  # 35-60 г
                    amount_wet = 200 + (pet_weight_kg - 2) * 20  # 200-240 г
                elif pet_age_months <= 6:
                    amount_dry = 50 + (pet_weight_kg - 4) * 10  # 50-70 г
                    amount_wet = 210 + (pet_weight_kg - 4) * 22.5  # 210-300 г
                else:  # 6-12 месяцев
                    amount_dry = 60 + (pet_weight_kg - 6) * 10  # 60-80 г
                    amount_wet = 170 + (pet_weight_kg - 6) * 17  # 170-255 г
            else:  # Для взрослых кошек
                amount_dry = 45 + (pet_weight_kg - 3) * 10  # 45 г + 10 г на каждый дополнительный килограмм
                if pet_weight_kg <= 3:
                    amount_wet = 190  # 190-200 г
                elif pet_weight_kg <= 4:
                    amount_wet = 230  # 230-240 г
                elif pet_weight_kg <= 5:
                    amount_wet = 250  # 250-260 г
                else:
                    amount_wet = 300  # Более 300 г
        else:
            # Здесь вы можете добавить логику для расчета корма для собак
            amount_dry = 0
            amount_wet = 0
        print(amount_dry,amount_wet)
        # Заполнение поля "Рекомендованое питание:" информацией о корме
        self.text_inputs['food'].text = f'Сухой корм: {amount_dry / 4} г или Влажный корм: {amount_wet / 4} г'

    def feed_pet(self, instance):
        # Получить текущую дату и время
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        # Отправить текущую дату и время на сервер
        email = MDApp.get_running_app().user_email
        data = {'email': email, 'last_feed': current_time}
        response = requests.post('http://localhost:5000/save_last_feed', json=data)
        if response.status_code == 200:
            print("Время последнего кормления успешно сохранено!")
        else:
            print(f"Ошибка сохранения времени последнего кормления: {response.status_code}")

        # Обновить поле "Дата прошлого кормления"
        self.text_inputs['last_feed'].text = current_time

        last_feed_time = datetime.now()
        next_feed_time = last_feed_time + timedelta(hours=6)
        self.text_inputs['next_feedding'].text = next_feed_time.strftime("%Y-%m-%d %H:%M:%S")

    def calculate_next_feed(self, last_feed):
        # Проверка, что last_feed не None
        if last_feed is not None:
            # Преобразование строки last_feed в объект datetime
            last_feed_time = datetime.strptime(last_feed, "%Y-%m-%d %H:%M:%S")
            # Вычисление времени следующего кормления путем добавления 6 часов к времени последнего кормления
            next_feed_time = last_feed_time + timedelta(hours=6)
            # Запись времени следующего кормления в поле "Рекомендованое время кормления:"
            self.text_inputs['next_feedding'].text = next_feed_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.text_inputs['next_feedding'].text = "Информации нет"




