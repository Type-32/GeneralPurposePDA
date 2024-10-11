from pdaos_lib import Application


class DiceApplication(Application):
    def __init__(self):
        super().__init__("Dices", "DC", "dices", 0xE4080A)

    async def run(self):
        # UI shit
        pass

    def