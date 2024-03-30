import reflex as rx

from .components import custom_input, todo


class State(rx.State):
    current_todo: dict = {"title": "", "description": "", "status": "todo"}
    todos: list[dict] = []
    can_submit: bool = False
    current_tab: str = "todo"

    def current_items(self):
        return [t for t in self.todos if t["status"] == self.current_tab]

    def edit_title(self, title: str):
        self.current_todo = {
            **self.current_todo,
            "title": title,
        }
        self.can_submit = bool(title) and bool(self.current_todo["description"])

    def edit_description(self, description: str):
        self.current_todo = {
            **self.current_todo,
            "description": description,
        }
        self.can_submit = bool(description) and bool(self.current_todo["title"])

    def submit(self, _: any) -> None:
        self.todos.append(self.current_todo)
        self.can_submit = False

    def change_tab(self, tab: str):
        self.current_tab = tab

    def complete_todo(self, t: dict):
        self.todos.remove(t)

        new_todo = {
            **t,
            "status": "completed"
        }

        self.todos.append(new_todo)

    def remove_todo(self, t: dict):
        self.todos.remove(t)


def index():
    def render_todo(t: dict):
        return rx.cond(t["status"] == State.current_tab, todo(t, State.complete_todo, State.remove_todo))

    return rx.vstack(
        rx.script(
            src="https://www.googletagmanager.com/gtag/js?id=G-R32T2965HZ",
            custom_attrs={"async": True}
        ),
        rx.script(
            """
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
            
              gtag('config', 'G-R32T2965HZ');
            """
        ),
        rx.heading("My Todos", font_size="2em"),
        rx.hstack(
            rx.form(
                custom_input("Title:", on_change=State.edit_title),
                custom_input("Description:", on_change=State.edit_description),
                rx.button(
                    "Submit",
                    type="submit",
                    disabled=~State.can_submit,
                    style={"height": "auto"}
                ),
                style={
                    "backgroundColor": "var(--gray-a10)",
                    "borderRadius": "8px",
                    "display": "flex",
                    "justifyContent": "space-between",
                    "padding": "24px",
                    "width": "100%"
                },
                on_submit=State.submit,
                reset_on_submit=True
            ),
            style={
                "width": "100%"
            },
            align="center",
            spacing="8"
        ),
        rx.section(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("To Do", value="todo"),
                    rx.tabs.trigger("Completed", value="completed"),
                    size="2",
                    style={"marginBottom": "24px"}
                ),
                rx.grid(
                    rx.foreach(
                        State.todos,
                        render_todo
                    ),
                    columns="3",
                    spacing="4"
                ),
                default_value="todo",
                orientation="vertical",
                on_change=State.change_tab
            ),
            style={
                "padding": "0",
                "width": "100%"
            }
        ),
        style={
            "margin": "40px auto 0 auto",
            "width": "768px"
        },
        align="center",
        spacing="8",
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
        accent_color="crimson",
    ),
    stylesheets=["styles.css"]
)
app.add_page(index)
