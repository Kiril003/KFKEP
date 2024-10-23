import flet as ft

def main_page(page):
    def logout(e):
        page.clean()  # Очищаємо головну сторінку
        from main import login_page  # Імпортуємо функцію входу
        page.add(login_page(page))  # Додаємо форму для входу
        page.update()

    # Головна сторінка з елементами
    return ft.Column([
        ft.Text("Ласкаво просимо до особистого кабінету!", size=20, weight="bold"),
        ft.Divider(),
        ft.Text("1. Особистий кабінет"),
        ft.Text("2. Чат"),
        ft.Text("3. Форум"),
        ft.Text("4. Розклад занять"),
        ft.Divider(),
        ft.ElevatedButton("Вийти з профілю", on_click=logout)  # Кнопка виходу
    ])
