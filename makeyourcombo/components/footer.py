import reflex as rx
import datetime

def footer() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.center(
                rx.text(f"© Make Your Combo by JDDev. All game images are owned by their respective companies. {datetime.date.today().year}", align="center", padding_x="1rem", padding_y="1rem",color="white"),
                
            ),align="center"
        ),
        align="center"
    )