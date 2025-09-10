from flet import app, Page

def main(page: Page):
    page.title = "My Flet App"
    page.vertical_alignment = "center"
    page.add("Welcome to My Flet App!")

if __name__ == "__main__":
    app(target=main)