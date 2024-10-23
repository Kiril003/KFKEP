import flet as ft
import asyncio
from database import create_table, get_student_by_full_name
from main_page import main_page

create_table()

COLORS = {
    "primary": "#7C3AED",
    "primary_light": "#8B5CF6",
    "primary_dark": "#6D28D9",
    "secondary": "#EC4899",
    "secondary_light": "#F472B6",
    "accent": "#3B82F6",
    "accent_light": "#60A5FA",
    "background": "#F9FAFB",
    "surface": "#FFFFFF",
    "error": "#EF4444",
    "error_light": "#FEE2E2",
    "success": "#10B981",
    "success_light": "#D1FAE5",
    "warning": "#F59E0B",
    "warning_light": "#FEF3C7",
    "text": "#1E293B",
    "text_secondary": "#64748B",
    "border": "#E2E8F0",
    "input_bg": "#F8FAFC",
    "gradient_1": "#4F46E5",
    "gradient_2": "#7C3AED",
    "gradient_3": "#EC4899"
}

class LoadingOverlay:
    def __init__(self, page: ft.Page):
        self.page = page
        self.overlay = ft.Container(
            content=ft.ProgressBar(
                color=COLORS["primary"],
                bgcolor=ft.colors.with_opacity(0.1, COLORS["primary"]),
                height=4,
            ),
            alignment=ft.alignment.top_center,
            animate=ft.animation.Animation(300, "decelerate"),
        )
        self.visible = False

    def show(self):
        if not self.visible:
            self.page.overlay.append(self.overlay)
            self.visible = True
            self.page.update()

    def hide(self):
        if self.visible:
            self.page.overlay.remove(self.overlay)
            self.visible = False
            self.page.update()

class Message:
    def __init__(self, page: ft.Page):
        self.page = page
        self.message_container = None

    async def show(self, text: str, color: str = "error"):
        colors = {
            "error": (COLORS["error"], COLORS["error_light"]),
            "warning": (COLORS["warning"], COLORS["warning_light"]),
            "success": (COLORS["success"], COLORS["success_light"])
        }
        main_color, bg_color = colors.get(color, colors["error"])

        if self.message_container:
            self.message_container.opacity = 0
            self.message_container.update()
            await asyncio.sleep(0.2)
            self.page.controls.remove(self.message_container)

        self.message_container = ft.Container(
            content=ft.Row([
                ft.Icon(name=ft.icons.INFO_ROUNDED, color=main_color, size=20),
                ft.Text(value=text, color=main_color, size=14, weight="w500")
            ], spacing=10, alignment=ft.MainAxisAlignment.START),
            bgcolor=bg_color,
            padding=15,
            border_radius=12,
            opacity=0,
            animate=ft.animation.Animation(300, "decelerate"),
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=ft.colors.with_opacity(0.1, "black"),
                offset=ft.Offset(0, 4),
            ),
        )

        self.page.add(self.message_container)
        self.message_container.opacity = 1
        self.page.update()

def create_input_field(label: str, icon: str, password: bool = False) -> ft.Container:
    field = ft.Container(
        content=ft.TextField(
            label=label,
            border=ft.InputBorder.NONE,
            prefix_icon=icon,
            password=password,
            can_reveal_password=password,
            text_size=14,
            hint_text=f"Введіть {label.lower()}",
            cursor_color=COLORS["primary"],
            cursor_width=2,
            color=COLORS["text"],
            bgcolor=COLORS["input_bg"],
            content_padding=ft.padding.only(left=20, right=20, top=18, bottom=18),
            focused_bgcolor=ft.colors.with_opacity(0.05, COLORS["primary"]),
        ),
        border=ft.border.all(1, COLORS["border"]),
        border_radius=12,
        shadow=ft.BoxShadow(
            blur_radius=4,
            color=ft.colors.with_opacity(0.05, "black"),
            offset=ft.Offset(0, 2),
        ),
        animate=ft.animation.Animation(150, "decelerate"),
    )

    def on_focus(e):
        field.border = ft.border.all(2 if e.data == "true" else 1, 
                                   COLORS["primary"] if e.data == "true" else COLORS["border"])
        field.shadow = ft.BoxShadow(
            blur_radius=8 if e.data == "true" else 4,
            color=ft.colors.with_opacity(0.1 if e.data == "true" else 0.05, 
                                       COLORS["primary"] if e.data == "true" else "black"),
            offset=ft.Offset(0, 4 if e.data == "true" else 2),
        )
        field.update()

    field.content.on_focus = on_focus
    return field

def create_button(text: str, icon: str, on_click) -> ft.Container:
    return ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row(
                [ft.Text(text, size=15, weight="w600"), ft.Icon(icon, size=18)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            style=ft.ButtonStyle(
                color="white",
                padding=ft.padding.only(top=22, bottom=22, left=30, right=30),
                animation_duration=300,
                elevation=0,
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            on_click=on_click,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[COLORS["gradient_1"], COLORS["gradient_2"], COLORS["gradient_3"]],
        ),
        border_radius=12,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.colors.with_opacity(0.3, COLORS["primary"]),
            offset=ft.Offset(0, 6),
        ),
        animate=ft.animation.Animation(300, "decelerate"),
    )

def login_page(page: ft.Page):
    message = Message(page)
    loading = LoadingOverlay(page)
    
    container = ft.Container(
        width=350,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[COLORS["surface"], COLORS["background"]],
        ),
        border_radius=24,
        padding=30,
        animate=ft.animation.Animation(500, "decelerate"),
        shadow=ft.BoxShadow(
            blur_radius=30,
            color=ft.colors.with_opacity(0.08, "black"),
            offset=ft.Offset(0, 15),
        ),
    )

    icon_container = ft.Container(
        content=ft.Stack([
            ft.Container(
                width=80,
                height=80,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[COLORS["gradient_1"], COLORS["gradient_3"]],
                ),
                border_radius=40,
                animate=ft.animation.Animation(1000, "bounceOut"),
                rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
            ),
            ft.Container(
                content=ft.Icon(name=ft.icons.SCHOOL_ROUNDED, size=40, color="white"),
                width=80,
                height=80,
                alignment=ft.alignment.center,
            ),
        ]),
        animate=ft.animation.Animation(1000, "decelerate"),
        shadow=ft.BoxShadow(
            blur_radius=25,
            color=ft.colors.with_opacity(0.2, COLORS["primary"]),
            offset=ft.Offset(0, 8),
        ),
    )

    full_name_input = create_input_field("ПІБ студента", ft.icons.PERSON_ROUNDED)
    password_input = create_input_field("Пароль", ft.icons.LOCK_ROUNDED, password=True)

    async def login(e):
        full_name = full_name_input.content.value.strip()
        password = password_input.content.value.strip()

        if not full_name or len(full_name.split()) < 3:
            await message.show("⚠️ Введіть повне ПІБ", "warning")
            return

        if not password or len(password) < 6:
            await message.show("⚠️ Пароль має містити мінімум 6 символів", "warning")
            return

        loading.show()
        await asyncio.sleep(0.5)

        student = get_student_by_full_name(full_name.title())
        
        if not student:
            loading.hide()
            await message.show("❌ Користувача не знайдено", "error")
            
            for i in range(3):
                container.offset = ft.transform.Offset(-0.02 if i % 2 == 0 else 0.02, 0)
                page.update()
                await asyncio.sleep(0.05)
            container.offset = ft.transform.Offset(0, 0)
            page.update()
            
        elif student[2] != password:
            loading.hide()
            await message.show("❌ Неправильний пароль", "error")
            password_input.content.value = ""
            page.update()
            
        else:
            await message.show("✅ Успішний вхід!", "success")
            container.scale = ft.transform.Scale(0.95)
            container.opacity = 0
            container.rotate = ft.transform.Rotate(0.05)
            page.update()
            await asyncio.sleep(0.5)
            
            loading.hide()
            page.clean()
            page.add(main_page(page))
            page.update()

    login_btn = create_button("Увійти", ft.icons.LOGIN_ROUNDED, login)

    content = ft.Column(
        controls=[
            icon_container,
            ft.Container(height=25),
            ft.Text("Вхід до порталу", size=24, color=COLORS["text"], 
                   weight="bold", text_align=ft.TextAlign.CENTER),
            ft.Container(height=8),
            ft.Text("Введіть дані для входу", size=14, 
                   color=COLORS["text_secondary"], text_align=ft.TextAlign.CENTER),
            ft.Container(height=30),
            full_name_input,
            ft.Container(height=15),
            password_input,
            ft.Container(height=30),
            login_btn,
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    container.content = content
    return container

def main(page: ft.Page):
    page.title = "Студентський портал"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 400
    page.window.height = 700
    page.window.min_width = 350
    page.window.min_height = 600
    page.window.resizable = True
    page.bgcolor = COLORS["background"]
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    login_container = login_page(page)
    login_container.opacity = 0
    login_container.scale = ft.transform.Scale(0.9)
    login_container.offset = ft.transform.Offset(0, 0.1)
    page.add(login_container)
    
    login_container.opacity = 1
    login_container.scale = ft.transform.Scale(1)
    login_container.offset = ft.transform.Offset(0, 0)
    page.update()

if __name__ == "__main__":
    ft.app(target=main, port=5000)