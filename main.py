from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivymd.uix.button import MDIconButton
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivymd.uix.dialog import MDDialog
#Импорты основных окон
from advice_screen import AdviceScreen
from PetProfileScreen import PetProfileScreen
from feeding_screen import FeedingScreen
from login_screen import LoginScreen
from registration_screen import Registration_screen
#Импорты окон совета advice_screen
from advice.birth_screen_cat import BirthScreen
from advice.teeth import Teeth
from advice.tick_bite import Tick_bite

LabelBase.register(name='Ubuntu',
                   fn_regular='fonts\\Ubuntu-Regular.ttf',
                   fn_bold='fonts\\Ubuntu-Bold.ttf')

resource_add_path('mobile-py\\fonts')

# Зарегистрируйте шрифт (вы можете добавить больше вариантов шрифта, если они доступны)
LabelBase.register(DEFAULT_FONT, "fonts\\Ubuntu-Regular.ttf")

class MainApp(MDApp):
    def build(self):
        Window.size = (400, 700) 
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        # Создаем список для Navigation Drawer
        list_drawer = MDList()
        button_names = ['Профиль питомца', 'Button 2', 'График питания', 'Дресировка', 'Советы на особый случай', 'Выйти из аккаунта']
        buttons = [OneLineListItem(text=name) for name in button_names]
        for button in buttons:
            list_drawer.add_widget(button)

        # Создаем Navigation Drawer и добавляем в него список
        self.nav_drawer = MDNavigationDrawer()
        self.nav_drawer.add_widget(list_drawer)

        # Добавляем кнопку для переключения темы
        theme_button = MDIconButton(icon="lightbulb-on-outline", pos_hint={"right": 1, "top": 1}, on_release=self.switch_theme)
        self.nav_drawer.add_widget(theme_button)

        # Создаем ScreenManager
        sm = ScreenManager()

        # Добавляем экран авторизации
        login_screen = LoginScreen(name='login')
        sm.add_widget(login_screen)

        registration_screen = Registration_screen(name='registration')
        sm.add_widget(registration_screen)

        # Добавляем остальные экраны
        pet_profile_screen = PetProfileScreen(name = 'pet_profile')
        sm.add_widget(pet_profile_screen)

        notification_screen = FeedingScreen(name = 'feeding_screen')
        sm.add_widget(notification_screen)

        advice_screen = AdviceScreen(name='advice')
        sm.add_widget(advice_screen)

        birth_screen_cat = BirthScreen(name='birth_screen_cat')
        sm.add_widget(birth_screen_cat)

        teeth = Teeth(name='teeth')
        sm.add_widget(teeth)

        tick_bite = Tick_bite(name='tick_bite')
        sm.add_widget(tick_bite)

        # Создаем MDNavigationLayout и добавляем в него ScreenManager и NavigationDrawer
        nav_layout = MDNavigationLayout()
        nav_layout.add_widget(sm)
        nav_layout.add_widget(self.nav_drawer)

        return nav_layout

    def switch_theme(self, *args):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        self.nav_drawer.md_bg_color = get_color_from_hex("#2C2C2C") if self.theme_cls.theme_style == "Dark" else get_color_from_hex("#c3c3c3")

    def show_logout_dialog(self, sm):
        self.dialog = MDDialog(title='Выход из аккаунта', text='Вы уверены, что хотите выйти из аккаунта?', size_hint=(0.8, 1),
                          buttons=[MDRaisedButton(text='Да', on_release=lambda *args: self.logout(sm)),
                                   MDRaisedButton(text='Нет', on_release=self.close_dialog)])
        self.dialog.open()

    def logout(self, sm):
        self.dialog.dismiss()
        sm.current = 'login'

    def close_dialog(self, instance):
        self.dialog.dismiss()

MainApp().run()
