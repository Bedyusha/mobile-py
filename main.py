from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class PetProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(PetProfileScreen, self).__init__(**kwargs)
        self.name = 'pet_profile'
        self.layout = BoxLayout(orientation='horizontal')
        self.image = Image(source='default_pet_image.jpg', size_hint=(0.5, 1))
        self.image.bind(on_release=self.open_file_chooser)
        self.layout.add_widget(self.image)
        self.text_input = TextInput(hint_text='Введите имя питомца', size_hint=(0.5, 1))
        self.layout.add_widget(self.text_input)
        self.file_chooser = FileChooserIconView(size_hint=(1, 0.4))
        self.add_widget(self.layout)

    def open_file_chooser(self, *args):
        popup = Popup(title='Выберите изображение', content=self.file_chooser, size_hint=(0.9, 0.9))
        self.file_chooser.bind(on_submit=self.load_image)
        popup.open()

    def load_image(self, instance, value, touch):
        self.image.source = value[0]
        instance.unbind(on_submit=self.load_image)

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        # Создаем список для Navigation Drawer
        self.nav_drawer = MDNavigationDrawer()
        list_drawer = MDList()
        for i in range(5):
            list_drawer.add_widget(OneLineListItem(text=f'Button {i+1}'))
        self.nav_drawer.add_widget(list_drawer)

        # Создаем ScreenManager и добавляем в него экран
        sm = ScreenManager()
        screen = Screen(name='screen')
        screen.add_widget(MDRaisedButton(
            text="Hello, World",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        ))
        screen.add_widget(self.nav_drawer)

        # Добавляем кнопку для переключения темы
        theme_button = MDIconButton(icon="lightbulb-on-outline",
                                     pos_hint={"right": 1, "top": 1},
                                     on_release=self.switch_theme)
        screen.add_widget(theme_button)

        # Добавляем экран профиля питомца


        # Привязываем первую кнопку в списке к переключению на экран профиля питомца
        def switch_to_pet_profile(*args):
            sm.current = 'pet_profile'
        
        list_drawer.children[0].bind(on_release=switch_to_pet_profile)

        sm.add_widget(screen)

        pet_profile_screen = PetProfileScreen()
        sm.add_widget(pet_profile_screen)
        
        return sm

    def switch_theme(self, *args):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        self.nav_drawer.md_bg_color = get_color_from_hex("#2C2C2C") if self.theme_cls.theme_style == "Dark" else get_color_from_hex("#c3c3c3")

MainApp().run()
