import flet as ft

def main(page: ft.Page):
    page.title = "Chad Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    
    page.padding = ft.Padding.only(top=40, left=10, right=10, bottom=0)
    page.bgcolor = "#0F0F0F"
    
    BLUE = ft.Colors.BLUE_500
    CARD_COLOR = "#1C1C1E"
    TEXT_COLOR = "#E0E0E0"

    alarms = []
    current_day = "Пн"

    def get_schedule_text(day):
        morning = (
            "07:00 - Подъем. Стакан воды.\n"
            "07:05 - Умывание (Пропеллер). Тоник.\n"
            "07:10 - Зубы (2 мин) + нить.\n"
            "07:15 - ОСАНКА: Встань к стене. Сведи лопатки 15 раз.\n"
            "07:20 - МЬЮИНГ: Язык на небо, дыши носом.\n"
            "07:30 - Завтрак (Овсянка + яйца)."
        )
        evening = (
            "18:00 - Душ. Мой тело и спину.\n"
            "18:15 - ОСАНКА: 'Лодочка' (3х10). Растяжка груди в дверях.\n"
            "18:25 - Липобейз на тело.\n"
            "18:30 - Ужин (Курица + овощи).\n"
            "19:00 - Умывание. Тоник."
        )
        night = (
            "21:30 - Зубы + нить.\n"
            "21:40 - Мьюинг. Ляг на спину.\n"
            "22:00 - Отбой. Спи 9 часов."
        )

        if day in ["Пн", "Ср", "Пт"]:
            evening = "🔥 МЫТЬЕ ВОЛОС!\n" + evening + "\n19:30 - Шампунь (корни). Сушка вниз головой."
        elif day in ["Вт", "Чт"]:
            evening = "💪 ДЕНЬ СИЛЫ\n" + evening + "\n19:30 - Скраб для спины. Отжимания + Планка."
        else:
            morning = "🌅 ВЫХОДНОЙ\n" + morning
            evening = "🚶‍♂️ ПРОГУЛКА\n" + evening + "\n19:30 - Гуляй 2 часа."

        return morning, evening, night

    def create_card(title, text):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=BLUE),
                ft.Text(text, size=13, color=TEXT_COLOR),
            ], spacing=4),
            bgcolor=CARD_COLOR,
            padding=12,
            border_radius=12,
        )

    schedule_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE, expand=True)

    def update_schedule(e=None):
        schedule_list.controls.clear()
        morning, evening, night = get_schedule_text(current_day)
        schedule_list.controls.append(create_card("☀️ УТРО", morning))
        schedule_list.controls.append(create_card("🚿 ВЕЧЕР", evening))
        schedule_list.controls.append(create_card("🌙 НОЧЬ", night))
        page.update()

    days_row = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=5)
    day_buttons = {}

    def select_day(e):
        nonlocal current_day
        current_day = e.control.data
        for d, btn in day_buttons.items():
            btn.bgcolor = BLUE if d == current_day else CARD_COLOR
            btn.color = "white" if d == current_day else TEXT_COLOR
        update_schedule()

    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        btn = ft.Button(
            day, 
            data=day, 
            on_click=select_day,
            bgcolor=BLUE if day == "Пн" else CARD_COLOR,
            color="white" if day == "Пн" else TEXT_COLOR,
            height=35,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding.symmetric(horizontal=10, vertical=0), 
                text_style=ft.TextStyle(size=13)
            )
        )
        day_buttons[day] = btn
        days_row.controls.append(btn)

    alarm_list = ft.Column(spacing=8)

    def add_alarm(e):
        if time_input.value and msg_input.value:
            alarms.append(f"⏰ {time_input.value} — {msg_input.value}")
            alarm_list.controls.append(ft.Text(alarms[-1], color="white", size=14))
            time_input.value = ""
            msg_input.value = ""
            page.update()

    def auto_set(e):
        default_alarms = [
            "⏰ 07:00 — Подъем, умывание, осанка",
            "⏰ 18:00 — Душ, Лодочка, растяжка",
            "⏰ 21:30 — Зубы, нить, мьюинг, сон"
        ]
        for a in default_alarms:
            if a not in alarms:
                alarms.append(a)
                alarm_list.controls.append(ft.Text(a, color="white", size=14))
        page.update()

    time_input = ft.TextField(hint_text="07:00", width=90, border_radius=8, bgcolor=CARD_COLOR, text_size=13, height=40)
    msg_input = ft.TextField(hint_text="Напоминание", expand=True, border_radius=8, bgcolor=CARD_COLOR, text_size=13, height=40)

    alarms_view = ft.Container(
        content=ft.Column([
            ft.Button("⚡ Автонастройка", on_click=auto_set, bgcolor=BLUE, color="white", height=40, style=ft.ButtonStyle(text_style=ft.TextStyle(size=14))),
            ft.Row([time_input, msg_input, ft.IconButton(icon=ft.Icons.ADD, on_click=add_alarm, icon_color=BLUE)]),
            alarm_list
        ], scroll=ft.ScrollMode.ADAPTIVE, expand=True),
        padding=10,
        expand=True
    )

    music_view = ft.Container(
        content=ft.Column([
            ft.Text("Твой саундтрек", size=20, weight=ft.FontWeight.BOLD),
            ft.Button(
                "🎵 Открыть Яндекс Музыку", 
                url="https://music.yandex.ru",
                bgcolor=BLUE, 
                color="white", 
                height=45, 
                width=220, 
                style=ft.ButtonStyle(text_style=ft.TextStyle(size=14))
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
        padding=10,
        expand=True
    )

    content_area = ft.Container(expand=True)

    def change_tab(e):
        index = e.control.selected_index
        content_area.content = None
        if index == 0:
            content_area.content = ft.Container(
                content=ft.Column([days_row, schedule_list], expand=True),
                padding=ft.Padding.only(top=5) 
            )
            update_schedule()
        elif index == 1:
            content_area.content = alarms_view
        elif index == 2:
            content_area.content = music_view
        page.update()

    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_TODAY, label="План"),
            ft.NavigationBarDestination(icon=ft.Icons.ALARM, label="Будильники"),
            ft.NavigationBarDestination(icon=ft.Icons.MUSIC_NOTE, label="Музыка"),
        ],
        on_change=change_tab,
        bgcolor=CARD_COLOR,
        indicator_color=BLUE,
    )

    page.add(content_area, nav_bar)
    
    content_area.content = ft.Container(
        content=ft.Column([days_row, schedule_list], expand=True),
        padding=ft.Padding.only(top=5)
    )
    update_schedule()

if __name__ == "__main__":
    ft.run(main)
