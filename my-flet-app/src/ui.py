from flet import Page, Text, ElevatedButton, Column

def create_ui(page: Page):
    page.title = "My Flet App"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    greeting = Text("Welcome to My Flet App!", size=24)
    button = ElevatedButton("Click Me", on_click=lambda e: page.add(Text("Button Clicked!")))

    page.add(Column([greeting, button]))