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
import sqlite3
from kivymd.uix.list import OneLineIconListItem
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import IconLeftWidget
# Импорты основных окон
from advice_screen import AdviceScreen
from PetProfileScreen import PetProfileScreen
from feeding_screen import FeedingScreen
from training_screen import TrainingScreen
from login_screen import LoginScreen
from registration_screen import RegistrationScreen  # Добавьте импорт экрана регистрации
# Импорты окон совета advice_screen
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

        list_drawer = MDList()
        button_names = ['Профиль питомца', 'График питания', 'Дресировка', 'Советы на особый случай', 'Выйти из аккаунта']
        icons = ['cat', 'bowl', 'paw', 'information', 'logout']  # Примеры иконок

        buttons = []
        for name, icon in zip(button_names, icons):
            item = OneLineIconListItem(text=name)
            item.add_widget(IconLeftWidget(icon=icon))
            buttons.append(item)
            list_drawer.add_widget(item)

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

        # Привязываем первую кнопку в списке к переключению на экран профиля питомца
        def switch_to_pet_profile(*args):
            sm.current = 'pet_profile'
        buttons[0].bind(on_release=switch_to_pet_profile)

        def switch_to_feeding_screen(*args):
            sm.current = 'feeding_screen'
        buttons[1].bind(on_release=switch_to_feeding_screen)

        def switch_to_training_screen(*args):
            sm.current = 'training_screen'
        buttons[2].bind(on_release=switch_to_training_screen)

        # Привязываем кнопку "Советы на особый случай" к переключению на экран советов
        def switch_to_advice_screen(*args):
            sm.current = 'advice'
        buttons[3].bind(on_release=switch_to_advice_screen)

        # Привязываем кнопку "Вернуться на главную страницу" к переключению на главный экран
        def switch_to_login_screen(*args):
            sm.current = 'login' 
        buttons[-1].bind(on_release=switch_to_login_screen)

        # Добавляем остальные экраны
        pet_profile_screen = PetProfileScreen(name = 'pet_profile')
        sm.add_widget(pet_profile_screen)

        registration_screen = RegistrationScreen(name='registration')
        sm.add_widget(registration_screen)

        notification_screen = FeedingScreen(name = 'feeding_screen')
        sm.add_widget(notification_screen)
        
        notification_screen = TrainingScreen(name = 'training_screen')
        sm.add_widget(notification_screen)

        advice_screen = AdviceScreen(name='advice')
        sm.add_widget(advice_screen)

                # Подключиться к базе данных SQLite (будет создана, если еще не существует)
        conn = sqlite3.connect('session.db')
        c = conn.cursor()

        # Создать таблицу для хранения информации о сессии, если она еще не существует
        c.execute('''
            CREATE TABLE IF NOT EXISTS sessioninfo (
                id INTEGER PRIMARY KEY,
                user_email TEXT
            )
        ''')

        # Получить email пользователя из базы данных
        c.execute('SELECT user_email FROM sessioninfo WHERE id = 1')
        result = c.fetchone()
        self.user_email = result[0] if result else None

        # Если пользователь уже вошел в систему, перейти на экран профиля питомца
        if self.user_email is not None:
            pet_profile_screen = sm.get_screen('pet_profile')
            pet_profile_screen.user_email = self.user_email
            sm.current = 'pet_profile'
        else:
            sm.current = 'login'

        # Закрыть соединение с базой данных
        conn.close()

######окна советов
        birth_screen_cat = BirthScreen(name='birth_screen_cat')
        sm.add_widget(birth_screen_cat)

        teeth = Teeth(name='teeth')
        sm.add_widget(teeth)

        tick_bite = Tick_bite(name='tick_bite')
        sm.add_widget(tick_bite)
######окна советов

        # Создаем MDNavigationLayout и добавляем в него ScreenManager и NavigationDrawer
        nav_layout = MDNavigationLayout()
        nav_layout.add_widget(sm)
        nav_layout.add_widget(self.nav_drawer)
        
        return nav_layout

    def switch_screen(self, screen_name):
        self.root.ids.sm.current = screen_name

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

        # Подключиться к базе данных SQLite
        conn = sqlite3.connect('session.db')
        c = conn.cursor()

        # Удалить информацию о сессии из базы данных
        c.execute('DELETE FROM sessioninfo WHERE id = 1')

        # Закрыть соединение с базой данных
        conn.commit()
        conn.close()

    def close_dialog(self, instance):
        self.dialog.dismiss()

MainApp().run()
