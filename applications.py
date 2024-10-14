import asyncio

import globals
import pdaos
from pdaos_lib import Application, AsyncJob
from osui import SetFlag, add_lvgl_object_binding
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
        elif len(segments) == 1:
            if print_output: print(random.randint(1, int(segments[1])))
        return rolls

    def run(self, container: any):

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
                print("Editing dice parser text")
                # help(event_struct.get_target_obj())
                pdaos.invoke_keyboard(event_struct.get_target_obj().get_text())
                globals.set_temp_variable("ui_DiceParserInput", event_struct.get_target_obj())
                globals.set_temp_variable("diceParserFocused", True)
            elif globals.get_temp_variable("diceParserFocused") and not pdaos.is_keyboard_focused():
                globals.set_temp_variable("diceParserFocused", False)
                globals.remove_temp_variable("diceParserFocused")
                print("Woah")
                # pdaos.revoke_keybaord()
                globals.get_temp_variable("ui_DiceParserInput").set_text(pdaos.get_keyboard_text())
                globals.remove_temp_variable("ui_DiceParserInput")
            return

        def DiceCalculateButton_eventhandler(event_struct):
            target = event_struct.get_target()
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                set_result(DiceApplication.parseDiceRoll(event_struct.get_target_obj().get_text(), False)[0])
            return

        def set_result(number: int):
            ui_DiceRollResult.set_text(f"Result: {number}")

        def quick_roll(dice_number: int) -> int:
            return DiceApplication.parseDiceRoll(f"d{dice_number}")[0]

        # async def sync_text_to_area(self):
        #     while True:
        #         if self.diceParserFocused and not pdaos.is_keyboard_focused():
        #             print(self.ui_DiceParserInput.set_text(pdaos.get_keyboard_text()))
        #             self.diceParserFocused = False
        #         await asyncio.sleep(0.1)

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
        add_lvgl_object_binding(ui_DiceAppScreen, self.get_process_id())


class SettingsApplication(Application):
    def __init__(self):
        super().__init__("Settings", "ST", "settings", 0x2B2B2B)

    async def run(self, container: any):
        # UI shit
        pass