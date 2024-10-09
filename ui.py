# This file was generated by SquareLine Studio
# SquareLine Studio version: SquareLine Studio 1.4.2
# LVGL version: 9.1.0
# Project name: SquareLine_Project

import lvgl as lv
import ui_images

dispp = lv.display_get_default()
theme = lv.theme_default_init(dispp, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.RED), False, lv.font_default())
dispp.set_theme(theme)

def ui_theme_set(idx):
   return

def SetFlag( obj, flag, value):
    if (value):
        obj.add_flag(flag)
    else:
        obj.remove_flag(flag)
    return

_ui_comp_table = {}
_ui_comp_prev = None
_ui_name_prev = None
_ui_child_prev = None
_ui_comp_table.clear()

def _ui_comp_del_event(e):
    target = e.get_target()
    _ui_comp_table[id(target)].remove()

def ui_comp_get_child(comp, child_name):
    return _ui_comp_table[id(comp)][child_name]

def ui_comp_get_root_from_child(child, compname):
    for component in _ui_comp_table:
        if _ui_comp_table[component]["_CompName"]==compname:
            for part in _ui_comp_table[component]:
                if id(_ui_comp_table[component][part]) == id(child):
                    return _ui_comp_table[component]
    return None
def SetBarProperty(target, id, val):
   if id == 'Value_with_anim': target.set_value(val, lv.ANIM.ON)
   if id == 'Value': target.set_value(val, lv.ANIM.OFF)
   return

def SetPanelProperty(target, id, val):
   if id == 'Position_X': target.set_x(val)
   if id == 'Position_Y': target.set_y(val)
   if id == 'Width': target.set_width(val)
   if id == 'Height': target.set_height(val)
   return

def SetDropdownProperty(target, id, val):
   if id == 'Selected':
      target.set_selected(val)
   return

def SetImageProperty(target, id, val, val2):
   if id == 'Image': target.set_src(val)
   if id == 'Angle': target.set_rotation(val2)
   if id == 'Zoom': target.set_scale(val2)
   return

def SetLabelProperty(target, id, val):
   if id == 'Text': target.set_text(val)
   return

def SetRollerProperty(target, id, val):
   if id == 'Selected':
      target.set_selected(val, lv.ANIM.OFF)
   if id == 'Selected_with_anim':
      target.set_selected(val, lv.ANIM.ON)
   return

def SetSliderProperty(target, id, val):
   if id == 'Value_with_anim': target.set_value(val, lv.ANIM.ON)
   if id == 'Value': target.set_value(val, lv.ANIM.OFF)
   return

def ChangeScreen( src, fademode, speed, delay):
    lv.screen_load_anim(src, fademode, speed, delay, False)
    return

def DeleteScreen(src):
    return

def IncrementArc( trg, val):
    trg.set_value(trg.get_value()+val)
    trg.send_event(lv.EVENT.VALUE_CHANGED, None)
    return

def IncrementBar( trg, val, anim):
    trg.set_value(trg.get_value()+val,anim)
    return

def IncrementSlider( trg, val, anim):
    trg.set_value(trg.get_value()+val,anim)
    trg.send_event(lv.EVENT.VALUE_CHANGED, None)
    return

def KeyboardSetTarget( keyboard, textarea):
    keyboard.set_textarea(textarea)
    return

def ModifyFlag( obj, flag, value):
    if (value=="TOGGLE"):
        if ( obj.has_flag(flag) ):
            obj.remove_flag(flag)
        else:
            obj.add_flag(flag)
        return

    if (value=="ADD"):
        obj.add_flag(flag)
    else:
        obj.remove_flag(flag)
    return

def ModifyState( obj, state, value):
    if (value=="TOGGLE"):
        if ( obj.has_state(state) ):
            obj.remove_state(state)
        else:
            obj.add_state(state)
        return

    if (value=="ADD"):
        obj.add_state(state)
    else:
        obj.remove_state(state)
    return

def TextAreaMoveCursor( trg, val):
    if val=="UP" : trg.cursor_up()
    if val=="RIGHT" : trg.cursor_right()
    if val=="DOWN" : trg.cursor_down()
    if val=="LEFT" : trg.cursor_left()
    trg.add_state(lv.STATE.FOCUSED)
    return

def set_opacity(obj, v):
    obj.set_style_opa(v, lv.STATE.DEFAULT|lv.PART.MAIN)
    return

def SetTextValueArc( trg, src, prefix, postfix):
    trg.set_text(prefix+str(src.get_value())+postfix)
    return

def SetTextValueSlider( trg, src, prefix, postfix):
    trg.set_text(prefix+str(src.get_value())+postfix)
    return

def SetTextValueChecked( trg, src, txton, txtoff):
    if src.has_state(lv.STATE.CHECKED):
        trg.set_text(txton)
    else:
        trg.set_text(txtoff)
    return

def StepSpinbox( trg, val):
    if val==1 : trg.increment()
    if val==-1 : trg.decrement()
    trg.send_event(lv.EVENT.VALUE_CHANGED, None)
    return

def SwitchTheme(val):
    ui_theme_set(val)
    return

# COMPONENTS

 # COMPONENT OptionsModal
def ui_OptionsModal_create(comp_parent):
    cui_OptionsModal = lv.obj(comp_parent)
    cui_OptionsModal.set_width(lv.pct(60))
    cui_OptionsModal.set_height(lv.SIZE_CONTENT)   # 50
    cui_OptionsModal.set_align( lv.ALIGN.CENTER)
    cui_OptionsModal.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    cui_OptionsModal.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
    SetFlag(cui_OptionsModal, lv.obj.FLAG.SCROLLABLE, False)
    cui_ModalTitle = lv.label(cui_OptionsModal)
    cui_ModalTitle.set_text("ModalTitle")
    cui_ModalTitle.set_width(lv.pct(100))
    cui_ModalTitle.set_height(lv.SIZE_CONTENT)   # 1
    cui_ModalTitle.set_style_text_color(lv.color_hex(0x4C4C4C), lv.PART.MAIN | lv.STATE.DEFAULT )
    cui_ModalTitle.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
    cui_ModalTitle.set_style_text_letter_space( 1, lv.PART.MAIN | lv.STATE.DEFAULT )
    cui_ModalTitle.set_style_text_line_space( 0, lv.PART.MAIN | lv.STATE.DEFAULT )
    cui_ModalTitle.set_style_text_font( lv.font_montserrat_18, lv.PART.MAIN | lv.STATE.DEFAULT )
    cui_ModalContent = lv.label(cui_OptionsModal)
    cui_ModalContent.set_text("text")
    cui_ModalContent.set_width(lv.pct(100))
    cui_ModalContent.set_height(lv.SIZE_CONTENT)   # 1
    cui_ModalContent.set_align( lv.ALIGN.CENTER)
    cui_Options = lv.obj(cui_OptionsModal)
    cui_Options.remove_style_all()
    cui_Options.set_height(40)
    cui_Options.set_width(lv.pct(100))
    cui_Options.set_align( lv.ALIGN.CENTER)
    cui_Options.set_flex_flow(lv.FLEX_FLOW.ROW)
    cui_Options.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
    SetFlag(cui_Options, lv.obj.FLAG.CLICKABLE, False)
    SetFlag(cui_Options, lv.obj.FLAG.SCROLLABLE, False)
    cui_Opt1 = lv.button(cui_Options)
    cui_Opt1.set_height(50)
    cui_Opt1.set_flex_grow(1)
    cui_Opt1.set_align( lv.ALIGN.CENTER)
    SetFlag(cui_Opt1, lv.obj.FLAG.SCROLLABLE, False)
    SetFlag(cui_Opt1, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
    cui_Opt1Text = lv.label(cui_Opt1)
    cui_Opt1Text.set_text("Option1")
    cui_Opt1Text.set_width(lv.SIZE_CONTENT)	# 1
    cui_Opt1Text.set_height(lv.SIZE_CONTENT)   # 1
    cui_Opt1Text.set_align( lv.ALIGN.CENTER)
    cui_Container9 = lv.obj(cui_Options)
    cui_Container9.remove_style_all()
    cui_Container9.set_width(10)
    cui_Container9.set_height(lv.pct(100))
    cui_Container9.set_align( lv.ALIGN.CENTER)
    SetFlag(cui_Container9, lv.obj.FLAG.CLICKABLE, False)
    SetFlag(cui_Container9, lv.obj.FLAG.SCROLLABLE, False)
    cui_Opt2 = lv.button(cui_Options)
    cui_Opt2.set_height(50)
    cui_Opt2.set_flex_grow(1)
    cui_Opt2.set_align( lv.ALIGN.CENTER)
    SetFlag(cui_Opt2, lv.obj.FLAG.SCROLLABLE, False)
    SetFlag(cui_Opt2, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
    cui_Option2Text = lv.label(cui_Opt2)
    cui_Option2Text.set_text("Option2")
    cui_Option2Text.set_width(lv.SIZE_CONTENT)	# 1
    cui_Option2Text.set_height(lv.SIZE_CONTENT)   # 1
    cui_Option2Text.set_align( lv.ALIGN.CENTER)
    _ui_comp_table[id(cui_OptionsModal)]= {"OptionsModal" : cui_OptionsModal,"ModalTitle" : cui_ModalTitle,"ModalContent" : cui_ModalContent,"Options" : cui_Options,"Options_Opt1" : cui_Opt1,"Options_Opt1_Opt1Text" : cui_Opt1Text,"Options_Container9" : cui_Container9,"Options_Opt2" : cui_Opt2,"Options_Opt2_Option2Text" : cui_Option2Text, "_CompName" : "OptionsModal"}
    return cui_OptionsModal

 # COMPONENT App

def comp_App_AppButton_eventhandler(event_struct):
   target = event_struct.get_target()
   comp_App = ui_comp_get_root_from_child(target, "App")
   event = event_struct.code
   if event == lv.EVENT.CLICKED and True:
      ( event_struct )
   return

def ui_App_create(comp_parent):
    cui_App = lv.obj(comp_parent)
    cui_App.remove_style_all()
    cui_App.set_width(80)
    cui_App.set_height(80)
    cui_App.set_x(-200)
    cui_App.set_y(-30)
    cui_App.set_align( lv.ALIGN.CENTER)
    SetFlag(cui_App, lv.obj.FLAG.CLICKABLE, False)
    SetFlag(cui_App, lv.obj.FLAG.SCROLLABLE, False)
    cui_AppButton = lv.button(cui_App)
    cui_AppButton.set_width(60)
    cui_AppButton.set_height(60)
    cui_AppButton.set_align( lv.ALIGN.TOP_MID)
    SetFlag(cui_AppButton, lv.obj.FLAG.SCROLLABLE, False)
    SetFlag(cui_AppButton, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
    cui_AppIcon = lv.label(cui_AppButton)
    cui_AppIcon.set_text("BYD")
    cui_AppIcon.set_width(lv.SIZE_CONTENT)	# 1
    cui_AppIcon.set_height(lv.SIZE_CONTENT)   # 1
    cui_AppIcon.set_align( lv.ALIGN.CENTER)
    cui_AppButton.add_event_cb(comp_App_AppButton_eventhandler, lv.EVENT.ALL, None)
    cui_AppTitle = lv.label(cui_App)
    cui_AppTitle.set_text("AppTitle")
    cui_AppTitle.set_width(lv.SIZE_CONTENT)	# 1
    cui_AppTitle.set_height(lv.SIZE_CONTENT)   # 1
    cui_AppTitle.set_align( lv.ALIGN.BOTTOM_MID)
    _ui_comp_table[id(cui_App)]= {"App" : cui_App,"AppButton" : cui_AppButton,"AppButton_AppIcon" : cui_AppIcon,"AppTitle" : cui_AppTitle, "_CompName" : "App"}
    return cui_App

ui____initial_actions0 = lv.obj()

def OptionsModal_Options_Opt1_eventhandler(event_struct):
   target = event_struct.get_target()
   event = event_struct.code
   if event == lv.EVENT.CLICKED and True:
      ( event_struct )
   return

def OptionsModal_Options_Opt2_eventhandler(event_struct):
   target = event_struct.get_target()
   event = event_struct.code
   if event == lv.EVENT.CLICKED and True:
      ( event_struct )
   return

ui_Screen1 = lv.obj()
SetFlag(ui_Screen1, lv.obj.FLAG.SCROLLABLE, False)

ui_MainContainer = lv.obj(ui_Screen1)
ui_MainContainer.remove_style_all()
ui_MainContainer.set_width(lv.pct(100))
ui_MainContainer.set_height(lv.pct(100))
ui_MainContainer.set_align( lv.ALIGN.CENTER)
SetFlag(ui_MainContainer, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_MainContainer, lv.obj.FLAG.SCROLLABLE, False)

ui_Interface = lv.obj(ui_MainContainer)
ui_Interface.remove_style_all()
ui_Interface.set_width(lv.pct(100))
ui_Interface.set_height(lv.pct(100))
ui_Interface.set_align( lv.ALIGN.CENTER)
ui_Interface.set_flex_flow(lv.FLEX_FLOW.COLUMN)
ui_Interface.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
SetFlag(ui_Interface, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_Interface, lv.obj.FLAG.SCROLLABLE, False)

ui_InfoHeader = lv.obj(ui_Interface)
ui_InfoHeader.remove_style_all()
ui_InfoHeader.set_height(20)
ui_InfoHeader.set_width(lv.pct(100))
ui_InfoHeader.set_align( lv.ALIGN.TOP_MID)
ui_InfoHeader.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_InfoHeader.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
SetFlag(ui_InfoHeader, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_InfoHeader, lv.obj.FLAG.SCROLLABLE, False)
ui_InfoHeader.set_style_bg_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT )
ui_InfoHeader.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )

ui_InfoHeader.set_style_pad_left( 4, lv.PART.SCROLLBAR | lv.STATE.DEFAULT )
ui_InfoHeader.set_style_pad_right( 4, lv.PART.SCROLLBAR | lv.STATE.DEFAULT )
ui_InfoHeader.set_style_pad_top( 2, lv.PART.SCROLLBAR | lv.STATE.DEFAULT )
ui_InfoHeader.set_style_pad_bottom( 2, lv.PART.SCROLLBAR | lv.STATE.DEFAULT )

ui_LeftSection = lv.obj(ui_InfoHeader)
ui_LeftSection.remove_style_all()
ui_LeftSection.set_height(lv.pct(100))
ui_LeftSection.set_flex_grow(1)
ui_LeftSection.set_align( lv.ALIGN.CENTER)
ui_LeftSection.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_LeftSection.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER)
SetFlag(ui_LeftSection, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_LeftSection, lv.obj.FLAG.SCROLLABLE, False)

ui_WifiStatus = lv.label(ui_LeftSection)
ui_WifiStatus.set_text("Wifi: Not Connected")
ui_WifiStatus.set_width(lv.SIZE_CONTENT)	# 1
ui_WifiStatus.set_height(lv.SIZE_CONTENT)   # 1
ui_WifiStatus.set_align( lv.ALIGN.CENTER)

ui_MiddleSection = lv.obj(ui_InfoHeader)
ui_MiddleSection.remove_style_all()
ui_MiddleSection.set_height(lv.pct(100))
ui_MiddleSection.set_flex_grow(1)
ui_MiddleSection.set_align( lv.ALIGN.CENTER)
ui_MiddleSection.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_MiddleSection.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
SetFlag(ui_MiddleSection, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_MiddleSection, lv.obj.FLAG.SCROLLABLE, False)

ui_Time = lv.label(ui_MiddleSection)
ui_Time.set_text("10:00")
ui_Time.set_width(lv.SIZE_CONTENT)	# 1
ui_Time.set_height(lv.SIZE_CONTENT)   # 1
ui_Time.set_align( lv.ALIGN.CENTER)

ui_RightSection = lv.obj(ui_InfoHeader)
ui_RightSection.remove_style_all()
ui_RightSection.set_height(lv.pct(100))
ui_RightSection.set_flex_grow(1)
ui_RightSection.set_align( lv.ALIGN.CENTER)
ui_RightSection.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_RightSection.set_flex_align(lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
SetFlag(ui_RightSection, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_RightSection, lv.obj.FLAG.SCROLLABLE, False)

ui_Battery = lv.label(ui_RightSection)
ui_Battery.set_text("90% Charge")
ui_Battery.set_width(lv.SIZE_CONTENT)	# 1
ui_Battery.set_height(lv.SIZE_CONTENT)   # 1
ui_Battery.set_align( lv.ALIGN.CENTER)

ui_AppInterface = lv.obj(ui_Interface)
ui_AppInterface.remove_style_all()
ui_AppInterface.set_width(lv.pct(100))
ui_AppInterface.set_height(lv.pct(95))
ui_AppInterface.set_align( lv.ALIGN.CENTER)
ui_AppInterface.set_flex_flow(lv.FLEX_FLOW.ROW)
ui_AppInterface.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
SetFlag(ui_AppInterface, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_AppInterface, lv.obj.FLAG.SCROLLABLE, False)
ui_AppInterface.set_style_pad_left( 30, lv.PART.MAIN | lv.STATE.DEFAULT )
ui_AppInterface.set_style_pad_right( 30, lv.PART.MAIN | lv.STATE.DEFAULT )
ui_AppInterface.set_style_pad_top( 30, lv.PART.MAIN | lv.STATE.DEFAULT )
ui_AppInterface.set_style_pad_bottom( 30, lv.PART.MAIN | lv.STATE.DEFAULT )
ui_AppInterface.set_style_pad_row( 10, lv.PART.MAIN | lv.STATE.DEFAULT )
ui_AppInterface.set_style_pad_column( 10, lv.PART.MAIN | lv.STATE.DEFAULT )

ui_App = ui_App_create(ui_AppInterface)
ui_App.set_x(-200)
ui_App.set_y(-30)

ui_OverInterface = lv.obj(ui_MainContainer)
ui_OverInterface.remove_style_all()
ui_OverInterface.set_width(lv.pct(100))
ui_OverInterface.set_height(lv.pct(100))
ui_OverInterface.set_align( lv.ALIGN.CENTER)
SetFlag(ui_OverInterface, lv.obj.FLAG.HIDDEN, True)
SetFlag(ui_OverInterface, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_OverInterface, lv.obj.FLAG.SCROLLABLE, False)

ui_ModalContainer = lv.obj(ui_OverInterface)
ui_ModalContainer.remove_style_all()
ui_ModalContainer.set_width(lv.pct(100))
ui_ModalContainer.set_height(lv.pct(100))
ui_ModalContainer.set_align( lv.ALIGN.CENTER)
SetFlag(ui_ModalContainer, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_ModalContainer, lv.obj.FLAG.SCROLLABLE, False)
ui_ModalContainer.set_style_bg_color(lv.color_hex(0x101010), lv.PART.MAIN | lv.STATE.DEFAULT )
ui_ModalContainer.set_style_bg_opa(100, lv.PART.MAIN| lv.STATE.DEFAULT )

ui_OptionsModal = ui_OptionsModal_create(ui_ModalContainer)
ui_OptionsModal.set_x(0)
ui_OptionsModal.set_y(0)

ui_comp_get_child(ui_OptionsModal, "Options_Opt1").add_event_cb(OptionsModal_Options_Opt1_eventhandler, lv.EVENT.ALL, None)

ui_comp_get_child(ui_OptionsModal, "Options_Opt2").add_event_cb(OptionsModal_Options_Opt2_eventhandler, lv.EVENT.ALL, None)
ui_KeyboardContainer = lv.obj(ui_OverInterface)
ui_KeyboardContainer.remove_style_all()
ui_KeyboardContainer.set_width(lv.pct(100))
ui_KeyboardContainer.set_height(lv.pct(100))
ui_KeyboardContainer.set_align( lv.ALIGN.CENTER)
ui_KeyboardContainer.set_flex_flow(lv.FLEX_FLOW.COLUMN)
ui_KeyboardContainer.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
SetFlag(ui_KeyboardContainer, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_KeyboardContainer, lv.obj.FLAG.SCROLLABLE, False)
ui_KeyboardContainer.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT )
ui_KeyboardContainer.set_style_bg_opa(100, lv.PART.MAIN| lv.STATE.DEFAULT )

ui_PeerView = lv.obj(ui_KeyboardContainer)
ui_PeerView.remove_style_all()
ui_PeerView.set_width(lv.pct(100))
ui_PeerView.set_height(lv.pct(10))
ui_PeerView.set_align( lv.ALIGN.CENTER)
SetFlag(ui_PeerView, lv.obj.FLAG.CLICKABLE, False)
SetFlag(ui_PeerView, lv.obj.FLAG.SCROLLABLE, False)

ui_KeyboardContent = lv.textarea(ui_KeyboardContainer)
ui_KeyboardContent.set_width(lv.pct(100))
ui_KeyboardContent.set_height(lv.pct(30))
ui_KeyboardContent.set_placeholder_text("Placeholder...")
ui_KeyboardContent.set_x(-321)
ui_KeyboardContent.set_y(-183)
ui_KeyboardContent.set_align( lv.ALIGN.CENTER)

ui_MainKeyboard = lv.keyboard(ui_KeyboardContainer)
ui_MainKeyboard.set_width(lv.pct(100))
ui_MainKeyboard.set_height(lv.pct(60))
ui_MainKeyboard.set_align( lv.ALIGN.BOTTOM_MID)

#if 'ui_KeyboardContent' in globals():

ui_MainKeyboard.set_textarea(ui_KeyboardContent)

lv.screen_load(ui_Screen1)
