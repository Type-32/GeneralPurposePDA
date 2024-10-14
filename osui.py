import gc
import lvgl as lv
import utime
import connectivity as con
import asyncio

import pdaos_lib
from globals import QUEUED_NOTIFICATIONS
from pdaos_lib import Application, LVGLToObjectBindings, Notification

# import ui
# import ui_images


dispp = lv.display_get_default()
theme = lv.theme_default_init(dispp, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.RED), False,
                              lv.font_default())
dispp.set_theme(theme)

_ui_comp_table = {}
_ui_comp_prev = None
_ui_name_prev = None
_ui_child_prev = None
_ui_comp_table.clear()


def SetFlag(obj, flag, value: bool):
    if (value):
        obj.add_flag(flag)
    else:
        obj.remove_flag(flag)
    return


# COMPONENTS

# COMPONENT OptionsModal
def ui_OptionsModal_create(comp_parent, title: str = "Modal", content: str = "Content", opt1_label: str = "Option 1",
                           opt2_label: str = "Option 2", opt1: callable = None, opt2: callable = None):
    cui_OptionsModal = lv.obj(comp_parent)
    cui_OptionsModal.set_width(lv.pct(60))
    cui_OptionsModal.set_height(lv.SIZE_CONTENT)  # 50
    cui_OptionsModal.set_align(lv.ALIGN.CENTER)
    cui_OptionsModal.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    cui_OptionsModal.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
    SetFlag(cui_OptionsModal, lv.obj.FLAG.SCROLLABLE, False)
    cui_ModalTitle = lv.label(cui_OptionsModal)
    cui_ModalTitle.set_text(title)
    cui_ModalTitle.set_width(lv.pct(100))
    cui_ModalTitle.set_height(lv.SIZE_CONTENT)  # 1
    cui_ModalTitle.set_style_text_color(lv.color_hex(0x4C4C4C), lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_ModalTitle.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_ModalTitle.set_style_text_letter_space(1, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_ModalTitle.set_style_text_line_space(0, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_ModalTitle.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_ModalContent = lv.label(cui_OptionsModal)
    cui_ModalContent.set_text(content)
    cui_ModalContent.set_width(lv.pct(100))
    cui_ModalContent.set_height(lv.SIZE_CONTENT)  # 1
    cui_ModalContent.set_align(lv.ALIGN.CENTER)
    cui_Options = lv.obj(cui_OptionsModal)
    cui_Options.remove_style_all()
    cui_Options.set_height(40)
    cui_Options.set_width(lv.pct(100))
    cui_Options.set_align(lv.ALIGN.CENTER)
    cui_Options.set_flex_flow(lv.FLEX_FLOW.ROW)
    cui_Options.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
    SetFlag(cui_Options, lv.obj.FLAG.CLICKABLE, False)
    SetFlag(cui_Options, lv.obj.FLAG.SCROLLABLE, False)
    cui_Opt1 = lv.button(cui_Options)
    cui_Opt1.set_height(50)
    cui_Opt1.set_flex_grow(1)
    cui_Opt1.set_align(lv.ALIGN.CENTER)
    SetFlag(cui_Opt1, lv.obj.FLAG.SCROLLABLE, False)
    SetFlag(cui_Opt1, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
    cui_Opt1Text = lv.label(cui_Opt1)
    cui_Opt1Text.set_text(opt1_label)
    cui_Opt1Text.set_width(lv.SIZE_CONTENT)  # 1
    cui_Opt1Text.set_height(lv.SIZE_CONTENT)  # 1
    cui_Opt1Text.set_align(lv.ALIGN.CENTER)
    cui_Container9 = lv.obj(cui_Options)
    cui_Container9.remove_style_all()
    cui_Container9.set_width(10)
    cui_Container9.set_height(lv.pct(100))
    cui_Container9.set_align(lv.ALIGN.CENTER)
    SetFlag(cui_Container9, lv.obj.FLAG.CLICKABLE, False)
    SetFlag(cui_Container9, lv.obj.FLAG.SCROLLABLE, False)
    cui_Opt2 = lv.button(cui_Options)
    cui_Opt2.set_height(50)
    cui_Opt2.set_flex_grow(1)
    cui_Opt2.set_align(lv.ALIGN.CENTER)
    SetFlag(cui_Opt2, lv.obj.FLAG.SCROLLABLE, False)
    SetFlag(cui_Opt2, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
    cui_Option2Text = lv.label(cui_Opt2)
    cui_Option2Text.set_text(opt2_label)
    cui_Option2Text.set_width(lv.SIZE_CONTENT)  # 1
    cui_Option2Text.set_height(lv.SIZE_CONTENT)  # 1
    cui_Option2Text.set_align(lv.ALIGN.CENTER)
    _ui_comp_table[id(cui_OptionsModal)] = {"OptionsModal": cui_OptionsModal, "ModalTitle": cui_ModalTitle,
                                            "ModalContent": cui_ModalContent, "Options": cui_Options,
                                            "Options_Opt1": cui_Opt1, "Options_Opt1_Opt1Text": cui_Opt1Text,
                                            "Options_Container9": cui_Container9, "Options_Opt2": cui_Opt2,
                                            "Options_Opt2_Option2Text": cui_Option2Text, "_CompName": "OptionsModal"}
    return cui_OptionsModal


# COMPONENT App
def comp_App_AppButton_eventhandler(event_struct):
    target = event_struct.get_target()
    comp_App = ui_comp_get_root_from_child(target, "App")
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        (event_struct)
    return


def ui_App_create(comp_parent, app_title: str = "Untitled App", app_icon: str = "??", bg_color_hex: int = 0x5385ED):
    cui_App = lv.obj(comp_parent)
    cui_App.remove_style_all()
    cui_App.set_width(100)
    cui_App.set_height(100)
    cui_App.set_x(-200)
    cui_App.set_y(-30)
    cui_App.set_align(lv.ALIGN.CENTER)
    SetFlag(cui_App, lv.obj.FLAG.CLICKABLE, False)
    SetFlag(cui_App, lv.obj.FLAG.SCROLLABLE, False)
    cui_AppButton = lv.button(cui_App)
    cui_AppButton.set_width(80)
    cui_AppButton.set_height(80)
    cui_AppButton.set_align(lv.ALIGN.TOP_MID)
    SetFlag(cui_AppButton, lv.obj.FLAG.SCROLLABLE, False)
    SetFlag(cui_AppButton, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
    cui_AppButton.set_style_bg_color(lv.color_hex(bg_color_hex), lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_AppButton.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_AppIcon = lv.label(cui_AppButton)
    cui_AppIcon.set_text(app_icon)
    cui_AppIcon.set_width(lv.SIZE_CONTENT)  # 1
    cui_AppIcon.set_height(lv.SIZE_CONTENT)  # 1
    cui_AppIcon.set_align(lv.ALIGN.CENTER)
    cui_AppButton.add_event_cb(comp_App_AppButton_eventhandler, lv.EVENT.ALL, None)
    cui_AppTitle = lv.label(cui_App)
    cui_AppTitle.set_text(app_title)
    cui_AppTitle.set_width(lv.SIZE_CONTENT)  # 1
    cui_AppTitle.set_height(lv.SIZE_CONTENT)  # 1
    cui_AppTitle.set_align(lv.ALIGN.BOTTOM_MID)
    _ui_comp_table[id(cui_App)] = {"App": cui_App, "AppButton": cui_AppButton, "AppButton_AppIcon": cui_AppIcon,
                                   "AppTitle": cui_AppTitle, "_CompName": "App"}
    return cui_App


def comp_Notification_Notification_eventhandler(event_struct):
    target = event_struct.get_target()
    comp_Notification = ui_comp_get_root_from_child(target, "Notification")
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        # (event_struct)
        notif: Notification = QUEUED_NOTIFICATIONS.pop()
        notif.click_callback()
        remove_lvgl_object_binding(pdaos_lib.notif_identifier_hash(notif))
    return


def ui_Notification_create(comp_parent, notif: Notification):
    cui_Notification = lv.button(comp_parent)
    cui_Notification.set_height(70)
    cui_Notification.set_width(lv.pct(100))
    cui_Notification.set_align(lv.ALIGN.CENTER)
    cui_Notification.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    cui_Notification.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
    SetFlag(cui_Notification, lv.obj.FLAG.SCROLLABLE, False)
    SetFlag(cui_Notification, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
    cui_Notification.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_Notification.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_Notification.set_style_outline_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_Notification.set_style_outline_opa(50, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_Notification.set_style_outline_width(1, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_Notification.set_style_outline_pad(0, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_NotificationTitle = lv.label(cui_Notification)
    cui_NotificationTitle.set_text(notif.title)
    cui_NotificationTitle.set_width(lv.pct(100))
    cui_NotificationTitle.set_height(lv.SIZE_CONTENT)  # 100
    cui_NotificationTitle.set_align(lv.ALIGN.CENTER)
    cui_NotificationTitle.set_style_text_color(lv.color_hex(0x007EE3), lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_NotificationTitle.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_NotificationText = lv.label(cui_Notification)
    cui_NotificationText.set_text(notif.message)
    cui_NotificationText.set_width(lv.pct(100))
    cui_NotificationText.set_height(lv.SIZE_CONTENT)  # 100
    cui_NotificationText.set_align(lv.ALIGN.CENTER)
    cui_NotificationText.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_NotificationText.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
    cui_Notification.add_event_cb(comp_Notification_Notification_eventhandler, lv.EVENT.ALL, None)
    _ui_comp_table[id(cui_Notification)] = {"Notification": cui_Notification,
                                            "NotificationTitle": cui_NotificationTitle,
                                            "NotificationText": cui_NotificationText, "_CompName": "Notification"}
    return cui_Notification


# ui____initial_actions0 = lv.obj()
def OptionsModal_Options_Opt1_eventhandler(event_struct):
    target = event_struct.get_target()
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        (event_struct)
    return


def OptionsModal_Options_Opt2_eventhandler(event_struct):
    target = event_struct.get_target()
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        (event_struct)
    return


def HomeButton_eventhandler(event_struct):
    target = event_struct.get_target()
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        (event_struct)
    return


def _ui_comp_del_event(e):
    target = e.get_target()
    _ui_comp_table[id(target)].remove()


def ui_comp_get_child(comp, child_name):
    return _ui_comp_table[id(comp)][child_name]


def ui_comp_get_root_from_child(child, compname):
    for component in _ui_comp_table:
        if _ui_comp_table[component]["_CompName"] == compname:
            for part in _ui_comp_table[component]:
                if id(_ui_comp_table[component][part]) == id(child):
                    return _ui_comp_table[component]
    return None


keyboard: str = ""
KB_FOCUSED: bool = False


def set_keyboard_state(enabled: bool):
    global KB_FOCUSED
    SetFlag(ui_KeyboardContainer, lv.obj.HIDDEN, not enabled)
    KB_FOCUSED = enabled


def MainKeyboard_eventhandler(event_struct):
   target = event_struct.get_target()
   event = event_struct.code
   if event == lv.EVENT.READY and True:
      set_keyboard_state(False)
   return


def set_keyboard_content(content: str):
    global keyboard
    keyboard = content


def get_keyboard_content() -> str:
    global keyboard
    return keyboard


def get_local_current_time():
    current_time = utime.localtime()
    return "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])


ui_mainScreen = lv.screen_active()
ui_mainScreen.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
SetFlag(ui_mainScreen, lv.obj.FLAG.SCROLLABLE, False)

ui_MainContainer = lv.obj(ui_mainScreen)
ui_MainContainer.remove_style_all()
ui_MainContainer.set_width(lv.pct(100))
ui_MainContainer.set_height(lv.pct(100))
ui_MainContainer.set_align(lv.ALIGN.CENTER)
SetFlag(ui_MainContainer, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_MainContainer, lv.obj.FLAG.SCROLLABLE, False)

ui_Interface = lv.obj(ui_MainContainer)
ui_Interface.remove_style_all()
ui_Interface.set_width(lv.pct(100))
ui_Interface.set_height(lv.pct(100))
ui_Interface.set_align(lv.ALIGN.CENTER)
SetFlag(ui_Interface, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_Interface, lv.obj.FLAG.SCROLLABLE, False)

ui_InfoHeader = lv.obj(ui_Interface)
ui_InfoHeader.remove_style_all()
ui_InfoHeader.set_width(lv.pct(100))
ui_InfoHeader.set_height(lv.pct(5))
ui_InfoHeader.set_align(lv.ALIGN.TOP_MID)
ui_InfoHeader.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_InfoHeader.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
SetFlag(ui_InfoHeader, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_InfoHeader, lv.obj.FLAG.SCROLLABLE, False)
ui_InfoHeader.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_InfoHeader.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_InfoHeader.set_style_pad_left(4, lv.PART.SCROLLBAR | lv.STATE.DEFAULT)
ui_InfoHeader.set_style_pad_right(4, lv.PART.SCROLLBAR | lv.STATE.DEFAULT)
ui_InfoHeader.set_style_pad_top(2, lv.PART.SCROLLBAR | lv.STATE.DEFAULT)
ui_InfoHeader.set_style_pad_bottom(2, lv.PART.SCROLLBAR | lv.STATE.DEFAULT)

ui_LeftSection = lv.obj(ui_InfoHeader)
ui_LeftSection.remove_style_all()
ui_LeftSection.set_height(lv.pct(100))
ui_LeftSection.set_flex_grow(1)
ui_LeftSection.set_align(lv.ALIGN.CENTER)
ui_LeftSection.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_LeftSection.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER)
SetFlag(ui_LeftSection, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_LeftSection, lv.obj.FLAG.SCROLLABLE, False)

ui_WifiStatus = lv.label(ui_LeftSection)
ui_WifiStatus.set_text(f"Wifi: Loading...")
ui_WifiStatus.set_width(lv.SIZE_CONTENT)  # 1
ui_WifiStatus.set_height(lv.SIZE_CONTENT)  # 1
ui_WifiStatus.set_align(lv.ALIGN.CENTER)
ui_WifiStatus.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_WifiStatus.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_MiddleSection = lv.obj(ui_InfoHeader)
ui_MiddleSection.remove_style_all()
ui_MiddleSection.set_height(lv.pct(100))
ui_MiddleSection.set_flex_grow(1)
ui_MiddleSection.set_align(lv.ALIGN.CENTER)
ui_MiddleSection.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_MiddleSection.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
SetFlag(ui_MiddleSection, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_MiddleSection, lv.obj.FLAG.SCROLLABLE, False)

ui_Time = lv.label(ui_MiddleSection)
ui_Time.set_text("??:??:??")
ui_Time.set_width(lv.SIZE_CONTENT)  # 1
ui_Time.set_height(lv.SIZE_CONTENT)  # 1
ui_Time.set_align(lv.ALIGN.CENTER)

ui_RightSection = lv.obj(ui_InfoHeader)
ui_RightSection.remove_style_all()
ui_RightSection.set_height(lv.pct(100))
ui_RightSection.set_flex_grow(1)
ui_RightSection.set_align(lv.ALIGN.CENTER)
ui_RightSection.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_RightSection.set_flex_align(lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
SetFlag(ui_RightSection, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_RightSection, lv.obj.FLAG.SCROLLABLE, False)

ui_Battery = lv.label(ui_RightSection)
ui_Battery.set_text("??% Charge")
ui_Battery.set_width(lv.SIZE_CONTENT)  # 1
ui_Battery.set_height(lv.SIZE_CONTENT)  # 1
ui_Battery.set_align(lv.ALIGN.CENTER)
ui_Battery.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_Battery.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_AppInterface = lv.obj(ui_Interface)
ui_AppInterface.remove_style_all()
ui_AppInterface.set_width(lv.pct(100))
ui_AppInterface.set_height(lv.pct(95))
ui_AppInterface.set_align(lv.ALIGN.BOTTOM_MID)
ui_AppInterface.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_AppInterface.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
SetFlag(ui_AppInterface, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_AppInterface, lv.obj.FLAG.SCROLLABLE, True)
ui_AppInterface.set_style_pad_left(30, lv.PART.MAIN | lv.STATE.DEFAULT)
ui_AppInterface.set_style_pad_right(30, lv.PART.MAIN | lv.STATE.DEFAULT)
ui_AppInterface.set_style_pad_top(30, lv.PART.MAIN | lv.STATE.DEFAULT)
ui_AppInterface.set_style_pad_bottom(30, lv.PART.MAIN | lv.STATE.DEFAULT)
ui_AppInterface.set_style_pad_row(30, lv.PART.MAIN | lv.STATE.DEFAULT)
ui_AppInterface.set_style_pad_column(30, lv.PART.MAIN | lv.STATE.DEFAULT)

# ui_App = ui_App_create(ui_AppInterface)
# ui_App.set_x(-200)
# ui_App.set_y(-30)

ui_ApplicationScreen = lv.obj(ui_Interface)
ui_ApplicationScreen.remove_style_all()
ui_ApplicationScreen.set_width(lv.pct(100))
ui_ApplicationScreen.set_height(lv.pct(95))
ui_ApplicationScreen.set_align(lv.ALIGN.BOTTOM_MID)
SetFlag(ui_ApplicationScreen, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_ApplicationScreen, lv.obj.FLAG.SCROLLABLE, False)

ui_OverInterface = lv.obj(ui_MainContainer)
ui_OverInterface.remove_style_all()
ui_OverInterface.set_width(lv.pct(100))
ui_OverInterface.set_height(lv.pct(100))
ui_OverInterface.set_align(lv.ALIGN.CENTER)
SetFlag(ui_OverInterface, lv.obj.FLAG.HIDDEN, True)
SetFlag(ui_OverInterface, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_OverInterface, lv.obj.FLAG.SCROLLABLE, False)

ui_ModalContainer = lv.obj(ui_OverInterface)
ui_ModalContainer.remove_style_all()
ui_ModalContainer.set_width(lv.pct(100))
ui_ModalContainer.set_height(lv.pct(100))
ui_ModalContainer.set_align(lv.ALIGN.CENTER)
SetFlag(ui_ModalContainer, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_ModalContainer, lv.obj.FLAG.SCROLLABLE, False)
ui_ModalContainer.set_style_bg_color(lv.color_hex(0x101010), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_ModalContainer.set_style_bg_opa(100, lv.PART.MAIN | lv.STATE.DEFAULT)

# ui_OptionsModal = ui_OptionsModal_create(ui_ModalContainer)
# ui_OptionsModal.set_x(0)
# ui_OptionsModal.set_y(0)

# ui_comp_get_child(ui_OptionsModal, "Options_Opt1").add_event_cb(OptionsModal_Options_Opt1_eventhandler,
#                                                                 lv.EVENT.ALL, None)
#
# ui_comp_get_child(ui_OptionsModal, "Options_Opt2").add_event_cb(OptionsModal_Options_Opt2_eventhandler,
#                                                                 lv.EVENT.ALL, None)
ui_KeyboardContainer = lv.obj(ui_OverInterface)
ui_KeyboardContainer.remove_style_all()
ui_KeyboardContainer.set_width(lv.pct(100))
ui_KeyboardContainer.set_height(lv.pct(100))
ui_KeyboardContainer.set_align(lv.ALIGN.CENTER)
ui_KeyboardContainer.set_flex_flow(lv.FLEX_FLOW.COLUMN)
ui_KeyboardContainer.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
SetFlag(ui_KeyboardContainer, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_KeyboardContainer, lv.obj.FLAG.SCROLLABLE, False)
ui_KeyboardContainer.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_KeyboardContainer.set_style_bg_opa(100, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_PeerView = lv.obj(ui_KeyboardContainer)
ui_PeerView.remove_style_all()
ui_PeerView.set_width(lv.pct(100))
ui_PeerView.set_height(lv.pct(10))
ui_PeerView.set_align(lv.ALIGN.CENTER)
SetFlag(ui_PeerView, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_PeerView, lv.obj.FLAG.SCROLLABLE, False)

ui_KeyboardContent = lv.textarea(ui_KeyboardContainer)
ui_KeyboardContent.set_width(lv.pct(100))
ui_KeyboardContent.set_height(lv.pct(30))
ui_KeyboardContent.set_placeholder_text("Placeholder...")
ui_KeyboardContent.set_x(-321)
ui_KeyboardContent.set_y(-183)
ui_KeyboardContent.set_align(lv.ALIGN.CENTER)
set_keyboard_content(ui_KeyboardContent.get_label())

ui_MainKeyboard = lv.keyboard(ui_KeyboardContainer)
ui_MainKeyboard.add_event_cb(MainKeyboard_eventhandler, lv.EVENT.ALL, None)
ui_MainKeyboard.set_width(lv.pct(100))
ui_MainKeyboard.set_height(lv.pct(60))
ui_MainKeyboard.set_align(lv.ALIGN.BOTTOM_MID)

# if 'ui_KeyboardContent' in globals():
ui_TopGuide = lv.obj(ui_MainContainer)
ui_TopGuide.remove_style_all()
ui_TopGuide.set_width(80)
ui_TopGuide.set_height(50)
ui_TopGuide.set_align(lv.ALIGN.TOP_MID)
ui_TopGuide.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_TopGuide.set_flex_align(lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START)
SetFlag(ui_TopGuide, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_TopGuide, lv.obj.FLAG.SCROLLABLE, False)

ui_HomeButton = lv.button(ui_TopGuide)
ui_HomeButton.set_height(45)
ui_HomeButton.set_width(lv.pct(100))
ui_HomeButton.set_align(lv.ALIGN.CENTER)
SetFlag(ui_HomeButton, lv.obj.FLAG.SCROLLABLE, False)
SetFlag(ui_HomeButton, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
ui_HomeButton.set_style_radius(50, lv.PART.MAIN | lv.STATE.DEFAULT)
ui_HomeButton.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_HomeButton.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_HomeButtonText = lv.label(ui_HomeButton)
ui_HomeButtonText.set_text("Home")
ui_HomeButtonText.set_width(lv.SIZE_CONTENT)  # 1
ui_HomeButtonText.set_height(lv.SIZE_CONTENT)  # 1
ui_HomeButtonText.set_align(lv.ALIGN.CENTER)
ui_HomeButtonText.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_HomeButtonText.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_HomeButton.add_event_cb(HomeButton_eventhandler, lv.EVENT.ALL, None)
ui_NotificationsContainer = lv.obj(ui_MainContainer)
ui_NotificationsContainer.remove_style_all()
ui_NotificationsContainer.set_height(80)
ui_NotificationsContainer.set_width(lv.pct(40))
ui_NotificationsContainer.set_align(lv.ALIGN.TOP_RIGHT)
ui_NotificationsContainer.set_flex_flow(lv.FLEX_FLOW.COLUMN)
ui_NotificationsContainer.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.END)
SetFlag(ui_NotificationsContainer, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_NotificationsContainer, lv.obj.FLAG.SCROLLABLE, False)
SetFlag(ui_NotificationsContainer, lv.obj.FLAG.HIDDEN, True)
ui_NotificationsContainer.set_style_pad_left(5, lv.PART.MAIN | lv.STATE.DEFAULT)
ui_NotificationsContainer.set_style_pad_right(5, lv.PART.MAIN | lv.STATE.DEFAULT)
ui_NotificationsContainer.set_style_pad_top(5, lv.PART.MAIN | lv.STATE.DEFAULT)
ui_NotificationsContainer.set_style_pad_bottom(5, lv.PART.MAIN | lv.STATE.DEFAULT)

# ui_Notification = ui_Notification_create(ui_NotificationsContainer)
# ui_Notification.set_x(0)
# ui_Notification.set_y(0)

ui_MainKeyboard.set_textarea(ui_KeyboardContent)

lvgl_app_objects: list[LVGLToObjectBindings] = []

lvgl_object_bindings: list[LVGLToObjectBindings] = []


class BeijingTime:
    def __init__(self):
        self.sync_time()
        self.update_time()

    def sync_time(self):
        pass
        # try:
        #     ntptime.settime()
        #     print("Time synchronized with NTP server")
        # except:
        #     print("Failed to sync time with NTP server")

    def update_time(self):
        current_time = utime.localtime()
        # Beijing time is UTC+8
        hour = (current_time[3] + 8) % 24
        self.current_time_str = "{:02d}:{:02d}".format(hour, current_time[4])

    async def tick(self):
        while True:
            self.update_time()
            ui_Time.set_text(self.current_time_str)
            lv.task_handler()
            await asyncio.sleep(1)


async def data_to_lvgl_every_second():
    """
    This function updates the data to accord the changes to the Main Screen UI asynchronously every second.
    """
    while True:
        # ui_Time.set_text(get_local_current_time())
        if con.is_wifi_connected():
            ui_WifiStatus.set_text("Wifi: Connected")
        else:
            ui_WifiStatus.set_text("Wifi: Disconnected")
        await asyncio.sleep(1)


async def queue_push_notif_every_second():
    """
    This Async function runs as a background process in the UI-Update level.
    """
    while True:
        if len(QUEUED_NOTIFICATIONS) > 0:
            SetFlag(ui_NotificationsContainer, lv.obj.HIDDEN, False)
            create_notification(QUEUED_NOTIFICATIONS[0])
            temp_sec: float = QUEUED_NOTIFICATIONS[0].duration
            temp_hash: str = pdaos_lib.notif_identifier_hash(QUEUED_NOTIFICATIONS[0])
            while temp_sec > 0 or temp_hash != pdaos_lib.notif_identifier_hash(QUEUED_NOTIFICATIONS[0]):
                temp_sec -= 0.1
                await asyncio.sleep(0.1) # Detect whether the callback was invoked before the duration was up
        else:
            SetFlag(ui_NotificationsContainer, lv.obj.HIDDEN, True)
            await asyncio.sleep(1)


def refresh_lvgl_app_objects(apps: list[Application]):
    global lvgl_app_objects
    for obj in lvgl_app_objects:
        obj.get().delete()
        del obj

    lvgl_app_objects.clear()
    gc.collect()

    for app in apps:
        ui_App = ui_App_create(ui_AppInterface, app.get_name(), app.get_icon(), app.get_color())
        ui_App.set_x(0)
        ui_App.set_y(0)
        lvgl_app_objects.append(LVGLToObjectBindings(ui_App, app.get_name()))


def add_lvgl_object_binding(obj: any, identifier: str):
    global lvgl_object_bindings
    lvgl_object_bindings.append(LVGLToObjectBindings(obj, identifier))


def get_lvgl_object_binding(identifier: str) -> LVGLToObjectBindings | None:
    for l in lvgl_object_bindings:
        l: LVGLToObjectBindings
        if l.identifier == identifier:
            return l
    return None


def remove_lvgl_object_binding(identifier: str, delete_lvgl_object: bool = True, do_gc: bool = False):
    ind: int = 0
    for l in lvgl_object_bindings:
        l: LVGLToObjectBindings
        if l.identifier == identifier:
            if delete_lvgl_object:
                l.get().delete()
                del l
                if do_gc:
                    gc.collect()

            lvgl_object_bindings.pop(ind)
            return
        ind += 1


def get_app_interface_container():
    return ui_AppInterface


def update_main_screen():
    import globals as g
    SetFlag(ui_AppInterface, lv.obj.FLAG.HIDDEN, g.FOCUSED_APP is None)


def create_notification(notif: Notification):
    lv_obj = ui_Notification_create(ui_NotificationsContainer, notif)
    add_lvgl_object_binding(lv_obj, pdaos_lib.notif_identifier_hash(notif))


async def update():
    """
    This function starts the OS-UI Level async updates.
    """
    # time = BeijingTime()
    task1, task2 = asyncio.create_task(data_to_lvgl_every_second()), asyncio.create_task(queue_push_notif_every_second())
    await asyncio.gather(task1, task2) # runs these tasks in parallel, asynchronously
