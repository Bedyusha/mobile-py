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
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

from advice_screen import AdviceScreen
from PetProfileScreen import PetProfileScreen
from feeding_screen import FeedingScreen
from training_screen import TrainingScreen
from login_screen import LoginScreen

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"  # Основной цвет - оранжевый
        self.theme_cls.theme_style = "Dark"  # Темная тема

        sm = ScreenManager()
        #self.manager.current= 'main' # Создаем главный ScreenManager

        # Создаем экраны, которые будут доступны через нижнюю панель навигации
        bn = MDBottomNavigation()
        items = [
            {"name": "Профиль\nпитомца", "icon": "cat","screen": PetProfileScreen(name='pet_profile')},
            {"name": "График\nпитания", "icon": "bowl","screen": FeedingScreen(name='feeding_screen')},
            {"name": "Дресировка", "icon": "dog-side", "screen": TrainingScreen(name='training_screen')},
            {"name": "Советы", "icon": "help-circle", "screen": AdviceScreen(name='advice') },
            {"name": "Выйти", "icon": "menu", "screen": LoginScreen(name='login')}, 
        ]
        for i, item in enumerate(items):
            bn_item = MDBottomNavigationItem(
                name=f"screen{i+1}",
                text=item["name"],
                icon=item["icon"],
            )
            bn_item.add_widget(item["screen"])
            bn.add_widget(bn_item)
        
        # Создаем экран, который будет содержать MDBottomNavigation
        main_screen = Screen(name='main')
        main_screen.add_widget(bn)
        sm.add_widget(main_screen)  # Добавляем этот экран в главный ScreenManager

        # # Создаем экраны, которые будут доступны через кнопки на экране AdviceScreen
        # sm.add_widget(BirthScreen(name='birth_screen_cat'))
        # sm.add_widget(Teeth(name='teeth'))
        # sm.add_widget(Tick_bite(name='tick_bite'))

        return sm  # Возвращаем главный ScreenManager как корневой виджет приложения

MainApp().run()


#         self.sm = ScreenManager()
#         self.sm.add_widget(PetProfileScreen(name='pet_profile'))
#         self.sm.add_widget(AdviceScreen(name='advice'))
#         self.sm.add_widget(TrainingScreen(name='training_screen'))

#         self.nav_drawer = MDNavigationDrawer()

#         items = [
#             {"name": "Профиль питомца", "screen": "pet_profile"},
#             {"name": "График питания", "screen": "advice"},
#             {"name": "Дресировка", "screen": "training_screen"},
#         ]

#         self.list = MDList()
#         for item in items:
#             list_item = OneLineListItem(text=item["name"], on_release=lambda x, screen=item["screen"]: self.switch_screen(screen))
#             self.list.add_widget(list_item)

#         self.nav_drawer.add_widget(self.list)

#         self.nav_layout = MDNavigationLayout()
#         self.nav_layout.add_widget(self.sm)
#         self.nav_layout.add_widget(self.nav_drawer)

#         # Создаем кнопку для открытия и закрытия боковой панели навигации
#         self.nav_button = MDIconButton(icon="menu", on_release=lambda x: self.nav_drawer.set_state("toggle"))
#         self.nav_button.pos_hint = {"x": 0, "top": 1}  # Размещаем кнопку в верхнем левом углу

#         # Добавляем кнопку на каждый экран
#         for screen in self.sm.screens:
#             screen.add_widget(self.nav_button)

#         return self.nav_layout

#     def switch_screen(self, screen_name):
#         self.sm.current = screen_name
#         self.nav_drawer.set_state("close")

# MainApp().run()
