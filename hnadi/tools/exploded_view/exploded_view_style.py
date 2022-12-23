# Copyright (c) 2022, HNADIACE.  All rights reserved.

__all__ = ["HNADI_window_style"]

from omni.ui import color as cl
from omni.ui import constant as fl
from omni.ui import url
import omni.kit.app
import omni.ui as ui
import pathlib

EXTENSION_FOLDER_PATH = pathlib.Path(
    omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__)
)

##颜色预设##
#主题色
main_color = cl.hnadi_color = cl("#F5B81B")
#主字体色
white = cl.hnadi_text_color = cl("#DADADA") # 最浅色
#窗口
cl.window_label_bg = cl("#0F0F0F") # 窗口标题背景色
cl.window_bg = cl("#252525") # 窗口背景色，60~90%透明度（透明度不知道定义）
#折叠框架
cl.clloapsible_bg_label = cl("#252525")
#按钮
cl.button_bg = cl("#252525") # 常规背景色+边框#9393939，1px
cl.button_bg_hover = cl("#98999C")
cl.button_bg_click = cl("#636363")
cl.button_label = cl("#939393") # 按钮常规字体颜色
cl.button_label_hover = cl("#383838") # 按钮悬停时字体颜色
cl.button_label_click = cl("#DADADA")
#下拉框
cl.combobox_bg = cl("#252525")
cl.combobox_label = cl("#939393")
cl.combobox_bg_hover = cl("#0F0F0F")
cl.combobox_label_hover = cl("#AFAFAF")
#勾选框/还原按钮
cl.revert_arrow_enabled = cl("#AFAFAF") # 启用状态
cl.revert_arrow_disabled = cl("#383838") # 禁用状态
cl.checkbox_hover = cl("#DADADA")
cl.checkbox_click = cl("#F5B81B")
#边界线框
border_color = cl.border = cl("#636363") # 1px-2px厚度
#滑块
cl.slider_fill = cl("#F5B81B") # 滑块填充色，主题色
cl.slider_bg = cl("#252525")
cl.floatslider_sele = cl("#BB8E1A") # 滑块点击效果
cl.slider_text_color = cl("98999C")
#还原按钮
cl.revert_arrow_enabled = cl("#F5B81B") # 启用状态
cl.revert_arrow_disabled = cl("#383838") # 禁用状态
#好像用不到的
cl.transparent = cl(0, 0, 0, 0)
# HC Color
black = cl("#252525")
white = cl("#FFFFFF")
cls_temperature_gradient = [cl("#fe0a00"), cl("#f4f467"), cl("#a8b9ea"), cl("#2c4fac"), cl("#274483"), cl("#1f334e")]


## 间距预设 ##
fl.window_attr_hspacing = 8 # 文字与功能框间距（全部）
fl.window_attr_spacing = 4 # 纵向间距
fl.group_spacing = 4 # 组间间距
fl.spacing = 4 
fl.border_radius = 4
fl.border_width = 1


## 字体大小 ##
fl.window_title_font_size = 18
fl.collapsable_font_size = 16
fl.text_font_size = 14


## 链接 ##
url.icon_achiview = f"{EXTENSION_FOLDER_PATH}/image/achi_view.png"
url.icon_achiview_click = f"{EXTENSION_FOLDER_PATH}/image/achi_view_click.png"
url.icon_bowlgenerator = f"{EXTENSION_FOLDER_PATH}/image/bowl_generator.png"
url.icon_bowlgenerator_click = f"{EXTENSION_FOLDER_PATH}/image/bowl_generator_click.png"
url.icon_buildingblock = f"{EXTENSION_FOLDER_PATH}/image/building_block.png"
url.icon_buildingblock_click = f"{EXTENSION_FOLDER_PATH}/image/building_blockc_click.png"
url.icon_draincurve = f"{EXTENSION_FOLDER_PATH}/image/drain_curve.png"
url.icon_draincurve_click = f"{EXTENSION_FOLDER_PATH}/image/drain_curve_click.png"
url.icon_explodedview = f"{EXTENSION_FOLDER_PATH}/image/exploded_view.png"
url.icon_explodedview_click = f"{EXTENSION_FOLDER_PATH}/image/exploded_view_click.png"
url.icon_isochronouscircle = f"{EXTENSION_FOLDER_PATH}/image/isochronouscircle.png"
url.icon_isochronouscircle_click = f"{EXTENSION_FOLDER_PATH}/image/isochronouscircle_click.png"
url.icon_light_studio = f"{EXTENSION_FOLDER_PATH}/image/light_studio.png"
url.icon_lightstudio_click = f"{EXTENSION_FOLDER_PATH}/image/light_studio_click.png"
url.icon_solarpanel = f"{EXTENSION_FOLDER_PATH}/image/solar_panel.png"
url.icon_solarpanel_click = f"{EXTENSION_FOLDER_PATH}/image/solar_panel_click.png"
url.closed_arrow_icon = f"{EXTENSION_FOLDER_PATH}/image/closed.svg"
url.radio_btn_on_icon = f"{EXTENSION_FOLDER_PATH}/image/Slice 3.png"
url.radio_btn_off_icon = f"{EXTENSION_FOLDER_PATH}/image/Slice 1.png"
url.radio_btn_hovered_icon = f"{EXTENSION_FOLDER_PATH}/image/Slice 2.png"


## Style格式说明 ##
"""
"Button":{"border_width":0.5}  # 1———为一类控件指定样式,直接"WidgetType":{}
"Button::B1":{XXXX}  # 2———为一类控件下的某个实例指定特殊样式,"WidgetType::InstanceName":{}
"Button::B1:hovered/pressed":{XXXX}  # 3———为一类控件的某个实例的某个状态指定样式,"WidgetType::InstanceName:State":{}
"Button.Label::B1":{}  # 3———为一类控件的某个实例的某种属性指定样式,"WidgetType.AttributeName::InstanceName":{}
"""


HNADI_window_style = {
# 属性字体 attribute_name
    "Label::attribute_name": {
        "alignment": ui.Alignment.RIGHT_CENTER,
        "margin_height": fl.window_attr_spacing,
        "margin_width": fl.window_attr_hspacing,
        "color": cl.button_label,
    },

    "Label::attribute_name:hovered": {"color": cl.hnadi_text_color},

# 可折叠标题 
# 可折叠标题文字 collapsable_name
    "Label::collapsable_name": {
        "alignment": ui.Alignment.LEFT_CENTER,
        "color": cl.hnadi_text_color,
        "font_size": fl.collapsable_font_size,
        },
# 可折叠标题命名（间隔属性） group 
    "CollapsableFrame::group": {"margin_height": fl.group_spacing},
# HeaderLine 线 
    "HeaderLine": {"color": cl(.5, .5, .5, .5)},


# 滑杆
    "Slider": {
        "border_radius": fl.border_radius,
        "color": cl.slider_text_color,
        "background_color": cl.slider_bg,
        "secondary_color": cl.slider_fill,
        "secondary_selected_color": cl.floatslider_sele,
        "draw_mode": ui.SliderDrawMode.HANDLE,
    },
# FloatSlider attribute_float
    "Slider::attribute_float": {"draw_mode": ui.SliderDrawMode.FILLED},
    "Slider::attribute_float:hovered": {
        "color": cl.slider_text_color,
        "background_color": cl.slider_bg
        },
    "Slider::attribute_float:pressed": {"color": cl.slider_text_color},
# IntSlider attribute_int
    "Slider::attribute_int": {
        "secondary_color": cl.slider_fill,
        "secondary_selected_color": cl.floatslider_sele,
    },
    "Slider::attribute_int:hovered": {"color": cl.slider_text_color},
    "Slider::attribute_float:pressed": {"color": cl.slider_text_color},

# 按钮 tool_button
    "Button::tool_button": {
        "background_color": cl.button_bg,
        "border_width": fl.border_width,
        "border_color": cl.border,
        "border_radius": fl.border_radius,
        },
    "Button::tool_button:hovered": {"background_color": cl.button_bg_hover},
    "Button::tool_button:pressed": {"background_color": cl.button_bg_click},
    "Button::tool_button:checked": {"background_color": cl.button_bg_click},
    "Button::tool_button:pressed": {"background_color": cl.slider_fill},
    "Button.Label::tool_button:hovered": {"color": cl.button_label_hover},
    "Button.Label::tool_button:pressed": {"color": white},
    "Button.Label::tool_button": {"color": cl.button_label},



# # 图片按钮 image_button
#     "Button::image_button": {
#         "background_color": cl.transparent,
#         "border_radius": fl.border_radius,
#         "fill_policy": ui.FillPolicy.PRESERVE_ASPECT_FIT,
#         },
#     "Button.Image::image_button": {
#         "image_url": url.icon_achiview,
#         "alignment": ui.Alignment.CENTER_TOP,
#         "border_radius": fl.border_radius,
#     },
#     "Button.Image::image_button:checked": {"image_url": url.icon_achiview_click},
#     "Button::image_button:hovered": {"background_color": cl.button_bg_hover},
#     "Button::image_button:pressed": {"background_color": cl.button_bg_click},
#     "Button::image_button:checked": {"background_color": cl.imagebutton_bg_click},

# Field attribute_field
    "Field": {
        "background_color": cl.slider_bg,
        "border_radius": fl.border_radius,
        "border_color": cl.border,
        "border_width": fl.border_width,
    },
    "Field::attribute_field": {
        "corner_flag": ui.CornerFlag.RIGHT,
        "font_size": fl.text_font_size, 
    },
    "Field::attribute_field:hovered":{"background_color": cl.combobox_bg_hover},
    "Field::attribute_field:pressed":{"background_color": cl.combobox_bg_hover},
# cl.slider_fill




# # 下拉框
    "Rectangle::box": {
        "background_color": cl.slider_fill,
        "border_radius": fl.border_radius,
        "border_color": cl.slider_fill,
        "border_width": 0,
        "color": cl.combobox_label, 
    },

#     "ComboBox::dropdown_menu":{
#         "background_color": cl.combobox_bg,
#         "secondary_color": 0x0,
#         "font_size": fl.text_font_size,

#     },
#     "ComboBox::dropdown_menu:hovered":{
#         "color": cl.combobox_label_hover,
#         "background_color": cl.combobox_bg_hover,
#         "secondary_color": cl.combobox_bg_hover,
#     },
#     "ComboBox::dropdown_menu:pressed":{
#         "background_color": cl.combobox_bg_hover,
#         "border_color": cl.border,
    # },
    # "Rectangle::combobox_icon_cover": {"background_color": cl.field_bg},

# RadioButtion
    # "Button::radiobutton":{
    #     "background_color":cl.transparent,
    #     "image_url": url.radio_btn_off_icon,
    # },
    # "Button::radiobutton:pressed":{"image_url": url.radio_btn_on_icon},
    # "Button::radiobutton:checked":{"image_url": url.radio_btn_on_icon},
    
#图片
    # "Image::radio_on": {"image_url": url.radio_btn_on_icon},
    # "Image::radio_off": {"image_url": url.radio_btn_off_icon},
    # "Image::collapsable_opened": {"color": cl.example_window_text, "image_url": url.example_window_icon_opened},
    # "Image::collapsable_closed": {"color": cl.example_window_text, "image_url": url.example_window_icon_closed},   
    # "Image::collapsable_closed": {
    #     "color": cl.collapsible_header_text,
    #     "image_url": url.closed_arrow_icon,
    # },
    # "Image::collapsable_closed:hovered": {
    #     "color": cl.collapsible_header_text_hover,
    #     "image_url": url.closed_arrow_icon,
    # },
}
