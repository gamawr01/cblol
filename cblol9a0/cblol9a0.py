import reflex as rx
from .ui import index
from .state import GameState

app = rx.App(
    stylesheets=["https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800;900&display=swap"],
)
app.add_page(index, route="/", title="CBLOL 9A0", on_load=GameState.on_load)
