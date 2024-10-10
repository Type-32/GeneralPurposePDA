class Application:
    def __init__(self, name: str = "Untitled App", icon: str = "??", screen: str = "untitled_screen", color: int = 0x5385ED, tick_update: callable = None, second_update: callable = None):
        self.app_name = name
        self.app_icon = icon
        self.app_screen = screen
        self.app_tick = tick_update
        self.app_second = second_update
        self.app_color = color

    def get_name(self):
        return self.app_name

    def get_icon(self):
        return self.app_icon

    def get_screen(self):
        return self.app_screen

    def get_color(self):
        return self.app_color

    def get_tick(self):
        return self.app_tick

    def get_second(self):
        return self.app_second
