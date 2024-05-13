import reflex as rx

from makeyourcombo.components.navbar_buttons_with_links import navbar_button_with_link
from makeyourcombo.components.mobile_navbar_buttons import mobile_navbar_button
from makeyourcombo.constants import *


# def index_navbar() -> rx.Component:
#     return rx.hstack(
#         navbar_button_with_link(image="/github.svg", text="Project's Github", url="/"),
#         navbar_button_with_link(image="/x-twitter.svg", text="Follow me on X", url="/"),
#         margin_y=["1em", "1.5em"],
#     )
    
def index_navbar() -> rx.Component:
    return rx.chakra.flex(
        rx.chakra.button_group(
            navbar_button_with_link(image="/github.svg", text="Project's Github", url=GITHUB, external=True),
            navbar_button_with_link(image="/x-twitter.svg", text="Follow me on X", url=TWITTER, external=True),
            rx.color_mode.button(rx.color_mode.icon(), background="#62499e"),
            spacing=4,  # Adjust spacing between buttons as needed
        ),
        justify="center",
        align="center",
        width="100%",
        margin_y=["1em", "1.5em"],
    )
    
def game_navbar() -> rx.Component:
    return rx.tablet_and_desktop(rx.chakra.flex(
        rx.chakra.button_group(
            navbar_button_with_link(image="/logo_white_navbar.webp", text="Home", url="/", external=False),
            navbar_button_with_link(image="/github.svg", text="Project's Github", url=GITHUB, external=True),
            navbar_button_with_link(image="/x-twitter.svg", text="Follow me on X", url=TWITTER, external=True),
            navbar_button_with_link(image="/kofi.webp", text="Donate", url=KOFI, external=True),
            rx.color_mode.button(rx.color_mode.icon(), background="#62499e"),
            spacing=5,  # Adjust spacing between buttons as needed
        ),
        justify="center",
        align_items="center",
        margin_y=["1em", "1.5em"],
        width="100%",
        ),
        width="100%",
    )

# def game_navbar() -> rx.Component:
#     return rx.chakra.flex(
#             rx.chakra.button_group(
#                 navbar_button_with_link(image="/logo_white_navbar.webp", text="Home", url="/"),
#                 navbar_button_with_link(image="/github.svg", text="Project's Github", url="/"),
#                 navbar_button_with_link(image="/x-twitter.svg", text="Follow me on X", url="/"),
#                 navbar_button_with_link(image="/kofi.webp", text="Donate", url="https://ko-fi.com/jddev"),
#                 rx.color_mode.button(rx.color_mode.icon(), background="#62499e"),
#                 spacing=5,
#             ),
#             justify_content="center",
#             align_content="center",  # Allow wrapping to next line
#             width="100%",  # Take full width to center within
#             margin_y=["1em", "1.5em"],
#         ),
    

# Mobile navbar

def sf6_mobile_navbar() -> rx.Component:
    return rx.mobile_only(
        rx.drawer.root(
            rx.drawer.trigger(
                rx.button(rx.icon("menu"), margin_top="1em"), background="#62499e"
            ),
            rx.drawer.overlay(),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.vstack(
                        rx.drawer.close(
                            rx.button(rx.icon("menu"), background="#62499e")
                        ),
                        mobile_navbar_button("Home",image="/logo_white.webp", url="/"),
                        mobile_navbar_button("Project's Github",image="/github.svg", url=GITHUB),
                        mobile_navbar_button("Follow me on X!",image="/x-twitter.svg", url=TWITTER),
                        mobile_navbar_button("Donate",image="/kofi.webp", url=KOFI),
                        # Add more links here if needed
                        spacing="4",  # Adjust spacing between items as needed
                        width="100%",
                    ),
                    justify="center",
                    padding="2em",
                    background="linear-gradient(90deg, rgba(97,16,150,1) 0%, rgba(55,5,135,1) 50%, rgba(97,16,150,1) 100%)",
                ),
                top="auto",
                right="auto",
                height="100%",
                width="100%",
            ),
        ),
        direction="bottom",
    )

def tk8_mobile_navbar() -> rx.Component:
    return rx.mobile_only(
        rx.drawer.root(
            rx.drawer.trigger(
                rx.button(rx.icon("menu"), margin_top="1em"), background="#62499e"
            ),
            rx.drawer.overlay(),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.vstack(
                        rx.drawer.close(
                            rx.button(rx.icon("menu"), background="#62499e")
                        ),
                        mobile_navbar_button("Home",image="/logo_white.webp", url="/"),
                        mobile_navbar_button("Project's Github",image="/github.svg", url=GITHUB),
                        mobile_navbar_button("Follow me on X!",image="/x-twitter.svg", url=TWITTER),
                        mobile_navbar_button("Donate",image="/kofi.webp", url=KOFI),
                        # Add more links here if needed
                        spacing="4",  # Adjust spacing between items as needed
                        width="100%",
                    ),
                    justify="center",
                    padding="2em",
                    background="linear-gradient(180deg, rgba(21,14,27,1) 0%, rgba(37,20,78,1) 87%, rgba(57,24,36,1) 100%)",
                ),
                top="auto",
                right="auto",
                height="100%",
                width="100%",
            ),
        ),
        direction="bottom",
    )
    
def xko_mobile_navbar() -> rx.Component:
    return rx.mobile_only(
        rx.drawer.root(
            rx.drawer.trigger(
                rx.button(rx.icon("menu"), margin_top="1em"), background="#62499e"
            ),
            rx.drawer.overlay(),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.vstack(
                        rx.drawer.close(
                            rx.button(rx.icon("menu"), background="#62499e")
                        ),
                        mobile_navbar_button("Home",image="/logo_white.webp", url="/"),
                        mobile_navbar_button("Project's Github",image="/github.svg", url=GITHUB),
                        mobile_navbar_button("Follow me on X!",image="/x-twitter.svg", url=TWITTER),
                        mobile_navbar_button("Donate",image="/kofi.webp", url=KOFI),
                        # Add more links here if needed
                        spacing="4",  # Adjust spacing between items as needed
                        width="100%",
                    ),
                    justify="center",
                    padding="2em",
                    background="linear-gradient(180deg, rgba(28,29,31,1) 73%, rgba(205,245,100,1) 100%)",
                ),
                top="auto",
                right="auto",
                height="100%",
                width="100%",
            ),
        ),
        direction="bottom",
    )



# def mobile_navbar() -> rx.Component:
#     return rx.mobile_only(rx.drawer.root(
#     rx.drawer.trigger(rx.button(rx.icon("menu")), background="#62499e"),
#     rx.drawer.overlay(),
#     rx.drawer.portal(
#         rx.drawer.content(
#             rx.flex(
#                 rx.vstack(
#                 rx.drawer.close(rx.box(rx.button(rx.icon("menu"),
#                     background="#62499e"),
                                       
#                 rx.link("Home", href="/", is_external=False,),
#                 rx.link("Home", href="/", is_external=False,),
#                 flex_direction="row",
#                ),
#             ),
#                 align_items="start",
#                 direction="row",
#             ),
#             top="auto",
#             right="auto",
#             height="100%",
#             width="100%",
#             padding="2em",
#             background="linear-gradient(180deg, rgba(38,28,47,1) 0%, rgba(57,46,84,1) 87%, rgba(97,43,63,1) 100%)",
#             # background_color=rx.color("green", 3)
#         )
#     ),
# ),
#     direction="bottom",
#     ))
