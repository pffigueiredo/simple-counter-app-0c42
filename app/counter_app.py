from nicegui import ui
from app.counter_service import get_counter, increment_counter, reset_counter


def create():
    @ui.page("/counter")
    def counter_page():
        # Modern styling with cards and proper spacing
        with ui.column().classes("max-w-md mx-auto mt-8 p-6"):
            # Main counter card
            with ui.card().classes("p-8 text-center shadow-lg rounded-xl"):
                ui.label("Counter App").classes("text-3xl font-bold text-gray-800 mb-6")

                # Get initial counter value
                counter = get_counter()

                # Counter display
                counter_label = ui.label(str(counter.value)).classes("text-6xl font-bold text-primary mb-8")

                # Action buttons
                with ui.row().classes("gap-4 justify-center"):
                    ui.button("Increment", on_click=lambda: update_counter_display(counter_label), icon="add").classes(
                        "bg-primary text-white px-6 py-3 rounded-lg shadow-md hover:shadow-lg transition-shadow"
                    )

                    ui.button("Reset", on_click=lambda: reset_counter_display(counter_label), icon="refresh").classes(
                        "bg-gray-500 text-white px-6 py-3 rounded-lg shadow-md hover:shadow-lg transition-shadow"
                    )

            # Info card
            with ui.card().classes("p-4 mt-4 bg-blue-50 border-l-4 border-blue-500"):
                ui.label("💡 The counter value is automatically saved to the database").classes("text-sm text-blue-800")


def update_counter_display(label: ui.label):
    """Increment counter and update display"""
    counter = increment_counter()
    label.set_text(str(counter.value))
    ui.notify(f"Counter incremented to {counter.value}", type="positive")


def reset_counter_display(label: ui.label):
    """Reset counter and update display"""
    counter = reset_counter()
    label.set_text(str(counter.value))
    ui.notify("Counter reset to 0", type="info")
