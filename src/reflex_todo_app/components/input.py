import reflex as rx


def custom_input(title: str, on_change: any):
    return rx.vstack(
        rx.text(title),
        rx.input(on_change=on_change)
    )
