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
#Импорты основных окон
from advice_screen import AdviceScreen
from PetProfileScreen import PetProfileScreen
from feeding_screen import FeedingScreen
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

        list_drawer = MDList()
        button_names = ['Профиль питомца', 'Button 2', 'График питания', 'Дресировка', 'Советы на особый случай', 'На главную страницу']
        buttons = [OneLineListItem(text=name) for name in button_names]
        for button in buttons:
            list_drawer.add_widget(button)

################################################кнопка переключения темы широковата##################################################
        # Создаем список для Navigation Drawer
        self.nav_drawer = MDNavigationDrawer()

        # Добавляем кнопку для переключения темы
        theme_button = MDIconButton(icon="lightbulb-on-outline", pos_hint={"right": 1, "top": 1}, on_release=self.switch_theme)
        self.nav_drawer.add_widget(list_drawer)
        self.nav_drawer.add_widget(theme_button)
#####################################################################################################################################

        # Создаем ScreenManager и добавляем в него экран
        sm = ScreenManager()
        screen = Screen(name='screen')
        screen.add_widget(MDRaisedButton(
            text="Hello, World",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        ))

        # Привязываем первую кнопку в списке к переключению на экран профиля питомца
        def switch_to_pet_profile(*args):
            sm.current = 'pet_profile'
        
        buttons[0].bind(on_release=switch_to_pet_profile)
        
##########################################################################################################
        # Привязываем кнопку "Советы на особый случай" к переключению на экран советов
        def switch_to_advice_screen(*args):
            sm.current = 'advice'
        buttons[4].bind(on_release=switch_to_advice_screen)
##########################################################################################################
        # Привязываем кнопку "Вернуться на главную страницу" к переключению на главный экран
        def switch_to_main_screen(*args):
            sm.current = 'screen' 
        buttons[-1].bind(on_release=switch_to_main_screen)

        def switch_to_feeding_screen(*args):
            sm.current = 'feeding_screen'
        buttons[2].bind(on_release=switch_to_feeding_screen)

        sm.add_widget(screen)

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
        #sm.current = 'screen'
        return nav_layout

    def switch_theme(self, *args):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        self.nav_drawer.md_bg_color = get_color_from_hex("#2C2C2C") if self.theme_cls.theme_style == "Dark" else get_color_from_hex("#c3c3c3")

MainApp().run()