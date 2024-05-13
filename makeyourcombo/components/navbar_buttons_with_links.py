import reflex as rx
def navbar_button_with_link(text: str, image: str, url: str, external: bool) -> rx.Component:
    return rx.link(
        rx.button(
            rx.image(src=image, width=["1.35rem","2rem"], padding_x="0.2em", border_radius="0.2em"),
            rx.text(text, color="white", font_size=["0.7em", "0.8em", "1em"], padding_x="0.2em"),
            background="#62499e",
            width="100%",
            
        padding_x="0.5em"),
        href=url,
        is_external=external,
        high_contrast=True
    )