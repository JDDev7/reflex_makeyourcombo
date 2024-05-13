from makeyourcombo import styles
from makeyourcombo.components.game_link_button import game_link_button
from makeyourcombo.components.footer import footer
from makeyourcombo.styles import *
import reflex as rx


@rx.page(route="/en", title="Home", image="/github.svg")
def index_en() -> rx.Component:
    return rx.center(rx.vstack(
        rx.chakra.heading(
            "Welcome to Make Your Combo!", size=["2xl","lg","md","sm"]
        ),
        rx.chakra.text(
            "Pick your game clicking on an image below!"
        ),
        rx.spacer(),
        rx.tablet_and_desktop(
        rx.hstack(
            game_link_button(image="/tk8_image_link.webp", url="/", alt="Tekken 8 image"),
            game_link_button(image="/sf6_image_link.webp", url="/", alt="Street Fighter 6 image")
        ),),
        rx.mobile_only(
            rx.vstack(
            game_link_button(image="/tk8_image_link_phone.webp", url="/", alt="Tekken 8 image"),
            rx.spacer(spacing="4"),
            game_link_button(image="/sf6_image_link_phone.webp", url="/", alt="Street Fighter 6 image")
            )
        ),
        footer()
    )
)