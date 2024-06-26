# teeth.py
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.widget import Widget

class Teeth(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10])
        self.add_widget(self.layout)

        self.label = MDLabel(
            halign="center",
            theme_text_color="Secondary",
            font_style="H5",
            size_hint=(1, None),
            height="44dp"
        )
        self.layout.add_widget(self.label)

        self.image = Image(size_hint=(1, None), height="250dp")
        self.layout.add_widget(self.image)

        self.text = MDLabel(
            halign="center",
            theme_text_color="Secondary",
            font_style="Body1",
            height="20dp"
            
        )
        self.layout.add_widget(self.text)

        button_layout = BoxLayout(size_hint=(1, None), height="48dp")
        self.layout.add_widget(button_layout)

        self.back_button = MDRaisedButton(
            text="Назад",
            pos_hint={"center_x": 0.5},
            size_hint=(0.5, 1),
            disabled=True  # Кнопка "Назад" отключена на первом шаге
        )
        self.back_button.bind(on_release=self.previous_step)
        button_layout.add_widget(self.back_button)

        button_layout.add_widget(Widget(size_hint_x=None, width=10))

        self.next_button = MDRaisedButton(
            pos_hint={"center_x": 0.5},
            size_hint=(0.5, 1)
        )
        self.next_button.bind(on_release=self.next_step)
        button_layout.add_widget(self.next_button)

        # Добавьте пустое пространство внизу
        self.layout.add_widget(Widget())

        self.step = 1

        # Определите информацию о шагах
        self.steps = {
            1: {"image": 'img\\teeth\\шаг1.png', "text": "Шаг 1: Определение причины. Если ваш питомец еще молод, то скорее всего, он просто меняет зубы. У щенков это происходит в возрасте от 4 до 6 месяцев, а у котят - от 3 до 7 месяцев. ", "title": "Выпадение зубов", "button": "Далее"},
            2: {"image": 'img\\teeth\\шаг2.png', "text": "Шаг 2: Поводы обратится в ветеринару. Если ваш питомец взрослый и у него выпадают зубы, это может быть признаком заболевания десен или других проблем со здоровьем, если у вашего питомца также наблюдаются симптомы, такие как слюнотечение, отказ от еды, кровотечение изо рта или наличие больших зубов, обратитесь к ветеринару. ", "title": "Выпадение зубов", "button": "Далее"},
            3: {"image": 'img\\teeth\\шаг3.png', "text": "Шаг 3: Рекомендации по уходу. Регулярно чистите зубы вашего питомца специальной зубной щеткой и зубной пастой для животных. Это поможет предотвратить заболевания десен и сохранит зубы вашего питомца здоровыми", "title": "Выпадение зубов", "button": "Выход"},
            # Добавьте больше шагов по мере необходимости
        }

        self.update_step()

    def on_enter(self, *args):
        self.step = 1
        self.update_step()
        self.back_button.disabled = True

    def previous_step(self, instance):
        self.step -= 1
        if self.step == 1:
            self.back_button.disabled = True  # Отключите кнопку "Назад" на первом шаге
        self.update_step()

    def next_step(self, instance):
        if self.step < len(self.steps):
            self.step += 1
            if self.step > 1:
                self.back_button.disabled = False  # Включите кнопку "Назад", если это не первый шаг
            self.update_step()
        else:
            self.manager.current = 'advice'  # Перейдите на экран советов, если это последний шаг

    def update_step(self):
        step_info = self.steps.get(self.step)
        if step_info:
            self.image.source = step_info["image"]
            self.text.text = step_info["text"]
            self.label.text = step_info["title"]
            self.next_button.text = step_info["button"]
            # anim = Animation(height=300) + Animation(height=250)
            # anim.start(self.image)
