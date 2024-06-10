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
from kivymd.uix.dialog import MDDialog

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
        threading.Thread(target=self.load_pet_profile).start()     

    def load_pet_profile(self):
        email = MDApp.get_running_app().user_email
        response = requests.get(f'http://localhost:5000/pet_profile?email={email}')
        if response.status_code == 200:
            pet_profile = response.json()
            if pet_profile is not None:
                Clock.schedule_once(lambda dt: self.update_ui(pet_profile))

    def update_ui(self, pet_profile):
        self.text_inputs['image_text'].text = pet_profile['pet_name'] if pet_profile['pet_name'] is not None else "информации нет"
        self.text_inputs['last_feed'].text = pet_profile['last_feed'] if pet_profile['last_feed'] is not None else "информации нет"
        self.image.source = pet_profile['image_path'] if pet_profile['image_path'] is not None else "default_image.png"
        pet_type = pet_profile['pet_type'] if pet_profile['pet_type'] is not None else ""
        pet_birthday = pet_profile['pet_birthday'] if pet_profile['pet_birthday'] is not None else ""
        pet_weight = pet_profile['pet_weight'] if pet_profile['pet_weight'] is not None else 0
        last_feed = pet_profile['last_feed'] if pet_profile['last_feed'] is not None else None
        Clock.schedule_once(lambda dt: self.calculate_feed(pet_type, pet_weight, pet_birthday))
        self.calculate_next_feed(last_feed)

    def __init__(self, **kwargs):
        super(FeedingScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.image = ImageButton(source='cat-defolt.png', size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5})
        self.layout.add_widget(self.image)
        
        self.info_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), padding=[10, 20, 10, 20], spacing=10)
        self.layout.add_widget(self.info_layout)

        self.text_inputs = {}  
        self.text_inputs['image_text'] = self.create_special_text('Кличка питомца:')

        self.text_inputs['last_feed'] = self.create_special_text('Дата прошлого кормления:')

        self.text_inputs['calories'] = self.create_text('Введите калорийность корма (ккал/100г):', size_hint_y=0.9)

        self.text_inputs['next_feedding'] = self.create_text('Рекомендованое время кормления:', size_hint_y=0.9)
        self.text_inputs['next_feedding'].readonly = True

        self.text_inputs['food'] = self.create_text('Рекомендованое питание:', size_hint_y=0.9)
        self.text_inputs['food'].readonly = True

        self.layout.add_widget(Widget(size_hint_y=0.4))

        self.save_button = MDRaisedButton(text='Расчитать и записать кормление', size_hint=(1, None))
        self.save_button.bind(on_release=self.feed_pet)
        self.layout.add_widget(self.save_button)

        self.add_widget(self.layout)

    def create_text(self, hint_text, size_hint_y=None):
        text_input = MDTextField(hint_text=hint_text, size_hint=(1, size_hint_y), font_size='15sp', mode="rectangle")
        self.layout.add_widget(text_input)
        return text_input  
    
    def create_special_text(self, hint_text):
        text_input = MDTextField(hint_text=hint_text, size_hint=(1, None), font_size='20sp')
        text_input.background_color = (1, 1, 1, 1)  
        text_input.color = (0, 0, 0, 1)  
        text_input.readonly = True  # Сделать поле только для чтения
        self.layout.add_widget(text_input)
        return text_input  
        
    def calculate_feed(self, pet_type, pet_weight, pet_birthday):
        # Получить калорийность корма из текстового поля
        calories_text = self.text_inputs['calories'].text
        if calories_text:  # Проверить, что строка не пустая
            calories_per_100g = float(calories_text)
        else:
            # Здесь вы можете установить значение по умолчанию или показать сообщение об ошибке
            calories_per_100g = 0  # Значение по умолчанию
            print("Пожалуйста, введите калорийность корма.")

        # Преобразование веса из грамм в килограммы
        pet_weight_kg = pet_weight / 1000

        birthday = datetime.strptime(pet_birthday, '%Y-%m-%d')
        now = datetime.now()
        pet_age_months = (now.year - birthday.year) * 12 + now.month - birthday.month

     # Определение типа и количества корма на основе веса и возраста питомца
        if pet_type == 'Кот':
            # Добавить логику для расчета корма для кошек
            resting_calorie = pet_weight_kg * 50 # Калорийность в состоянии покоя
            if pet_age_months < 12:  # Для котят
                daily_calories = resting_calorie * 2 # Умножаем на коэффициент 2 для котят
            else:  # Для взрослых кошек
                daily_calories = resting_calorie # Для взрослых кошек и котят старше 12 месяцев

            if calories_per_100g == 0:
                amount_dry=0
                daily_calories=0
            else:
                # Преобразование количества калорий в граммах корма
                amount_dry = (daily_calories * 100) / calories_per_100g

            amount_dry = round(amount_dry, 2)

                # Заполнение поля "Рекомендованое питание:" информацией о корме
            Clock.schedule_once(lambda dt: self.update_food_text( f'Сухой корм: {amount_dry} г, {daily_calories} ккал, разбить на 3-4 кормежки'))

        elif pet_type == 'Собака':
            # Добавить логику для расчета корма для собак
            resting_calorie = pet_weight_kg * 40 # Калорийность в состоянии покоя
            if pet_age_months <= 4:
                daily_calories = resting_calorie * 3 # Умножаем на коэффициент 3 для щенков до 4 месяцев
            elif pet_age_months <= 6:
                daily_calories = resting_calorie * 2 # Умножаем на коэффициент 2 для щенков до полугода
            elif pet_age_months <= 8:
                daily_calories = resting_calorie * 1.2 # Умножаем на коэффициент 1.2 для щенков до 8 месяцев
            else:
                daily_calories = resting_calorie # Для взрослых собак и щенков старше 8 месяцев

            if calories_per_100g == 0:
                amount_dry=0
                daily_calories=0
            else:
                # Преобразование количества калорий в граммах корма
                amount_dry = (daily_calories * 100) / calories_per_100g

            amount_dry = round(amount_dry, 2)

            # Заполнение поля "Рекомендованое питание:" информацией о корме
            Clock.schedule_once(lambda dt: self.update_food_text( f'Сухой корм: {amount_dry} г, {daily_calories} ккал, разбить на 1-2 кормёжки'))

    def update_food_text(self, text):
        self.text_inputs['food'].text = text

    def feed_pet(self, instance):
        # Запустите функцию send_feed_request в отдельном потоке
        threading.Thread(target=self.send_feed_request).start()
        Clock.schedule_once(lambda dt: self.show_alert_dialog("Информация обновлена успешно!"))
    def show_alert_dialog(self, text):
        self.dialog = MDDialog(title='Уведомление', text=text, size_hint=(0.8, 1),
                          buttons=[MDRaisedButton(text='ОК', on_release=self.close_dialog)])
        self.dialog.open()
    def close_dialog(self, instance):
        self.dialog.dismiss()
        

    def send_feed_request(self):
        # Вызовите функцию calculate_feed перед отправкой запроса
        email = MDApp.get_running_app().user_email
        response = requests.get(f'http://localhost:5000/pet_profile?email={email}')
        if response.status_code == 200:
            pet_profile = response.json()
            if pet_profile is not None:
                pet_type = pet_profile['pet_type'] if pet_profile['pet_type'] is not None else ""
                pet_birthday = pet_profile['pet_birthday'] if pet_profile['pet_birthday'] is not None else ""
                pet_weight = pet_profile['pet_weight'] if pet_profile['pet_weight'] is not None else 0
                self.calculate_feed(pet_type, pet_weight, pet_birthday)

        # Затем продолжайте с сохранением профиля питомца
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        email = MDApp.get_running_app().user_email
        data = {'email': email, 'last_feed': current_time}
        response = requests.post('http://localhost:5000/save_last_feed', json=data)
        if response.status_code == 200:
            print("Время последнего кормления успешно сохранено!")
            Clock.schedule_once(lambda dt: self.update_last_feed(current_time))
        else:
            print(f"Ошибка сохранения времени последнего кормления: {response.status_code}")


    def update_last_feed(self, current_time):
        self.text_inputs['last_feed'].text = current_time

        last_feed_time = datetime.now()
        next_feed_time = last_feed_time + timedelta(hours=6)
        self.text_inputs['next_feedding'].text = next_feed_time.strftime("%Y-%m-%d %H:%M:%S")

    def calculate_next_feed(self, last_feed):
        if last_feed is not None:
            last_feed_time = datetime.strptime(last_feed, "%Y-%m-%d %H:%M:%S")
            next_feed_time = last_feed_time + timedelta(hours=6)
            self.text_inputs['next_feedding'].text = next_feed_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.text_inputs['next_feedding'].text = "Информации нет"




