from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"  # Основной цвет - оранжевый
        self.theme_cls.theme_style = "Dark"  # Темная тема

        bn = MDBottomNavigation()

        items = [
            {"name": "Профиль\nпитомца", "icon": "cat"},
            {"name": "График\nпитания", "icon": "bowl"},
            {"name": "Дресировка", "icon": "dog-side"},
            {"name": "Советы", "icon": "help-circle"},
            {"name": "Выйти", "icon": "menu"}, 
        ]

        for i, item in enumerate(items):
            bn_item = MDBottomNavigationItem(
                name=f"screen{i+1}",
                text=item["name"],
                icon=item["icon"],
            )
            bn.add_widget(bn_item)

        return bn

if __name__ == "__main__":
    MainApp().run()
