from app.database import create_tables
from nicegui import ui
import app.counter_app


def startup() -> None:
    # this function is called before the first request
    create_tables()
    app.counter_app.create()

    @ui.page("/")
    def index():
        with ui.column().classes("max-w-lg mx-auto mt-16 p-6 text-center"):
            ui.label("Welcome to Counter App").classes("text-4xl font-bold text-gray-800 mb-4")
            ui.label("A simple web application with a persistent counter").classes("text-lg text-gray-600 mb-8")

            with ui.card().classes("p-6 shadow-lg rounded-xl"):
                ui.label("Ready to start counting?").classes("text-xl font-semibold mb-4")
                ui.button("Open Counter", on_click=lambda: ui.navigate.to("/counter"), icon="play_arrow").classes(
                    "bg-primary text-white px-8 py-3 rounded-lg shadow-md hover:shadow-lg transition-shadow text-lg"
                )
