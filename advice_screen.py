# advice_screen.py
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

class AdviceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[10, 50, 10, 10])
        self.add_widget(layout)

        label = MDLabel(
            text="Выбирите сценарий",
            halign="center",
            theme_text_color="Secondary",
            font_style="H5",
            size_hint=(1, None),
            height="24dp"
        )
        layout.add_widget(label)

        self.search_field = MDTextField(
            hint_text="Поиск",
            pos_hint={"center_x": 0.5},
            size_hint=(1, None),
            height="48dp"
        )
        self.search_field.bind(text=self.on_text)
        layout.add_widget(self.search_field)

        self.scroll_view = ScrollView()
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scroll_view.add_widget(self.list_layout)
        layout.add_widget(self.scroll_view)

        self.items = ["Роды питомца", "Выпадение зубов", "Укус клеща", "Рвота у питомца", "Что еще"]
        self.update_list()

    def on_text(self, instance, value):
        self.update_list()

    def update_list(self):
        self.list_layout.clear_widgets()
        for item in self.items:
            if self.search_field.text.lower() in item.lower():
                list_item = OneLineListItem(text=item)
                self.list_layout.add_widget(list_item)
