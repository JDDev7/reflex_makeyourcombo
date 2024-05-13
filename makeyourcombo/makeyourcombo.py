"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from makeyourcombo.components.navbar import index_navbar
from rxconfig import config
from makeyourcombo.components.game_link_button import game_link_button
from makeyourcombo.components.footer import footer
from makeyourcombo.pages.tekken_8_cm import tk8_page
from makeyourcombo.pages.sf6_cm import sf6_page
from makeyourcombo.pages.xko_cm import xko_page
from makeyourcombo.styles import *
import reflex as rx


@rx.page(route="/", title="Home | Make your Combo!", image="/github.svg")
def index_es() -> rx.Component:
    return rx.center(rx.vstack(
        index_navbar(),
        rx.heading(
            "Welcome to Make Your Combo!",
        ),
        rx.text(
            "Pick your game clicking on an image below! More to come soon!"
        ),
        rx.spacer(),
        rx.tablet_and_desktop(
        rx.hstack(
            game_link_button(image="/tk8_image_link.webp", url="/tk8", alt="Tekken 8 image"),
            game_link_button(image="/sf6_image_link.webp", url="/sf6", alt="Street Fighter 6 image"),
            game_link_button(image="/2xko_image_link.webp", url="/2xko", alt="2XKO image")
        ),),
        rx.mobile_only(
            rx.vstack(
            game_link_button(image="/tk8_image_link_phone.webp", url="/tk8", alt="Tekken 8 image"),
            game_link_button(image="/sf6_image_link_phone.webp", url="/sf6", alt="Street Fighter 6 image"),
            game_link_button(image="/2xko_image_link_phone.webp", url="/2xko", alt="2XKO image"),
            ),
        ),
    footer(),
    align="center",
    ),
)

app = rx.App(style=base_style)
app.add_page(index_es, route="/")
app.add_page(tk8_page, route="/tk8")
app.add_page(sf6_page, route="/sf6")
app.add_page(xko_page, route="/2xko")
