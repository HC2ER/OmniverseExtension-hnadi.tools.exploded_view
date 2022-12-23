from os import path
from data.image_path import image_path

from functools import partial
import omni.ui as ui
from .exploded_view import select_explode_Xform, on_ratio_change, on_pivot_change, remove_item, add_item, bind_item, unbind_item, hide_unhide_original_model, reset_model, clear, set_camera
from .exploded_view_style import HNADI_window_style, main_color, white, border_color

# Connect to Extension
class Cretae_UI_Framework(ui.Window):
    def __init__(self, transformer) -> None:
        self = transformer
        spacer_distance = distance = 6
        overall_width = 380
        overall_height = 395

        self._window = ui.Window("Exploded View", width=overall_width, height=overall_height)
        with self._window.frame:
            with ui.VStack(style=HNADI_window_style):
                # Column1 Main Functions UI
                with ui.HStack(height = 170):
                    # two big buttons
                    ui.Spacer(width=6)
                    with ui.VStack(width = 120):
                        ui.Spacer(height = distance - 1)
                        select_button = create_button_type1(name="Select Prims", tooltip="Select a group or all items at once to explode.", pic=image_path.select, height=102, spacing=-45)
                        ui.Spacer(height = 4)
                        camera_button = create_button_type1_1(name="Axono", tooltip="Set an axonometirc camera.", pic=image_path.Axono, height=53, spacing=-20)

                    ui.Spacer(width = 10)

                    # four main control sliders
                    with ui.VStack():
                        ui.Spacer(height = distance+2)
                        x_button = create_floatfield_ui(label="X ratio", tooltip="Explosion distance ratio in X direction", max=100.0)
                        ui.Spacer(height = 2)

                        y_button = create_floatfield_ui(label="Y ratio", tooltip="Explosion distance ratio in Y direction", max=100.0)
                        ui.Spacer(height = 2)

                        z_button = create_floatfield_ui(label="Z ratio", tooltip="Explosion distance ratio in Z direction", max=100.0)
                        ui.Spacer(height = 2)

                        ui.Spacer(height = 4)
                        with ui.HStack():
                            ui.Label("Pivot", name="attribute_name", width = 40, height=25, tooltip="Coordinates of the Explosion_Centre")
                            ui.Spacer(width=10)
                            with ui.HStack():
                                x_coord = create_coord_ui(name="X", color=0xFF5555AA)
                                ui.Spacer(width=10)
                                y_coord = create_coord_ui(name="Y", color=0xFF76A371)
                                ui.Spacer(width=10)
                                z_coord = create_coord_ui(name="Z", color=0xFFA07D4F)
                    ui.Spacer(width=6)

                # Column2 Edit Functions UI              
                with ui.CollapsableFrame("Edit Exploded Model", name="group", build_header_fn=_build_collapsable_header):
                    with ui.VStack():
                        with ui.HStack():
                            ui.Spacer(width=6)
                            add_button = create_button_type2(name="Add", tooltip="Add items into the Exploded_Model.", pic=image_path.add1, spacing=-85)
                            ui.Spacer(width=1)
                            bind_button = create_button_type2(name="Bind", tooltip="Bind items together to keep their relative distances during explosion.", pic=image_path.bind, spacing=-75)
                            ui.Spacer(width=6)
                        with ui.HStack():
                            ui.Spacer(width=6)
                            remove_button = create_button_type2(name="Remove", tooltip="Remove items from the Exploded_Model", pic=image_path.remove1, spacing=-85)
                            ui.Spacer(width=1)
                            unbind_button = create_button_type2(name="Unbind", tooltip="Unbind items.", pic=image_path.unbind, spacing=-75)
                            ui.Spacer(width=6)
                        ui.Spacer(height = 5)
                ui.Spacer(height = 6)

                # Column3 Other Functions UI 
                with ui.HStack():
                    ui.Spacer(width=6)
                    hideorshow_button = create_button_type3(tooltip="Hide or show the ORIGINAL prims.", pic=image_path.hide_show)
                    reset_button = create_button_type3(tooltip="Reset the Exploded_Model.", pic=image_path.reset)
                    clear_button = create_button_type3(tooltip="Delete the Exploded_Model and all data.", pic=image_path.clear)
                    ui.Spacer(width=6)

                # Connect functions to button
                select_button.set_clicked_fn(partial(select_explode_Xform, x_coord, y_coord, z_coord, x_button, y_button, z_button))
                camera_button.set_clicked_fn(set_camera)

                x_button.model.add_value_changed_fn(partial(on_ratio_change, x_button, y_button, z_button, x_coord, y_coord, z_coord))
                y_button.model.add_value_changed_fn(partial(on_ratio_change, x_button, y_button, z_button, x_coord, y_coord, z_coord))
                z_button.model.add_value_changed_fn(partial(on_ratio_change, x_button, y_button, z_button, x_coord, y_coord, z_coord))

                x_coord.model.add_value_changed_fn(partial(on_pivot_change, x_coord, y_coord, z_coord, x_button, y_button, z_button))
                y_coord.model.add_value_changed_fn(partial(on_pivot_change, x_coord, y_coord, z_coord, x_button, y_button, z_button))
                z_coord.model.add_value_changed_fn(partial(on_pivot_change, x_coord, y_coord, z_coord, x_button, y_button, z_button))

                add_button.set_clicked_fn(partial(add_item, x_coord, y_coord, z_coord, x_button, y_button, z_button))
                remove_button.set_clicked_fn(partial(remove_item, x_coord, y_coord, z_coord, x_button, y_button, z_button))
                bind_button.set_clicked_fn(partial(bind_item, x_coord, y_coord, z_coord, x_button, y_button, z_button))
                unbind_button.set_clicked_fn(partial(unbind_item, x_coord, y_coord, z_coord, x_button, y_button, z_button))

                hideorshow_button.set_clicked_fn(hide_unhide_original_model)
                reset_button.set_clicked_fn(partial(reset_model, x_coord, y_coord, z_coord, x_button, y_button, z_button))
                clear_button.set_clicked_fn(partial(clear, x_coord, y_coord, z_coord, x_button, y_button, z_button))


def _build_collapsable_header(collapsed, title):
    """Build a custom title of CollapsableFrame"""
    with ui.VStack():
        ui.Spacer(height=5)

        with ui.HStack():
            ui.Label(title, name="collapsable_name")
            if collapsed:
                image_name = "collapsable_opened"
            else:
                image_name = "collapsable_closed"
            ui.Image(name=image_name, width=10, height=10)

        ui.Spacer(height=5)
        ui.Line(style_type_name_override="HeaderLine")


# UI button style
def create_coord_ui(color:str, name:str):
    with ui.ZStack(width=13, height=25):
        ui.Rectangle(name="vector_label", width=15, style={"background_color":main_color, "border_radius":3})
        ui.Label(name, alignment=ui.Alignment.CENTER, style={"color":white})
    coord_button =ui.FloatDrag(min=-99999999.9, max=99999999.9)
    return coord_button


def create_floatfield_ui(label:str, max:float, tooltip:str, min=0.0):
    with ui.HStack():
        ui.Label(label, name="attribute_name", width=40, height=25, tooltip=tooltip)
        ui.Spacer(width=1.5)
        button = ui.FloatField(min=min, max=max, height=25)
        button.model.set_value(0.0)
    return button


def create_button_type1(name, tooltip, pic, height, spacing=-45):
    style = {
        "Button":{"stack_direction":ui.Direction.TOP_TO_BOTTOM},

        "Button.Label":{"alignment":ui.Alignment.CENTER_BOTTOM},
        
        # "border_width": 0.1,
        # "border_color": border_color,
        "border_radius": 4,

        "Button.Image":{# "color":0xffFFFFFF,
        "image_url":pic,
        "alignment":ui.Alignment.CENTER_BOTTOM,},

        ":hovered":{
        "background_gradient_color":main_color,
        "background_color":0X500066FF}}
    button = ui.Button(name, height=height, width=120, tooltip=tooltip, style=style)
    button.spacing = spacing
    return button


def create_button_type1_1(name, tooltip, pic, height, spacing=-20):
    style = {
        "Button":{"stack_direction":ui.Direction.LEFT_TO_RIGHT},
        "Button.Image":{# "color":0xffFFFFFF,
        "image_url":pic,
        "alignment":ui.Alignment.CENTER_BOTTOM,},
        "Button.Label":{"alignment":ui.Alignment.CENTER},

        "border_radius": 4,

        ":hovered":{
        "background_gradient_color":main_color,
        "background_color":0X500066FF}}
    button = ui.Button(name, height=height, width=120, tooltip=tooltip, style=style)
    button.spacing = spacing
    return button


def create_button_type2(name, tooltip, pic, height=40, spacing=-75):
    style={ 
        "Button":{"stack_direction":ui.Direction.LEFT_TO_RIGHT},
        "Button.Image":{# "color":0xffFFFFFF,
        "image_url":pic,
        "alignment":ui.Alignment.CENTER,},
        "Button.Label":{"alignment":ui.Alignment.CENTER},
    
        "background_color":0x10CCCCCC,

        ":hovered":{
        "background_gradient_color":0X500066FF,
        "background_color":main_color},
        
        "Button:pressed:":{"background_color":0xff000000}}
    button = ui.Button(name, height=height, tooltip=tooltip, style=style)
    button.spacing = spacing
    return button


def create_button_type3(tooltip, pic, height=50):
    style = {
        "Button":{"stack_direction":ui.Direction.TOP_TO_BOTTOM},
        "Button.Image":{# "color":0xffFFFFFF,
        "image_url":pic,
        "alignment":ui.Alignment.CENTER,},
        "Button.Label":{"alignment":ui.Alignment.CENTER},

        "border_radius": 4,
        
        ":hovered":{
        "background_gradient_color":main_color,
        "background_color":0X500066FF}}
    button = ui.Button("", height = height, style = style, tooltip = tooltip)
    return button