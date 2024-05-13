import reflex as rx
from makeyourcombo.components.footer import footer

from makeyourcombo.components.navbar import game_navbar, sf6_mobile_navbar
from makeyourcombo.components.sf6_input_buttons import *
from PIL import Image, ImageDraw, ImageFont
import base64
import os

from typing import Dict



# State to handle the selected character and its associated image.
class Sf6CharacterState(rx.State):
    selected_character: str = "Aki"
    image_path: str = "/sf6/characters/aki.webp"


    def select_character(self, character: str, image_path: str):
        self.selected_character = character
        self.image_path = image_path
        
# State to handle the input images

class Sf6ComboState(rx.State):
    current_combo: list[str]
    combo_name : str = ""
    sf6_directional_inputs = sf6_directional_inputs_dict
    sf6_normal_button_inputs = sf6_normal_buttons_dict
    sf6_special_inputs = sf6_special_inputs_dict
    all_inputs: Dict[str, str] = {**sf6_directional_inputs, **sf6_normal_button_inputs, **sf6_special_inputs}
    merged_image_data: str = ""

    def add_move(self, m: str):
        self.current_combo.append(m)
        print(self.current_combo)
        print(self.combo_name)
        
    def remove_move(self):
        self.current_combo.pop()
        print(self.current_combo)
        
    # def get_image_path(self, key):
    #     relative_path = self.all_inputs[key]
    #     project_root = os.path.dirname(os.path.abspath(__file__))
    #     assets_folder = os.path.join(project_root, '..', '..', 'assets')
    #     full_path = os.path.join(assets_folder, relative_path.strip('/'))
    #     return full_path
    
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
        font_path =  rx.get_upload_dir() / "helveticanowdisplay.ttf"
        custom_font_size = 18

        font = ImageFont.truetype(font_path, custom_font_size)
        text = combo_name.upper()

        extra_space = 30  # Space for text above the image

        with Image.open(output_path) as img:
            draw = ImageDraw.Draw(img)
            # draw.text((10, 10), text, fill="white", font=font)

            img.save(output_path)

        if combo_name:  # Add the background image only if combo_name has text
            bg_image_path = rx.get_upload_dir() / "background.png"
            bg_image = Image.open(bg_image_path).convert('RGBA')

            with Image.open(output_path) as img:
                img_with_text_space = Image.new("RGBA", (img.width, img.height + extra_space), (0, 0, 0, 0))
                img_with_text_space.alpha_composite(img, (0, extra_space))

                bg_position = (10, -30)  # Adjust the position as needed
                img_with_text_space.paste(bg_image, bg_position, mask=bg_image)

                draw = ImageDraw.Draw(img_with_text_space)
                draw.text((15, 20), text, fill="white", font=font)
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
            on_select=Sf6CharacterState.select_character(character, image_path)
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
    

@rx.page(route="/sf6", title="Make your Combo | Street Fighter 6 Combo Maker")
def sf6_page() -> rx.Component:
    return rx.flex(rx.flex(rx.center(
        rx.vstack(
            sf6_mobile_navbar(),
            game_navbar(),
            
rx.box(
    rx.center(
        rx.image(src=Sf6CharacterState.image_path, border_radius="1.2em"),
        width="100%",
    ),
    #padding_x="1em",
    width=["100%"],
    align="center",
    justify="center",

),rx.tablet_and_desktop(
            rx.hstack(
                character_menu(sf6_character_dict),
                #rx.spacer(direction="row", spacing="2"),
                rx.hstack(
                    rx.input(value=Sf6ComboState.combo_name,on_change=Sf6ComboState.set_combo_name,placeholder="Combo Name(Wall Combo, etc.)",min_width="10rem", width="100%", float="right", font_size=["0.6rem","0.8rem"], background="#392861"),
                    rx.button("Clear Combo", on_click=Sf6ComboState.set_current_combo([]), background="#62499e", width="30%"),
                    rx.button("Delete Last Input", on_click=Sf6ComboState.remove_move(Sf6ComboState.current_combo), background="#62499e", width="30%"),
                    rx.button("Download Combo", on_click=Sf6ComboState.merge_images_and_download(Sf6ComboState.combo_name), background="#62499e", width="30%"),

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
                    rx.button("Clear Combo", on_click=Sf6ComboState.set_current_combo([]), background="#62499e", width="50%"),
                    rx.button("Delete Last Input", on_click=Sf6ComboState.remove_move(Sf6ComboState.current_combo), background="#62499e", width="50%"),
                    rx.button("Download Combo", on_click=Sf6ComboState.merge_images_and_download(Sf6ComboState.combo_name), background="#62499e", width="50%"),
                    character_menu(sf6_character_dict),
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
                    Sf6ComboState.sf6_directional_inputs,
                    lambda m: rx.chakra.button(rx.image(src=rx.get_upload_url(m[1]), width="2em",height="auto", margin_x="0.2em",),variant="unstyled", on_click=Sf6ComboState.add_move(m[0]))
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
                    Sf6ComboState.sf6_normal_button_inputs,
                    lambda m: rx.chakra.button(rx.image(src=rx.get_upload_url(m[1]), width="2em",height="auto", margin_x="0.2em",),variant="unstyled", on_click=Sf6ComboState.add_move(m[0]))
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
                    Sf6ComboState.sf6_special_inputs,
                    lambda m: rx.chakra.button(rx.image(src=rx.get_upload_url(m[1]), width="2em",height="auto", margin_x="0.2em",),variant="unstyled", on_click=Sf6ComboState.add_move(m[0]))
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
                        Sf6ComboState.current_combo,
                        lambda m: rx.image(src=rx.get_upload_url(Sf6ComboState.all_inputs[m]), width=["1.5rem", "2rem"], border_radius="0.5em"),
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
                background="linear-gradient(90deg, rgba(97,16,150,1) 0%, rgba(55,5,135,1) 50%, rgba(97,16,150,1) 100%)",
            #background_color="#212b42",
            padding_x="1em",
            border_radius=["0em","0em","0em","0em","1.2em"],
        ),

    ),
    justify_content = "center",

    ),justify_content = "center",
    )
sf6_character_dict: dict = {
        "Aki": "/sf6/characters/aki.webp",
        "Blanka": "/sf6/characters/blanka.webp",
        "Cammy": "/sf6/characters/cammy.webp",
        "Chun-Li": "/sf6/characters/chun-li.webp",
        "Deejay": "/sf6/characters/deejay.webp",
        "Dhalsim": "/sf6/characters/dhalsim.webp",
        "Ed": "/sf6/characters/ed.webp",
        "Guile": "/sf6/characters/guile.webp",
        "E.Honda": "/sf6/characters/honda.webp",
        "Jamie": "/sf6/characters/jamie.webp",
        "JP": "/sf6/characters/jp.webp",
        "Juri": "/sf6/characters/juri.webp",
        "Ken": "/sf6/characters/ken.webp",
        "Kimberly": "/sf6/characters/kimberly.webp",
        "Lily": "/sf6/characters/lily.webp",
        "Luke": "/sf6/characters/luke.webp",
        "Manon": "/sf6/characters/manon.webp",
        "Marisa": "/sf6/characters/marisa.webp",
        "Rashid": "/sf6/characters/rashid.webp",
        "Ryu": "/sf6/characters/ryu.webp",
        "Zangief": "/sf6/characters/zangief.webp",
    }
