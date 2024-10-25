from nicegui import ui

ui.image("./static/logo-1080px.png").classes('w-60')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(native=True)
