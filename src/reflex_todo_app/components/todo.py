import reflex as rx


def todo(t: dict, on_complete: any, on_delete: any):
    button_color_scheme = rx.match(
        t["status"],
        ("todo", "crimson"),
        ("completed", "green"),
        "crimson"
    )

    return rx.hstack(
        rx.vstack(
            rx.text(t["title"], style={
                "fontSize": "40px",
                "fontWeight": "bold",
            }),
            rx.text(t["description"])
        ),
        rx.vstack(
            rx.cond(
                t["status"] == "todo",
                rx.icon_button(
                    "check",
                    variant="ghost",
                    color_scheme=button_color_scheme,
                    high_contrast=True,
                    on_click=lambda: on_complete(t)
                )
            ),
            rx.icon_button(
                "x",
                variant="ghost",
                color_scheme=button_color_scheme,
                high_contrast=True,
                on_click=lambda: on_delete(t)
            ),
        ),
        background_color=rx.match(
            t["status"],
            ("todo", "crimson"),
            ("completed", "green"),
            "crimson"
        ),
        style={
            "borderRadius": "8px",
            "display": "flex",
            "justifyContent": "space-between",
            "padding": "16px",
        }
    )
