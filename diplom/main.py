from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        # Создаем список для Navigation Drawer
        self.nav_drawer = MDNavigationDrawer()
        # self.nav_drawer.md_bg_color = get_color_from_hex("#424242")  # Устанавливаем цвет фона
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

        sm.add_widget(screen)

        return sm

    def switch_theme(self, *args):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        self.nav_drawer.md_bg_color = get_color_from_hex("#2C2C2C") if self.theme_cls.theme_style == "Dark" else get_color_from_hex("#c3c3c3")

MainApp().run()
