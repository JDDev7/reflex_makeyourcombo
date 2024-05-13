import reflex as rx

def mobile_navbar_button(text: str, image: str, url: str) -> rx.Component:
    return rx.chakra.button(
        rx.hstack(
        rx.image(src=image, width="1.5em",height="auto"),
        rx.link(text,font_size="1em", color="white", text_align="center", href=url, is_external=False),
        variant="link",
        spacing="5",
        
        ),
        width="100%",
    )