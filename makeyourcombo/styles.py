import reflex as rx
from enum import Enum

class Size(Enum):
    ZERO = "0px !important"
    SMALL = "0.5em"
    MEDIUM = "0.8em"
    DEFAULT = "1em"
    BIG = "2em"

base_style = {
    rx.heading: {
        "font_size": ["1.25em", "1.5em", "2em", "2.5em"]       
    },
    rx.text: {
        "font_size": ["0.8em", "1em","1.2em", "1.5em"]
    }
}
