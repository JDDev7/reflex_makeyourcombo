import reflex as rx

class ThemeState(rx.State):
    # Assuming 'light' and 'dark' are acceptable values for appearance in Reflex
    appearance: str = 'light'  # Initial theme set to 'light'

    def toggle_theme(self):
        # Toggle between 'light' and 'dark' theme
        self.appearance = 'dark' if self.appearance == 'light' else 'light'

def color_mode_button():
    return rx.button(
        "Toggle Theme",
        on_click=ThemeState.toggle_theme,
        # Example of conditional prop usage based on the current theme
        color_scheme=rx.cond(ThemeState.appearance == 'light', 'dark', 'light')
    )