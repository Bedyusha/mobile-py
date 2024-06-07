# birth_screen_сat.py
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.widget import Widget

class BirthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'birth_screen_cat'
        self.layout = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10])
        self.add_widget(self.layout)

        self.label = MDLabel(
            halign="center",
            theme_text_color="Secondary",
            font_style="H5",
            size_hint=(1, None),
            height="24dp"
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
            disabled=True,  # Кнопка "Назад" отключена на первом шаге
            
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
            1: {"image": 'img\\birth_screen_cat\\шаг1.jpg', "text": "Шаг 1: Определение начала родовой деятельности. За день до родов питомец может стать агрессивным и раздражительным или, наоборот, нетипично общительным и привязчивым, может привлекать хозяина голосом. За 4-6 часов наблюдаются активные шевеления живота. Кошка постоянно вылизывает наружные половые органы и ходит в туалет, в это время не спускайте с питомца глаз.", "title": "Роды питомца", "button": "Далее"},
            2: {"image": 'img\\birth_screen_cat\\шаг2.jpg', "text": "Шаг 2: Создайте для кошки тихое, теплое место без сквозняков и прямого солнечного света. Место должно быть изолированным от других животных и маленьких детей. Хорошо подойтет картонная коробка застланная пеленками. Не застилайте гнездо газетами, махровыми полотенцами, марлей или ватой. Не лишним будет узнать номер ближайшей ветклиники и график ее работы.", "title": "Роды питомца", "button": "Далее"},
            3: {"image": 'img\\birth_screen_cat\\шаг3-4.jpg', "text": "Шаг 3: Схватки. Кошка начнет дышать чаще, а живот станет напряженным. В норме необильные кровяные выделения из родовых путей, частая вокализация и беспокойное поведение. Например, кошка может рыть настил в гнезде или всюду следовать за хозяином. В этот момент питомца нужно поместить в ранее подготовленое место.", "title": "Роды питомца", "button": "Далее"},
            4: {"image": 'img\\birth_screen_cat\\шаг3-4.jpg', "text": "Шаг 4: Потуги. Этот период характерен интенсивным сокращением мышц живота, громким мурлыканьем и появлением из промежности плодного пузыря – шарика, наполненного темной жидкостью. В нем можно разглядеть мордочку, лапку или хвостик.В норме рождение котенка за 3-4 потуги. После чего кошка может перегрызть пуповину и облизать котенка самостоятельно.", "title": "Роды питомца", "button": "Далее"},
            5: {"image": 'img\\birth_screen_cat\\шаг5-6.jpg', "text": "Шаг 5: Возможные проблемы во время потугов. При прохождении по родовым путям или на выходе из петли пузырь может разорваться. Тогда околоплодная жидкость выльется наружу, и котенок начнет задыхаться. Если кошка попытается вылизать промежность и разорвать пузырь зубами, не дожидаясь рождения тельца, ее нужно остановить, мягко удерживая в положении на боку руками.", "title": "Роды питомца", "button": "Далее"},
            6: {"image": 'img\\birth_screen_cat\\шаг5-6.jpg', "text": "Шаг 6: Возможные проблемы во время потугов. Если плодный пузырь остался торчать, а родовая деятельность внезапно прекратилась, животному потребуется срочная помощь, обратитесь в ближайщую ветеринарную клинику.", "title": "Роды питомца", "button": "Далее"},
            7: {"image": 'img\\birth_screen_cat\\шаг7-8.jpg', "text": "Шаг 7: Другие проблемы при которых стоит сразу обратится в ветклинику: 1)Если кошка рожает более 12 часов. 2)Если воды отошли более 30 минут назад, но 1 котен так и не появился. 3) Слабая родовая деятельность, если кошка перестает тужится. 4)Если беременность длится более 70-72 дней, а предвестники родов так и не появились. 5)Большой интервал между рождением котят. 6) Обильные выделения из родовых путей и повышение температуры.", "title": "Роды питомца", "button": "Далее"},
            8: {"image": 'img\\birth_screen_cat\\шаг7-8.jpg', "text": "Шаг 8: Рождение плаценты. Плацента рождается сразу за котятами или спустя какое-то время. Главное, не допускать, чтобы хотя бы один из них остался в полости матки. Иначе это спровоцирует внутреннее воспаление, и нужно срочно обратится в ветклинику. Внимательно пересчитайте плаценты, когда роды завершатся. Их количество должно совпадать с количеством рожденных котят.", "title": "Роды питомца", "button": "Далее"},
            9: {"image": 'img\\birth_screen_cat\\шаг9-10.jpg', "text": "Шаг 9: В период между рождением котят животное должно успокаивается и дышать ровно. Котят можно приложить к наиболее молочным соскам. В норме, кошка может съесть 1 плаценту. Поедание плаценты за каждым котенком влечет несварение, рвоту и расстройство стула. Отказ от поедания вовсе является вариантом нормы.", "title": "Роды питомца", "button": "Далее"},
            10: {"image": 'img\\birth_screen_cat\\шаг9-10.jpg', "text": "Шаг 10: После родовой период. Если роды завершились без осложнений, кошка проявляет интерес к детенышам, а ее живот стал мягким, предложите ей воды и перестелите гнездо, чтобы пеленка была сухой и чистой. Первые 2-3 дня после родов кормите молодую маму жидким или влажным кормом, увеличив энергетическую ценность суточной нормы на 30%.", "title": "Роды питомца", "button": "Далее"},
            11: {"image": 'img\\birth_screen_cat\\шаг11.jpg', "text": "Шаг 11: После родовой период. Стремительное снижением уровня кальция из-за прилива молока, может вызвать послеродовую эклапсию (молочную лихорадку). Симптомы: повышенное слюноотделение, нарушение координации движений, судороги. При возникновении таких симптомов срочно обратитесь в ближайшую ветеринарную клинику.", "title": "Роды питомца", "button": "Выход"},
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
            # self.text.height = self.text.texture_size[1]  # Измените эту строку
            self.label.text = step_info["title"]
            self.next_button.text = step_info["button"]
            
            # anim = Animation(height=300) + Animation(height=250)
            # anim.start(self.image)
