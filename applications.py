import asyncio

import micropython

import globals
from pdaos_lib import Application, AsyncJob, Config, ConfigCategory, ConfigSetting, ConfigTypes
from osui import SetFlag
import lvgl as lv
import random

class DiceApplication(Application):
    def __init__(self):
        super().__init__("Dices", "DC", "dices", 0xE4080A)

    @staticmethod
    def parseDiceRoll(unparsed: str, print_output: bool = False):
        # Example: "d20" will be parsed into a d20 roll
        # Example 2: "3d20" will be parsed into rolling 3 times d20
        # Example 3: "3d20 + 10" will be parsed into rolling 3 times d20 then plus 10 of the total of the rolls
        text_output: str = ""
        segments = unparsed.split("d")
        rolls = []
        total = 0
        if len(segments) == 2:
            trailings = segments[1].split("+")
            if len(trailings) == 2:
                num_rolls, dice_type, modifier = int(segments[0] or 1), int(trailings[0]), int(trailings[1])
                for i in range(num_rolls):
                    roll = random.randint(1, dice_type)
                    rolls.append(roll)
                    total += roll
                total += modifier
            else:
                num_rolls, dice_type = int(segments[0] or 1), int(segments[1])
                for i in range(num_rolls):
                    roll = random.randint(1, dice_type)
                    rolls.append(roll)
                    total += roll
            if print_output: print(f"Rolls: {rolls}, Total: {total}")
            text_output = f"Rolls: {rolls}, Total: {total}"
        elif len(segments) == 1:
            if print_output: print(random.randint(1, int(segments[1])))
            text_output = f"{random.randint(1, int(segments[1]))}"
        return rolls, text_output

    def run(self, container: any):
        from pdaos import KeyboardManager, OSBindingsManager

        def d2Type_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                set_result(quick_roll(2))
            return

        def d4Type_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                set_result(quick_roll(4))
            return

        def d6Type_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                set_result(quick_roll(6))
            return

        def d8Type_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                set_result(quick_roll(8))
            return

        def d10Type_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                set_result(quick_roll(10))
            return

        def d12Type_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                set_result(quick_roll(12))
            return

        def d20Type_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                set_result(quick_roll(20))
            return

        def d100Type_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                set_result(quick_roll(100))
            return

        def DiceParserInput_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED:
                KeyboardManager.invoke_keyboard(event_struct.get_target_obj().get_text())
                globals.set_temp_variable("ui_DiceParserInput", event_struct.get_target_obj())
                globals.set_temp_variable("diceParserFocused", True)
            elif globals.get_temp_variable("diceParserFocused") and not KeyboardManager.is_keyboard_focused():
                def set_inputfield_text(*arg):
                    globals.get_temp_variable("ui_DiceParserInput").set_text(KeyboardManager.get_keyboard_text())
                    globals.remove_temp_variable("ui_DiceParserInput")

                globals.set_temp_variable("diceParserFocused", False)
                globals.remove_temp_variable("diceParserFocused")
                micropython.schedule(set_inputfield_text, None)
            return

        def DiceCalculateButton_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                rolls, output = DiceApplication.parseDiceRoll(ui_DiceParserInput.get_text(), False)
                set_result(output)
            return

        def set_result(number: str):
            ui_DiceRollResult.set_text(f"Result: {number}")

        def quick_roll(dice_number: int) -> int:
            rolls, text = DiceApplication.parseDiceRoll(f"d{dice_number}")
            return rolls[0]

        ui_DiceAppScreen = lv.obj(container)
        ui_DiceAppScreen.remove_style_all()
        ui_DiceAppScreen.set_width(lv.pct(100))
        ui_DiceAppScreen.set_height(lv.pct(100))
        ui_DiceAppScreen.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_DiceAppScreen, lv.obj.FLAG.CLICKABLE, False)
        SetFlag(ui_DiceAppScreen, lv.obj.FLAG.SCROLLABLE, False)

        ui_QuickDiceRolls = lv.obj(ui_DiceAppScreen)
        ui_QuickDiceRolls.set_height(120)
        ui_QuickDiceRolls.set_width(lv.pct(90))
        ui_QuickDiceRolls.set_x(0)
        ui_QuickDiceRolls.set_y(50)
        ui_QuickDiceRolls.set_align(lv.ALIGN.TOP_MID)
        ui_QuickDiceRolls.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        ui_QuickDiceRolls.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        SetFlag(ui_QuickDiceRolls, lv.obj.FLAG.SCROLLABLE, False)

        ui_QuickDiceRollerTitle = lv.label(ui_QuickDiceRolls)
        ui_QuickDiceRollerTitle.set_text("Quick Dice Roller (Click on the buttons to get results)")
        ui_QuickDiceRollerTitle.set_width(lv.SIZE_CONTENT)  # 1
        ui_QuickDiceRollerTitle.set_height(lv.SIZE_CONTENT)  # 1
        ui_QuickDiceRollerTitle.set_align(lv.ALIGN.CENTER)

        ui_DiceRollsButtons = lv.obj(ui_QuickDiceRolls)
        ui_DiceRollsButtons.remove_style_all()
        ui_DiceRollsButtons.set_height(50)
        ui_DiceRollsButtons.set_width(lv.pct(100))
        ui_DiceRollsButtons.set_align(lv.ALIGN.CENTER)
        ui_DiceRollsButtons.set_flex_flow(lv.FLEX_FLOW.ROW)
        ui_DiceRollsButtons.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        SetFlag(ui_DiceRollsButtons, lv.obj.FLAG.CLICKABLE, False)
        SetFlag(ui_DiceRollsButtons, lv.obj.FLAG.SCROLLABLE, False)
        ui_DiceRollsButtons.set_style_pad_row(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_DiceRollsButtons.set_style_pad_column(10, lv.PART.MAIN | lv.STATE.DEFAULT)

        ui_d2Type = lv.button(ui_DiceRollsButtons)
        ui_d2Type.set_height(lv.pct(100))
        ui_d2Type.set_flex_grow(1)
        ui_d2Type.set_x(-58)
        ui_d2Type.set_y(-135)
        ui_d2Type.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_d2Type, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_d2Type, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

        ui_Label1 = lv.label(ui_d2Type)
        ui_Label1.set_text("d2")
        ui_Label1.set_width(lv.SIZE_CONTENT)  # 1
        ui_Label1.set_height(lv.SIZE_CONTENT)  # 1
        ui_Label1.set_align(lv.ALIGN.CENTER)

        ui_d2Type.add_event_cb(d2Type_eventhandler, lv.EVENT.ALL, None)
        ui_d4Type = lv.button(ui_DiceRollsButtons)
        ui_d4Type.set_height(lv.pct(100))
        ui_d4Type.set_flex_grow(1)
        ui_d4Type.set_x(-58)
        ui_d4Type.set_y(-135)
        ui_d4Type.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_d4Type, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_d4Type, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

        ui_Label2 = lv.label(ui_d4Type)
        ui_Label2.set_text("d4")
        ui_Label2.set_width(lv.SIZE_CONTENT)  # 1
        ui_Label2.set_height(lv.SIZE_CONTENT)  # 1
        ui_Label2.set_align(lv.ALIGN.CENTER)

        ui_d4Type.add_event_cb(d4Type_eventhandler, lv.EVENT.ALL, None)
        ui_d6Type = lv.button(ui_DiceRollsButtons)
        ui_d6Type.set_height(lv.pct(100))
        ui_d6Type.set_flex_grow(1)
        ui_d6Type.set_x(-58)
        ui_d6Type.set_y(-135)
        ui_d6Type.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_d6Type, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_d6Type, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

        ui_Label3 = lv.label(ui_d6Type)
        ui_Label3.set_text("d6")
        ui_Label3.set_width(lv.SIZE_CONTENT)  # 1
        ui_Label3.set_height(lv.SIZE_CONTENT)  # 1
        ui_Label3.set_align(lv.ALIGN.CENTER)

        ui_d6Type.add_event_cb(d6Type_eventhandler, lv.EVENT.ALL, None)
        ui_d8Type = lv.button(ui_DiceRollsButtons)
        ui_d8Type.set_height(lv.pct(100))
        ui_d8Type.set_flex_grow(1)
        ui_d8Type.set_x(-58)
        ui_d8Type.set_y(-135)
        ui_d8Type.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_d8Type, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_d8Type, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

        ui_Label4 = lv.label(ui_d8Type)
        ui_Label4.set_text("d8")
        ui_Label4.set_width(lv.SIZE_CONTENT)  # 1
        ui_Label4.set_height(lv.SIZE_CONTENT)  # 1
        ui_Label4.set_align(lv.ALIGN.CENTER)

        ui_d8Type.add_event_cb(d8Type_eventhandler, lv.EVENT.ALL, None)
        ui_d10Type = lv.button(ui_DiceRollsButtons)
        ui_d10Type.set_height(lv.pct(100))
        ui_d10Type.set_flex_grow(1)
        ui_d10Type.set_x(-58)
        ui_d10Type.set_y(-135)
        ui_d10Type.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_d10Type, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_d10Type, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

        ui_Label5 = lv.label(ui_d10Type)
        ui_Label5.set_text("d10")
        ui_Label5.set_width(lv.SIZE_CONTENT)  # 1
        ui_Label5.set_height(lv.SIZE_CONTENT)  # 1
        ui_Label5.set_align(lv.ALIGN.CENTER)

        ui_d10Type.add_event_cb(d10Type_eventhandler, lv.EVENT.ALL, None)
        ui_d12Type = lv.button(ui_DiceRollsButtons)
        ui_d12Type.set_height(lv.pct(100))
        ui_d12Type.set_flex_grow(1)
        ui_d12Type.set_x(-58)
        ui_d12Type.set_y(-135)
        ui_d12Type.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_d12Type, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_d12Type, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

        ui_Label6 = lv.label(ui_d12Type)
        ui_Label6.set_text("d12")
        ui_Label6.set_width(lv.SIZE_CONTENT)  # 1
        ui_Label6.set_height(lv.SIZE_CONTENT)  # 1
        ui_Label6.set_align(lv.ALIGN.CENTER)

        ui_d12Type.add_event_cb(d12Type_eventhandler, lv.EVENT.ALL, None)
        ui_d20Type = lv.button(ui_DiceRollsButtons)
        ui_d20Type.set_height(lv.pct(100))
        ui_d20Type.set_flex_grow(1)
        ui_d20Type.set_x(-58)
        ui_d20Type.set_y(-135)
        ui_d20Type.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_d20Type, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_d20Type, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

        ui_Label7 = lv.label(ui_d20Type)
        ui_Label7.set_text("d20")
        ui_Label7.set_width(lv.SIZE_CONTENT)  # 1
        ui_Label7.set_height(lv.SIZE_CONTENT)  # 1
        ui_Label7.set_align(lv.ALIGN.CENTER)

        ui_d20Type.add_event_cb(d20Type_eventhandler, lv.EVENT.ALL, None)
        ui_d100Type = lv.button(ui_DiceRollsButtons)
        ui_d100Type.set_height(lv.pct(100))
        ui_d100Type.set_flex_grow(1)
        ui_d100Type.set_x(-58)
        ui_d100Type.set_y(-135)
        ui_d100Type.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_d100Type, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_d100Type, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

        ui_Label8 = lv.label(ui_d100Type)
        ui_Label8.set_text("d100")
        ui_Label8.set_width(lv.SIZE_CONTENT)  # 1
        ui_Label8.set_height(lv.SIZE_CONTENT)  # 1
        ui_Label8.set_align(lv.ALIGN.CENTER)

        ui_d100Type.add_event_cb(d100Type_eventhandler, lv.EVENT.ALL, None)
        ui_DiceRollResult = lv.label(ui_DiceAppScreen)
        ui_DiceRollResult.set_text("Result: <Unset>")
        ui_DiceRollResult.set_width(lv.SIZE_CONTENT)  # 1
        ui_DiceRollResult.set_height(lv.SIZE_CONTENT)  # 1
        ui_DiceRollResult.set_align(lv.ALIGN.CENTER)

        ui_DiceParser = lv.obj(ui_DiceAppScreen)
        ui_DiceParser.set_height(120)
        ui_DiceParser.set_width(lv.pct(90))
        ui_DiceParser.set_x(0)
        ui_DiceParser.set_y(-40)
        ui_DiceParser.set_align(lv.ALIGN.BOTTOM_MID)
        ui_DiceParser.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        ui_DiceParser.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        SetFlag(ui_DiceParser, lv.obj.FLAG.SCROLLABLE, False)

        ui_DiceParserTitle = lv.label(ui_DiceParser)
        ui_DiceParserTitle.set_text("Dice Parser: Enter a string of dice rolls. (e.g. \"d20\" or \"4d20 + 10\")")
        ui_DiceParserTitle.set_width(lv.SIZE_CONTENT)  # 1
        ui_DiceParserTitle.set_height(lv.SIZE_CONTENT)  # 1
        ui_DiceParserTitle.set_align(lv.ALIGN.CENTER)

        ui_DiceParserInputContainer = lv.obj(ui_DiceParser)
        ui_DiceParserInputContainer.remove_style_all()
        ui_DiceParserInputContainer.set_height(50)
        ui_DiceParserInputContainer.set_width(lv.pct(100))
        ui_DiceParserInputContainer.set_align(lv.ALIGN.CENTER)
        ui_DiceParserInputContainer.set_flex_flow(lv.FLEX_FLOW.ROW)
        ui_DiceParserInputContainer.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        SetFlag(ui_DiceParserInputContainer, lv.obj.FLAG.CLICKABLE, False)
        SetFlag(ui_DiceParserInputContainer, lv.obj.FLAG.SCROLLABLE, False)
        ui_DiceParserInputContainer.set_style_pad_row(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_DiceParserInputContainer.set_style_pad_column(15, lv.PART.MAIN | lv.STATE.DEFAULT)

        ui_DiceParserInput = lv.textarea(ui_DiceParserInputContainer)
        ui_DiceParserInput.set_height(lv.pct(100))
        ui_DiceParserInput.set_flex_grow(3)
        ui_DiceParserInput.set_placeholder_text("Placeholder...")
        ui_DiceParserInput.set_align(lv.ALIGN.CENTER)

        ui_DiceParserInput.add_event_cb(DiceParserInput_eventhandler, lv.EVENT.ALL, None)
        ui_DiceCalculateButton = lv.button(ui_DiceParserInputContainer)
        ui_DiceCalculateButton.set_height(lv.pct(100))
        ui_DiceCalculateButton.set_flex_grow(1)
        ui_DiceCalculateButton.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_DiceCalculateButton, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_DiceCalculateButton, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

        ui_DiceCalcLabel = lv.label(ui_DiceCalculateButton)
        ui_DiceCalcLabel.set_text("Calculate")
        ui_DiceCalcLabel.set_width(lv.SIZE_CONTENT)  # 1
        ui_DiceCalcLabel.set_height(lv.SIZE_CONTENT)  # 1
        ui_DiceCalcLabel.set_align(lv.ALIGN.CENTER)

        ui_DiceCalculateButton.add_event_cb(DiceCalculateButton_eventhandler, lv.EVENT.ALL, None)
        OSBindingsManager.add_lvgl_object_binding(ui_DiceAppScreen, self.get_process_id())

    def end(self):
        from pdaos import KeyboardManager, OSBindingsManager
        OSBindingsManager.remove_lvgl_object_binding(self.get_process_id(), delete_lvgl_object=True, do_gc=True)


class SettingsApplication(Application):
    def __init__(self):
        super().__init__("Settings", "ST", "settings", 0x2B2B2B)

    def run(self, container: any):
        from pdaos import m_Config, OSBindingsManager

        def connect_to_wifi_with_config_params():
            import connectivity as con
            m_Config.load()
            conf: Config = m_Config.get()
            ssid: str = conf.get_setting("Internet", "WiFi SSID").setting_value
            pwd: str = conf.get_setting("Internet", "WiFi Password").setting_value
            con.connect_wifi(ssid, pwd)

        globals.set_signature_method("connect_to_wifi_with_config_params", connect_to_wifi_with_config_params)

        m_Config.load()
        # print(m_Config.get())

        def to_main_settings_screen():
            SetFlag(ui_SettingsCategoryList, lv.obj.FLAG.HIDDEN, False)
            SetFlag(ui_SettingsCategoryScreen, lv.obj.FLAG.HIDDEN, True)

        def to_category_screen():
            SetFlag(ui_SettingsCategoryList, lv.obj.FLAG.HIDDEN, True)
            SetFlag(ui_SettingsCategoryScreen, lv.obj.FLAG.HIDDEN, False)

        def create_category_button(container: any, category: ConfigCategory):
            def CategoryButton_eventhandler(event_struct):
                target = event_struct.get_target()
                event = event_struct.code
                if event == lv.EVENT.CLICKED and True:
                    create_category_screen(category)
                    to_category_screen()
                return

            ui_CategoryButton = lv.button(container)
            ui_CategoryButton.set_height(40)
            ui_CategoryButton.set_width(lv.pct(80))
            ui_CategoryButton.set_align(lv.ALIGN.CENTER)
            SetFlag(ui_CategoryButton, lv.obj.FLAG.SCROLLABLE, False)
            SetFlag(ui_CategoryButton, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
            ui_CategoryButton.set_style_bg_color(lv.color_hex(0x3E3E3E), lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_CategoryButton.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_CategoryButtonLabel = lv.label(ui_CategoryButton)
            ui_CategoryButtonLabel.set_text(category.category_name)
            ui_CategoryButtonLabel.set_width(lv.SIZE_CONTENT)  # 1
            ui_CategoryButtonLabel.set_height(lv.SIZE_CONTENT)  # 1
            ui_CategoryButtonLabel.set_align(lv.ALIGN.CENTER)

            ui_CategoryButton.add_event_cb(CategoryButton_eventhandler, lv.EVENT.ALL, None)
            return ui_CategoryButton

        def create_category_screen(category: ConfigCategory):
            option_obj_ids: list[str] = []

            def CategoryAndBackButton_eventhandler(event_struct):
                target = event_struct.get_target()
                event = event_struct.code
                if event == lv.EVENT.CLICKED and True:
                    m_Config.save()
                    to_main_settings_screen()
                    for ids in option_obj_ids:
                        ids: str
                        OSBindingsManager.remove_lvgl_object_binding(ids)
                return

            ui_CategoryTitleContainer = lv.obj(ui_SettingsCategoryScreen)
            ui_CategoryTitleContainer.remove_style_all()
            ui_CategoryTitleContainer.set_height(110)
            ui_CategoryTitleContainer.set_width(lv.pct(100))
            ui_CategoryTitleContainer.set_align(lv.ALIGN.TOP_MID)
            ui_CategoryTitleContainer.set_flex_flow(lv.FLEX_FLOW.COLUMN)
            ui_CategoryTitleContainer.set_flex_align(lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
            SetFlag(ui_CategoryTitleContainer, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_CategoryTitleContainer, lv.obj.FLAG.SCROLLABLE, False)

            ui_CategoryAndBackButton = lv.button(ui_CategoryTitleContainer)
            ui_CategoryAndBackButton.set_width(lv.SIZE_CONTENT)  # 1
            ui_CategoryAndBackButton.set_height(lv.SIZE_CONTENT)  # 1
            ui_CategoryAndBackButton.set_align(lv.ALIGN.CENTER)
            SetFlag(ui_CategoryAndBackButton, lv.obj.FLAG.SCROLLABLE, False)
            SetFlag(ui_CategoryAndBackButton, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
            ui_CategoryAndBackButton.set_style_bg_color(lv.color_hex(0x3A3A3A), lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_CategoryAndBackButton.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_SettingsCategoryTitleLabel = lv.label(ui_CategoryAndBackButton)
            ui_SettingsCategoryTitleLabel.set_text(category.category_name)
            ui_SettingsCategoryTitleLabel.set_width(lv.SIZE_CONTENT)  # 1
            ui_SettingsCategoryTitleLabel.set_height(lv.SIZE_CONTENT)  # 1
            ui_SettingsCategoryTitleLabel.set_align(lv.ALIGN.CENTER)

            ui_CategoryAndBackButton.add_event_cb(CategoryAndBackButton_eventhandler, lv.EVENT.ALL, None)
            ui_SettingsCategoryDesc = lv.label(ui_CategoryTitleContainer)
            ui_SettingsCategoryDesc.set_text(category.category_description)
            ui_SettingsCategoryDesc.set_width(lv.SIZE_CONTENT)  # 100
            ui_SettingsCategoryDesc.set_height(lv.SIZE_CONTENT)  # 30
            ui_SettingsCategoryDesc.set_x(0)
            ui_SettingsCategoryDesc.set_y(30)
            ui_SettingsCategoryDesc.set_align(lv.ALIGN.TOP_MID)
            ui_SettingsCategoryDesc.set_style_pad_left(10, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SettingsCategoryDesc.set_style_pad_right(10, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SettingsCategoryDesc.set_style_pad_top(10, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SettingsCategoryDesc.set_style_pad_bottom(10, lv.PART.MAIN | lv.STATE.DEFAULT)

            option_obj_ids.append(f"category_title_{id(ui_CategoryTitleContainer)}")
            OSBindingsManager.add_lvgl_object_binding(ui_CategoryTitleContainer, f"category_title_{id(ui_CategoryTitleContainer)}")

            category.category_items.sort(key=lambda x: x.setting_name)
            for opt in category.category_items:
                opt: ConfigSetting
                if opt.option_type == ConfigTypes.VALUE:
                    obj_id = create_value_input_option(opt, category)
                    s = f"value_input_{id(obj_id)}"
                    option_obj_ids.append(s)
                    OSBindingsManager.add_lvgl_object_binding(obj_id, s)
                elif opt.option_type == ConfigTypes.ACTION:
                    obj_id = create_run_action_button(opt, category)
                    s = f"action_{id(obj_id)}"
                    option_obj_ids.append(s)
                    OSBindingsManager.add_lvgl_object_binding(obj_id, s)
                elif opt.option_type == ConfigTypes.TOGGLE:
                    obj_id = create_toggle_option(opt, category)
                    s = f"toggle_{id(obj_id)}"
                    option_obj_ids.append(s)
                    OSBindingsManager.add_lvgl_object_binding(obj_id, s)
                elif opt.option_type == ConfigTypes.SLIDER:
                    obj_id = create_slider_option(opt, category)
                    s = f"slider_{id(obj_id)}"
                    option_obj_ids.append(s)
                    OSBindingsManager.add_lvgl_object_binding(obj_id, s)
                elif opt.option_type == ConfigTypes.DROPDOWN:
                    obj_id = create_dropdown_option(opt, category)
                    s = f"dropdown_{id(obj_id)}"
                    option_obj_ids.append(s)
                    OSBindingsManager.add_lvgl_object_binding(obj_id, s)
            return ui_SettingsCategoryScreen

        def create_toggle_option(opt: ConfigSetting, cat: ConfigCategory):
            def Toggle_eventhandler(event_struct):
                target = event_struct.get_target()
                event = event_struct.code
                if event == lv.EVENT.VALUE_CHANGED and True:
                    m_Config.get().get_setting(cat.category_name, opt.setting_name).setting_value = event_struct.get_target_obj().has_state(lv.STATE.CHECKED)
                return

            ui_SettingsToggleOption = lv.obj(ui_SettingsCategoryScreen)
            ui_SettingsToggleOption.remove_style_all()
            ui_SettingsToggleOption.set_height(80)
            ui_SettingsToggleOption.set_width(lv.pct(90))
            ui_SettingsToggleOption.set_align(lv.ALIGN.CENTER)
            ui_SettingsToggleOption.set_flex_flow(lv.FLEX_FLOW.ROW)
            ui_SettingsToggleOption.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.CENTER,
                                                   lv.FLEX_ALIGN.CENTER)
            SetFlag(ui_SettingsToggleOption, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_SettingsToggleOption, lv.obj.FLAG.SCROLLABLE, False)

            ui_ToggleOptionInfo = lv.obj(ui_SettingsToggleOption)
            ui_ToggleOptionInfo.remove_style_all()
            ui_ToggleOptionInfo.set_height(lv.pct(100))
            ui_ToggleOptionInfo.set_flex_grow(1)
            ui_ToggleOptionInfo.set_align(lv.ALIGN.CENTER)
            ui_ToggleOptionInfo.set_flex_flow(lv.FLEX_FLOW.COLUMN)
            ui_ToggleOptionInfo.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
            SetFlag(ui_ToggleOptionInfo, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_ToggleOptionInfo, lv.obj.FLAG.SCROLLABLE, False)
            ui_ToggleOptionInfo.set_style_pad_row(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ToggleOptionInfo.set_style_pad_column(0, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_OptionLabelStyler = lv.obj(ui_ToggleOptionInfo)
            ui_OptionLabelStyler.remove_style_all()
            ui_OptionLabelStyler.set_width(lv.SIZE_CONTENT)  # 100
            ui_OptionLabelStyler.set_height(lv.SIZE_CONTENT)  # 50
            ui_OptionLabelStyler.set_align(lv.ALIGN.CENTER)
            SetFlag(ui_OptionLabelStyler, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_OptionLabelStyler, lv.obj.FLAG.SCROLLABLE, False)
            ui_OptionLabelStyler.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_OptionLabelStyler.set_style_bg_color(lv.color_hex(0xA0BFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_OptionLabelStyler.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_OptionLabelStyler.set_style_pad_left(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_OptionLabelStyler.set_style_pad_right(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_OptionLabelStyler.set_style_pad_top(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_OptionLabelStyler.set_style_pad_bottom(5, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_ToggleOptionLabel = lv.label(ui_OptionLabelStyler)
            ui_ToggleOptionLabel.set_text(opt.setting_name)
            ui_ToggleOptionLabel.set_width(lv.SIZE_CONTENT)  # 1
            ui_ToggleOptionLabel.set_height(lv.SIZE_CONTENT)  # 1
            ui_ToggleOptionLabel.set_align(lv.ALIGN.CENTER)

            ui_ToggleOptionDesc = lv.label(ui_ToggleOptionInfo)
            ui_ToggleOptionDesc.set_text(opt.setting_description)
            ui_ToggleOptionDesc.set_width(lv.SIZE_CONTENT)  # 1
            ui_ToggleOptionDesc.set_height(lv.SIZE_CONTENT)  # 1
            ui_ToggleOptionDesc.set_align(lv.ALIGN.CENTER)

            ui_Toggle = lv.switch(ui_SettingsToggleOption)
            ui_Toggle.set_width(50)
            ui_Toggle.set_height(25)
            ui_Toggle.set_align(lv.ALIGN.CENTER)
            from osui import set_toggle_state
            set_toggle_state(ui_Toggle, bool(opt.setting_value))

            ui_Toggle.add_event_cb(Toggle_eventhandler, lv.EVENT.ALL, None)
            return ui_SettingsToggleOption

        def create_value_input_option(opt: ConfigSetting, cat: ConfigCategory):
            def ValueInput_eventhandler(event_struct):
                from pdaos import KeyboardManager
                target = event_struct.get_target()
                event = event_struct.code
                if event == lv.EVENT.CLICKED:
                    KeyboardManager.invoke_keyboard(event_struct.get_target_obj().get_text())
                    globals.set_temp_variable("ui_SettingValueOptionInput", event_struct.get_target_obj())
                    globals.set_temp_variable("valueInputOptionFocused", True)
                elif globals.get_temp_variable("valueInputOptionFocused") and not KeyboardManager.is_keyboard_focused():
                    try:
                        # TODO this part of the code doesn't work... probably related to the firmware itself (Oct 18, 2024)
                        def set_inputfield_text(*arg):
                            try:
                                globals.get_temp_variable("ui_SettingValueOptionInput").set_text(KeyboardManager.get_keyboard_text())
                                globals.remove_temp_variable("ui_SettingValueOptionInput")
                                m_Config.get().get_setting(cat.category_name, opt.setting_name).setting_value = event_struct.get_target_obj().get_text()
                            except Exception as e:
                                print(e)

                        globals.set_temp_variable("valueInputOptionFocused", False)
                        globals.remove_temp_variable("valueInputOptionFocused")
                        micropython.schedule(set_inputfield_text, None)
                    except Exception as e:
                        print(e)

                return

            ui_SettingsInputValueOption = lv.obj(ui_SettingsCategoryScreen)
            ui_SettingsInputValueOption.remove_style_all()
            ui_SettingsInputValueOption.set_height(80)
            ui_SettingsInputValueOption.set_width(lv.pct(90))
            ui_SettingsInputValueOption.set_align(lv.ALIGN.CENTER)
            ui_SettingsInputValueOption.set_flex_flow(lv.FLEX_FLOW.ROW)
            ui_SettingsInputValueOption.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.CENTER,
                                                       lv.FLEX_ALIGN.CENTER)
            SetFlag(ui_SettingsInputValueOption, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_SettingsInputValueOption, lv.obj.FLAG.SCROLLABLE, False)

            ui_ValueOptionInfo = lv.obj(ui_SettingsInputValueOption)
            ui_ValueOptionInfo.remove_style_all()
            ui_ValueOptionInfo.set_height(lv.pct(100))
            ui_ValueOptionInfo.set_flex_grow(1)
            ui_ValueOptionInfo.set_align(lv.ALIGN.CENTER)
            ui_ValueOptionInfo.set_flex_flow(lv.FLEX_FLOW.COLUMN)
            ui_ValueOptionInfo.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
            SetFlag(ui_ValueOptionInfo, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_ValueOptionInfo, lv.obj.FLAG.SCROLLABLE, False)
            ui_ValueOptionInfo.set_style_pad_row(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ValueOptionInfo.set_style_pad_column(0, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_ValueOptionLabelStyler = lv.obj(ui_ValueOptionInfo)
            ui_ValueOptionLabelStyler.remove_style_all()
            ui_ValueOptionLabelStyler.set_width(lv.SIZE_CONTENT)  # 100
            ui_ValueOptionLabelStyler.set_height(lv.SIZE_CONTENT)  # 50
            ui_ValueOptionLabelStyler.set_align(lv.ALIGN.CENTER)
            SetFlag(ui_ValueOptionLabelStyler, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_ValueOptionLabelStyler, lv.obj.FLAG.SCROLLABLE, False)
            ui_ValueOptionLabelStyler.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ValueOptionLabelStyler.set_style_bg_color(lv.color_hex(0xA0BFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ValueOptionLabelStyler.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ValueOptionLabelStyler.set_style_pad_left(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ValueOptionLabelStyler.set_style_pad_right(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ValueOptionLabelStyler.set_style_pad_top(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ValueOptionLabelStyler.set_style_pad_bottom(5, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_ValueOptionLabel = lv.label(ui_ValueOptionLabelStyler)
            ui_ValueOptionLabel.set_text(opt.setting_name)
            ui_ValueOptionLabel.set_width(lv.SIZE_CONTENT)  # 1
            ui_ValueOptionLabel.set_height(lv.SIZE_CONTENT)  # 1
            ui_ValueOptionLabel.set_align(lv.ALIGN.CENTER)

            ui_ValueOptionDesc = lv.label(ui_ValueOptionInfo)
            ui_ValueOptionDesc.set_text(opt.setting_description)
            ui_ValueOptionDesc.set_width(lv.SIZE_CONTENT)  # 1
            ui_ValueOptionDesc.set_height(lv.SIZE_CONTENT)  # 1
            ui_ValueOptionDesc.set_align(lv.ALIGN.CENTER)

            ui_ValueInput = lv.textarea(ui_SettingsInputValueOption)
            ui_ValueInput.set_width(lv.pct(30))
            ui_ValueInput.set_height(lv.pct(50))
            ui_ValueInput.set_placeholder_text("Value...")
            ui_ValueInput.set_align(lv.ALIGN.CENTER)
            ui_ValueInput.set_text(str(opt.setting_value))

            ui_ValueInput.add_event_cb(ValueInput_eventhandler, lv.EVENT.ALL, None)
            return ui_SettingsInputValueOption

        def create_slider_option(opt: ConfigSetting, cat: ConfigCategory):
            def Slider_eventhandler(event_struct):
                target = event_struct.get_target()
                event = event_struct.code
                if event == lv.EVENT.VALUE_CHANGED and True:
                    m_Config.get().get_setting(cat.category_name, opt.setting_name).setting_value = event_struct.get_target_obj().get_value()
                    ui_SliderValueLabel.set_text(str(event_struct.get_target_obj().get_value()))
                return

            ui_SettingsSliderOption = lv.obj(ui_SettingsCategoryScreen)
            ui_SettingsSliderOption.remove_style_all()
            ui_SettingsSliderOption.set_height(80)
            ui_SettingsSliderOption.set_width(lv.pct(90))
            ui_SettingsSliderOption.set_align(lv.ALIGN.CENTER)
            ui_SettingsSliderOption.set_flex_flow(lv.FLEX_FLOW.ROW)
            ui_SettingsSliderOption.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.CENTER,
                                                   lv.FLEX_ALIGN.CENTER)
            SetFlag(ui_SettingsSliderOption, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_SettingsSliderOption, lv.obj.FLAG.SCROLLABLE, False)
            ui_SettingsSliderOption.set_style_pad_row(0, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SettingsSliderOption.set_style_pad_column(20, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_SliderOptionInfo = lv.obj(ui_SettingsSliderOption)
            ui_SliderOptionInfo.remove_style_all()
            ui_SliderOptionInfo.set_height(lv.pct(100))
            ui_SliderOptionInfo.set_flex_grow(1)
            ui_SliderOptionInfo.set_align(lv.ALIGN.CENTER)
            ui_SliderOptionInfo.set_flex_flow(lv.FLEX_FLOW.COLUMN)
            ui_SliderOptionInfo.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
            SetFlag(ui_SliderOptionInfo, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_SliderOptionInfo, lv.obj.FLAG.SCROLLABLE, False)
            ui_SliderOptionInfo.set_style_pad_row(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SliderOptionInfo.set_style_pad_column(0, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_SliderOptionLabelStyler = lv.obj(ui_SliderOptionInfo)
            ui_SliderOptionLabelStyler.remove_style_all()
            ui_SliderOptionLabelStyler.set_width(lv.SIZE_CONTENT)  # 100
            ui_SliderOptionLabelStyler.set_height(lv.SIZE_CONTENT)  # 50
            ui_SliderOptionLabelStyler.set_align(lv.ALIGN.CENTER)
            SetFlag(ui_SliderOptionLabelStyler, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_SliderOptionLabelStyler, lv.obj.FLAG.SCROLLABLE, False)
            ui_SliderOptionLabelStyler.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SliderOptionLabelStyler.set_style_bg_color(lv.color_hex(0xA0BFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SliderOptionLabelStyler.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SliderOptionLabelStyler.set_style_pad_left(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SliderOptionLabelStyler.set_style_pad_right(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SliderOptionLabelStyler.set_style_pad_top(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_SliderOptionLabelStyler.set_style_pad_bottom(5, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_SliderOptionLabel = lv.label(ui_SliderOptionLabelStyler)
            ui_SliderOptionLabel.set_text(opt.setting_name)
            ui_SliderOptionLabel.set_width(lv.SIZE_CONTENT)  # 1
            ui_SliderOptionLabel.set_height(lv.SIZE_CONTENT)  # 1
            ui_SliderOptionLabel.set_align(lv.ALIGN.CENTER)

            ui_SliderOptionDesc = lv.label(ui_SliderOptionInfo)
            ui_SliderOptionDesc.set_text(opt.setting_description)
            ui_SliderOptionDesc.set_width(lv.SIZE_CONTENT)  # 1
            ui_SliderOptionDesc.set_height(lv.SIZE_CONTENT)  # 1
            ui_SliderOptionDesc.set_align(lv.ALIGN.CENTER)

            ui_SliderValueLabel = lv.label(ui_SettingsSliderOption)
            ui_SliderValueLabel.set_text(str(opt.setting_value))
            ui_SliderValueLabel.set_width(lv.SIZE_CONTENT)  # 1
            ui_SliderValueLabel.set_height(lv.SIZE_CONTENT)  # 1
            ui_SliderValueLabel.set_align(lv.ALIGN.CENTER)

            ui_Slider = lv.slider(ui_SettingsSliderOption)
            ui_Slider.set_width(lv.pct(30))
            ui_Slider.set_height(lv.pct(20))
            ui_Slider.set_align(lv.ALIGN.CENTER)
            if opt.min < opt.max: ui_Slider.set_range(opt.min, opt.max)
            ui_Slider.set_value(int(opt.setting_value), lv.ANIM.OFF)  # need refresh: 0,100
            if 'NORMAL' is 'RANGE': ui_Slider.set_left_value(0, lv.ANIM.OFF)

            # Compensating for LVGL9.1 draw crash with bar/slider max value when top-padding is nonzero and right-padding is 0
            if (ui_Slider.get_style_pad_top(lv.PART.MAIN) > 0): ui_Slider.set_style_pad_right(
                ui_Slider.get_style_pad_right(lv.PART.MAIN) + 1, lv.PART.MAIN)
            ui_Slider.add_event_cb(Slider_eventhandler, lv.EVENT.ALL, None)
            return ui_SettingsSliderOption

        def create_dropdown_option(opt: ConfigSetting, cat: ConfigCategory):
            def Dropdown_eventhandler(event_struct):
                target = event_struct.get_target()
                event = event_struct.code
                if event == lv.EVENT.VALUE_CHANGED and True:
                    m_Config.get().get_setting(cat.category_name, opt.setting_name).setting_value = event_struct.get_target_obj().get_selected_str()
                return

            ui_SettingsDropdownOption = lv.obj(ui_SettingsCategoryScreen)
            ui_SettingsDropdownOption.remove_style_all()
            ui_SettingsDropdownOption.set_height(80)
            ui_SettingsDropdownOption.set_width(lv.pct(90))
            ui_SettingsDropdownOption.set_align(lv.ALIGN.CENTER)
            ui_SettingsDropdownOption.set_flex_flow(lv.FLEX_FLOW.ROW)
            ui_SettingsDropdownOption.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.CENTER,
                                                     lv.FLEX_ALIGN.CENTER)
            SetFlag(ui_SettingsDropdownOption, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_SettingsDropdownOption, lv.obj.FLAG.SCROLLABLE, False)

            ui_DropdownOptionInfo = lv.obj(ui_SettingsDropdownOption)
            ui_DropdownOptionInfo.remove_style_all()
            ui_DropdownOptionInfo.set_height(lv.pct(100))
            ui_DropdownOptionInfo.set_flex_grow(1)
            ui_DropdownOptionInfo.set_align(lv.ALIGN.CENTER)
            ui_DropdownOptionInfo.set_flex_flow(lv.FLEX_FLOW.COLUMN)
            ui_DropdownOptionInfo.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
            SetFlag(ui_DropdownOptionInfo, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_DropdownOptionInfo, lv.obj.FLAG.SCROLLABLE, False)
            ui_DropdownOptionInfo.set_style_pad_row(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_DropdownOptionInfo.set_style_pad_column(0, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_DropdownOptionLabelStyler = lv.obj(ui_DropdownOptionInfo)
            ui_DropdownOptionLabelStyler.remove_style_all()
            ui_DropdownOptionLabelStyler.set_width(lv.SIZE_CONTENT)  # 100
            ui_DropdownOptionLabelStyler.set_height(lv.SIZE_CONTENT)  # 50
            ui_DropdownOptionLabelStyler.set_align(lv.ALIGN.CENTER)
            SetFlag(ui_DropdownOptionLabelStyler, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_DropdownOptionLabelStyler, lv.obj.FLAG.SCROLLABLE, False)
            ui_DropdownOptionLabelStyler.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_DropdownOptionLabelStyler.set_style_bg_color(lv.color_hex(0xA0BFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_DropdownOptionLabelStyler.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_DropdownOptionLabelStyler.set_style_pad_left(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_DropdownOptionLabelStyler.set_style_pad_right(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_DropdownOptionLabelStyler.set_style_pad_top(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_DropdownOptionLabelStyler.set_style_pad_bottom(5, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_DropdownOptionLabel = lv.label(ui_DropdownOptionLabelStyler)
            ui_DropdownOptionLabel.set_text(opt.setting_name)
            ui_DropdownOptionLabel.set_width(lv.SIZE_CONTENT)  # 1
            ui_DropdownOptionLabel.set_height(lv.SIZE_CONTENT)  # 1
            ui_DropdownOptionLabel.set_align(lv.ALIGN.CENTER)

            ui_DropdownOptionDesc = lv.label(ui_DropdownOptionInfo)
            ui_DropdownOptionDesc.set_text(opt.setting_description)
            ui_DropdownOptionDesc.set_width(lv.SIZE_CONTENT)  # 1
            ui_DropdownOptionDesc.set_height(lv.SIZE_CONTENT)  # 1
            ui_DropdownOptionDesc.set_align(lv.ALIGN.CENTER)

            ui_Dropdown = lv.dropdown(ui_SettingsDropdownOption)
            optstring: str = ""
            for i in list(opt.values):
                optstring += i + "\n"
            optstring = optstring[:-1]
            ui_Dropdown.set_options(optstring)
            ui_Dropdown.set_width(lv.pct(30))
            ui_Dropdown.set_height(lv.SIZE_CONTENT)  # 1
            ui_Dropdown.set_align(lv.ALIGN.CENTER)
            ui_Dropdown.set_text( str(opt.setting_value) if len(list(opt.values))>0 else None)
            SetFlag(ui_Dropdown, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

            ui_Dropdown.add_event_cb(Dropdown_eventhandler, lv.EVENT.ALL, None)
            return ui_SettingsDropdownOption

        def create_run_action_button(opt: ConfigSetting, cat: ConfigCategory):
            def RunActionButton_eventhandler(event_struct):
                target = event_struct.get_target()
                event = event_struct.code
                if event == lv.EVENT.CLICKED and True:
                    globals.get_signature_method(str(opt.setting_value))()
                return

            ui_SettingsActionOption = lv.obj(ui_SettingsCategoryScreen)
            ui_SettingsActionOption.remove_style_all()
            ui_SettingsActionOption.set_height(80)
            ui_SettingsActionOption.set_width(lv.pct(90))
            ui_SettingsActionOption.set_align(lv.ALIGN.CENTER)
            ui_SettingsActionOption.set_flex_flow(lv.FLEX_FLOW.ROW)
            ui_SettingsActionOption.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.CENTER,
                                                   lv.FLEX_ALIGN.CENTER)
            SetFlag(ui_SettingsActionOption, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_SettingsActionOption, lv.obj.FLAG.SCROLLABLE, False)

            ui_ActionOptionInfo = lv.obj(ui_SettingsActionOption)
            ui_ActionOptionInfo.remove_style_all()
            ui_ActionOptionInfo.set_height(lv.pct(100))
            ui_ActionOptionInfo.set_flex_grow(1)
            ui_ActionOptionInfo.set_align(lv.ALIGN.CENTER)
            ui_ActionOptionInfo.set_flex_flow(lv.FLEX_FLOW.COLUMN)
            ui_ActionOptionInfo.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
            SetFlag(ui_ActionOptionInfo, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_ActionOptionInfo, lv.obj.FLAG.SCROLLABLE, False)
            ui_ActionOptionInfo.set_style_pad_row(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ActionOptionInfo.set_style_pad_column(0, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_ActionOptionLabelStyler = lv.obj(ui_ActionOptionInfo)
            ui_ActionOptionLabelStyler.remove_style_all()
            ui_ActionOptionLabelStyler.set_width(lv.SIZE_CONTENT)  # 100
            ui_ActionOptionLabelStyler.set_height(lv.SIZE_CONTENT)  # 50
            ui_ActionOptionLabelStyler.set_align(lv.ALIGN.CENTER)
            SetFlag(ui_ActionOptionLabelStyler, lv.obj.FLAG.CLICKABLE, False)
            SetFlag(ui_ActionOptionLabelStyler, lv.obj.FLAG.SCROLLABLE, False)
            ui_ActionOptionLabelStyler.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ActionOptionLabelStyler.set_style_bg_color(lv.color_hex(0xA0BFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ActionOptionLabelStyler.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ActionOptionLabelStyler.set_style_pad_left(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ActionOptionLabelStyler.set_style_pad_right(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ActionOptionLabelStyler.set_style_pad_top(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            ui_ActionOptionLabelStyler.set_style_pad_bottom(5, lv.PART.MAIN | lv.STATE.DEFAULT)

            ui_ActionOptionLabel = lv.label(ui_ActionOptionLabelStyler)
            ui_ActionOptionLabel.set_text(opt.setting_name)
            ui_ActionOptionLabel.set_width(lv.SIZE_CONTENT)  # 1
            ui_ActionOptionLabel.set_height(lv.SIZE_CONTENT)  # 1
            ui_ActionOptionLabel.set_align(lv.ALIGN.CENTER)

            ui_ActionOptionDesc = lv.label(ui_ActionOptionInfo)
            ui_ActionOptionDesc.set_text(opt.setting_description)
            ui_ActionOptionDesc.set_width(lv.SIZE_CONTENT)  # 1
            ui_ActionOptionDesc.set_height(lv.SIZE_CONTENT)  # 1
            ui_ActionOptionDesc.set_align(lv.ALIGN.CENTER)

            ui_RunActionButton = lv.button(ui_SettingsActionOption)
            ui_RunActionButton.set_width(lv.SIZE_CONTENT)  # 1
            ui_RunActionButton.set_height(lv.SIZE_CONTENT)  # 50
            ui_RunActionButton.set_align(lv.ALIGN.CENTER)
            SetFlag(ui_RunActionButton, lv.obj.FLAG.SCROLLABLE, False)
            SetFlag(ui_RunActionButton, lv.obj.FLAG.SCROLL_ON_FOCUS, True)

            ui_RunActionButtonLabel = lv.label(ui_RunActionButton)
            ui_RunActionButtonLabel.set_text("Run Action")
            ui_RunActionButtonLabel.set_width(lv.SIZE_CONTENT)  # 1
            ui_RunActionButtonLabel.set_height(lv.SIZE_CONTENT)  # 1
            ui_RunActionButtonLabel.set_align(lv.ALIGN.CENTER)

            ui_RunActionButton.add_event_cb(RunActionButton_eventhandler, lv.EVENT.ALL, None)
            return ui_SettingsActionOption

        ui_SettingsAppScreen = lv.obj(container)
        ui_SettingsAppScreen.remove_style_all()
        ui_SettingsAppScreen.set_width(lv.pct(100))
        ui_SettingsAppScreen.set_height(lv.pct(100))
        ui_SettingsAppScreen.set_align(lv.ALIGN.CENTER)
        SetFlag(ui_SettingsAppScreen, lv.obj.FLAG.CLICKABLE, False)
        SetFlag(ui_SettingsAppScreen, lv.obj.FLAG.SCROLLABLE, False)

        ui_SettingsCategoryList = lv.obj(ui_SettingsAppScreen)
        ui_SettingsCategoryList.remove_style_all()
        ui_SettingsCategoryList.set_width(lv.pct(100))
        ui_SettingsCategoryList.set_height(lv.pct(95))
        ui_SettingsCategoryList.set_align(lv.ALIGN.BOTTOM_MID)
        ui_SettingsCategoryList.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        ui_SettingsCategoryList.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        SetFlag(ui_SettingsCategoryList, lv.obj.FLAG.HIDDEN, False)
        SetFlag(ui_SettingsCategoryList, lv.obj.FLAG.SCROLLABLE, True)
        ui_SettingsCategoryList.set_style_pad_row( 10, lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_SettingsCategoryList.set_style_pad_column( 0, lv.PART.MAIN | lv.STATE.DEFAULT )

        ui_SettingsMainTitle = lv.label(ui_SettingsCategoryList)
        ui_SettingsMainTitle.set_text("Settings")
        ui_SettingsMainTitle.set_width(lv.SIZE_CONTENT)  # 100
        ui_SettingsMainTitle.set_height(lv.SIZE_CONTENT)  # 1
        ui_SettingsMainTitle.set_x(0)
        ui_SettingsMainTitle.set_y(30)
        ui_SettingsMainTitle.set_align(lv.ALIGN.TOP_MID)
        ui_SettingsMainTitle.set_style_pad_left(10, lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_SettingsMainTitle.set_style_pad_right(10, lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_SettingsMainTitle.set_style_pad_top(10, lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_SettingsMainTitle.set_style_pad_bottom(10, lv.PART.MAIN | lv.STATE.DEFAULT)

        ui_SettingsCategoryScreen = lv.obj(ui_SettingsAppScreen)
        ui_SettingsCategoryScreen.remove_style_all()
        ui_SettingsCategoryScreen.set_width(lv.pct(100))
        ui_SettingsCategoryScreen.set_height(lv.pct(100))
        ui_SettingsCategoryScreen.set_align(lv.ALIGN.BOTTOM_MID)
        ui_SettingsCategoryScreen.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        ui_SettingsCategoryScreen.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        SetFlag(ui_SettingsCategoryScreen, lv.obj.FLAG.HIDDEN, True)
        SetFlag(ui_SettingsCategoryScreen, lv.obj.FLAG.SCROLLABLE, True)

        ui_SettingsCategoryScreen.set_style_pad_row(20, lv.PART.SCROLLBAR | lv.STATE.DEFAULT)
        ui_SettingsCategoryScreen.set_style_pad_column(10, lv.PART.SCROLLBAR | lv.STATE.DEFAULT)
        # print(ui_SettingsCategoryList)
        for i in m_Config.get().config_categories:
            i: ConfigCategory
            btn = create_category_button(ui_SettingsCategoryList, i)
            # print(btn)
            OSBindingsManager.add_lvgl_object_binding(btn, f"config_category_button_{id(btn)}")
        OSBindingsManager.add_lvgl_object_binding(ui_SettingsAppScreen, self.get_process_id())

    def end(self):
        from pdaos import KeyboardManager, OSBindingsManager
        OSBindingsManager.remove_lvgl_object_binding(self.get_process_id(), delete_lvgl_object=True, do_gc=True)

