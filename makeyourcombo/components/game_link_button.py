import reflex as rx

def game_link_button(image: str, url: str, alt: str) -> rx.Component:
    return rx.link(
        rx.image(
            src=image,
            alt=alt,
            sizes="100%, 60%, 40%, 20%",
            border_radius="0.8em",
            
        ),
        href=url,
        is_external=False
    )