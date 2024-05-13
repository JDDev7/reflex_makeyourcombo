import reflex as rx
from makeyourcombo.components.footer import footer

from makeyourcombo.components.navbar import game_navbar, tk8_mobile_navbar
from makeyourcombo.components.tk8_input_buttons import *
from PIL import Image, ImageDraw, ImageFont
import base64
import os
from typing import Dict



# State to handle the selected character and its associated image.
class CharacterState(rx.State):
    selected_character: str = "Alisa"
    image_path: str = "/tekken_8/characters/alisa.webp"


    def select_character(self, character: str, image_path: str):
        self.selected_character = character
        self.image_path = image_path
        
# State to handle the input images

class ComboState(rx.State):
    current_combo: list[str]
    combo_name : str = ""
    directional_inputs = directional_inputs_dict
    normal_button_inputs = normal_buttons_dict
    special_inputs = special_inputs_dict
    all_inputs: Dict[str, str] = {**directional_inputs, **normal_button_inputs, **special_inputs}
    merged_image_data: str = ""

    def add_move(self, m: str):
        self.current_combo.append(m)
        print(self.current_combo)
        print(self.combo_name)
        
    def remove_move(self):
        self.current_combo.pop()
        print(self.current_combo)
        
    def get_image_path(self, key):
        return self.all_inputs[key]

    def merge_images(self, image_values, output_path, spacing=10):
        image_paths = [self.get_image_path(value) for value in image_values]
        images = [Image.open(rx.get_upload_dir() / image_path).convert('RGBA') for image_path in image_paths]

        total_width = sum(img.width + spacing for img in images[:-1]) + images[-1].width
        max_height = max(img.height for img in images)

        extra_space = 30  # Space for text above the image
        concatenated_image = Image.new("RGBA", (total_width, max_height + extra_space), (0, 0, 0, 0))

        x_offset = 0
        for img in images:
            alpha_background = Image.new("RGBA", img.size, (0, 0, 0, 0))
            alpha_background.alpha_composite(img)
            concatenated_image.alpha_composite(alpha_background, (x_offset, extra_space))  # Add extra_space to shift images down
            x_offset += img.width + spacing

        concatenated_image.save(output_path)
    def merge_images_and_download(self, combo_name: str):
        image_values = list(self.current_combo)

        if not image_values:  # Check if current_combo is empty
            return rx.window_alert("Please create a combo before downloading.")
        output_path = "your_combo.png"

        self.merge_images(image_values, output_path)
        font_path = rx.get_upload_dir() / "tekken_8/fonts/bebasneuepro.ttf"
        custom_font_size = 24

        font = ImageFont.truetype(font_path, custom_font_size)
        text = combo_name.upper()

        extra_space = 30  # Space for text above the image

        with Image.open(output_path) as img:
            draw = ImageDraw.Draw(img)

            img.save(output_path)

        if combo_name:  # Add the background image only if combo_name has text
            bg_image_path = bg_image_path = rx.get_upload_dir() / "tekken_8/inputs/background.png"
            bg_image = Image.open(bg_image_path).convert('RGBA')

            with Image.open(output_path) as img:
                img_with_text_space = Image.new("RGBA", (img.width, img.height + extra_space), (0, 0, 0, 0))
                img_with_text_space.alpha_composite(img, (0, extra_space))

                bg_position = (10, -20)  # Adjust the position as needed
                img_with_text_space.paste(bg_image, bg_position, mask=bg_image)

                draw = ImageDraw.Draw(img_with_text_space)
                draw.text((15, 15), text, fill="white", font=font)
                img_with_text_space.save(output_path)

        with open(output_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        os.remove(output_path)

        download_script = f'''
        (function() {{
            var binaryData = atob("{image_data}");
            var dataArray = new Uint8Array(binaryData.length);
            for (var i = 0; i < binaryData.length; i++) {{
                dataArray[i] = binaryData.charCodeAt(i);
            }}
            var blob = new Blob([dataArray], {{ type: "image/png" }});
            var objectURL = URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = objectURL;
            a.download = "your_combo.png";
            a.style.display = "none";
            document.body.appendChild(a);
            a.click();
            URL.revokeObjectURL(objectURL);
            document.body.removeChild(a);
        }})();
        '''
        return rx.call_script(download_script)
    
    
# Function to build the dropdown menu and the display container.
def character_menu(character_dict):
    menu_items = [
        rx.menu.item(
            character,
            on_select=CharacterState.select_character(character, image_path)
        )
        for character, image_path in character_dict.items()
    ]
    return rx.vstack(
        rx.menu.root(
            rx.menu.trigger(
                rx.button("Select Character", margin_y=["1em", "1.5em"], background="#62499e"),
            ),
            rx.menu.content(
                *menu_items
            ),
        ),min_width="1rem",)
    

@rx.page(route="/tk8", title="Make your Combo | Tekken 8 Combo Maker")
def tk8_page() -> rx.Component:
    return rx.flex(rx.flex(rx.center(
        rx.vstack(
            tk8_mobile_navbar(),
            game_navbar(),
            
rx.box(
    rx.center(
        rx.image(src=CharacterState.image_path, border_radius="1.2em"),
        width="100%",
    ),
    #padding_x="1em",
    width=["100%"],
    align="center",
    justify="center",

),rx.tablet_and_desktop(
            rx.hstack(
                character_menu(character_dict),
                #rx.spacer(direction="row", spacing="2"),
                rx.hstack(
                    rx.input(value=ComboState.combo_name,on_change=ComboState.set_combo_name,placeholder="Combo Name(Wall Combo, etc.)",min_width="10rem", width="100%", float="right", font_size=["0.6rem","0.8rem"], background="#392861"),
                    rx.button("Clear Combo", on_click=ComboState.set_current_combo([]), background="#62499e", width="30%"),
                    rx.button("Delete Last Input", on_click=ComboState.remove_move(ComboState.current_combo), background="#62499e", width="30%"),
                    rx.button("Download Combo", on_click=ComboState.merge_images_and_download(ComboState.combo_name), background="#62499e", width="30%"),

                ),
                align_items="center",
                justify_content="space-between",
                # margin_left="2em", 
                # margin_bottom="1.2em", 
                # width="40%",
                # padding_x="2em",
                min_width="20rem",
                width="100%",
                padding_x="7.5rem",
            ),),
            rx.mobile_only(
                rx.vstack(rx.input(placeholder="Combo Name(Wall Combo, etc.)", width="100%", float="right", font_size="0.6rem", background="#392861", color="white", min_width="10rem"),
                    rx.button("Clear Combo", on_click=ComboState.set_current_combo([]), background="#62499e", width="50%"),
                    rx.button("Delete Last Input", on_click=ComboState.remove_move(ComboState.current_combo), background="#62499e", width="50%"),
                    rx.button("Download Combo", on_click=ComboState.merge_images_and_download(ComboState.combo_name), background="#62499e", width="50%"),
                    character_menu(character_dict),
                    align_items= "center",
                    justify_content="space-between",
                    min_width="20rem",
                    width="100%"),
                margin="auto",
                ),
            rx.spacer(spacing="2"),
            rx.vstack(
                #directional inputs (b, db, d, df, f, uf, u, ub and holds)
                rx.chakra.heading("Directional Inputs", size="md", color="white", padding_left="4rem"),
                rx.hstack(
                    rx.foreach(
                    ComboState.directional_inputs,
                    lambda m: rx.chakra.button(rx.image(src=rx.get_upload_url(m[1]), width="2em",height="auto", margin_x="0.2em",),variant="unstyled", on_click=ComboState.add_move(m[0]))
                ),
                width="100%",
                height="auto",
                #padding_left="1.3em",
                #padding_right="-0.5em",
                #margin_left="1em",
                wrap="wrap",
                background_color="#101624",
                border_radius="1.2em",
                justify_content="center",
                align_items="center",
                ),
                # Normal inputs (1, 2, 3, 4, 12, 13, 14, 23, 24, 34, 134)
                rx.chakra.heading("Normals", size="md", color="white", padding_left="4rem"),
                rx.hstack(
                    rx.foreach(
                    ComboState.normal_button_inputs,
                    lambda m: rx.chakra.button(rx.image(src=rx.get_upload_url(m[1]), width="2em",height="auto", margin_x="0.2em",),variant="unstyled", on_click=ComboState.add_move(m[0]))
                ),
                width="100%",
                height="auto",
                #padding_left="1.3em",
                #padding_right="-0.5em",
                #margin_left="1em",
                wrap="wrap",
                background_color="#101624",
                border_radius="1.2em",
                justify_content="center",
                align_items="center",
                ),
                # Special inputs (separation, walls, etc)
                rx.chakra.heading("Special Inputs", size="md", color="white", padding_left="4rem"),
                rx.hstack(
                    rx.foreach(
                    ComboState.special_inputs,
                    lambda m: rx.chakra.button(rx.image(src=rx.get_upload_url(m[1]), width="2em",height="auto", margin_x="0.2em",),variant="unstyled", on_click=ComboState.add_move(m[0]))
                ),
                width="100%",
                height="auto",
                #padding_left="1.3em",
                #padding_right="-0.5em",
                #margin_left="1em",
                wrap="wrap",
                background_color="#101624",
                border_radius="1.2em",
                justify_content="center",
                align_items="center",
                ),
                rx.chakra.heading("Your Combo", size="md", color="white", padding_left="4rem"),
                rx.hstack(
                    rx.foreach(
                        ComboState.current_combo,
                        lambda m: rx.image(src=rx.get_upload_url(ComboState.all_inputs[m]), width=["1.5rem", "2rem"], border_radius="0.5em"),
                    ),
                max_width="68rem",
                width="100%",
                padding="1rem",
                wrap="wrap",
                background_color="#101624",
                border_radius="1.2em",
                justify_content="center",
                align_items="center",
                margin_bottom="0.5rem"
                ),
            footer(),
            ),
                background="linear-gradient(180deg, rgba(21,14,27,1) 0%, rgba(37,20,78,1) 87%, rgba(57,24,36,1) 100%)",
            #background_color="#212b42",
            padding_x="1em",
            border_radius=["0em","0em","0em","0em","1.2em"],
        ),

    ),
    justify_content = "center",

    ),justify_content = "center",
    )
character_dict: dict = {
        "Alisa": "/tekken_8/characters/alisa.webp",
        "Asuka": "/tekken_8/characters/asuka.webp",
        "Azucena": "/tekken_8/characters/azucena.webp",
        "Bryan": "/tekken_8/characters/bryan.webp",
        "Claudio": "/tekken_8/characters/claudio.webp",
        "Devil Jin": "/tekken_8/characters/djin.webp",
        "Dragunov": "/tekken_8/characters/drag.webp",
        "Feng": "/tekken_8/characters/feng.webp",
        "Hwoarang": "/tekken_8/characters/hwo.webp",
        "Jack-8": "/tekken_8/characters/jack8.webp",
        "Jin": "/tekken_8/characters/jin.webp",
        "Jun": "/tekken_8/characters/jun.webp",
        "Kazuya": "/tekken_8/characters/kaz.webp",
        "King": "/tekken_8/characters/king.webp",
        "Kuma": "/tekken_8/characters/kuma.webp",
        "Lars": "/tekken_8/characters/lars.webp",
        "Law": "/tekken_8/characters/law.webp",
        "Lee": "/tekken_8/characters/lee.webp",
        "Leo": "/tekken_8/characters/leo.webp",
        "Leroy": "/tekken_8/characters/leroy.webp",
        "Lili": "/tekken_8/characters/lili.webp",
        "Nina": "/tekken_8/characters/nina.webp",
        "Panda": "/tekken_8/characters/panda.webp",
        "Paul": "/tekken_8/characters/paul.webp",
        "Raven": "/tekken_8/characters/raven.webp",
        "Reina": "/tekken_8/characters/reina.webp",
        "Shaheen": "/tekken_8/characters/shaheen.webp",
        "Steve": "/tekken_8/characters/steve.webp",
        "Victor": "/tekken_8/characters/victor.webp",
        "Xiaoyu": "/tekken_8/characters/ling.webp",
        "Yoshimitsu": "/tekken_8/characters/yoshi.webp",
        "Zafina": "/tekken_8/characters/zafina.webp"
    }
