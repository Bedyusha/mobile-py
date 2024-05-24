from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
import json

class MainApp(MDApp):
    def build(self):
        self.pet_info = {}
        button = Button(text="Выберите дату рождения")
        button.bind(on_release=self.show_date_picker)
        return button

    def show_date_picker(self, instance):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.save_date)
        date_picker.open()

    def save_date(self, instance, the_date, the_time):
        self.pet_info['birth_date'] = str(the_date)
        with open('pet_info.json', 'w') as json_file:
            json.dump(self.pet_info, json_file)

MainApp().run()
