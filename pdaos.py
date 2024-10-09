import osui
import asyncio

class Application:
    def __init__(self, name: str, icon: str, screen: str, color: int = 0x5385ED, tick_update: callable = None, second_update: callable = None):
        self.app_name = "AppName"
        self.app_icon = "IC"
        self.app_screen = "screen"
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


apps: list[Application] = []
focused_app: Application = None
loaded_os: bool = False

def has_focused_app() -> bool:
    return focused_app is not None


def add_app(app: Application):
    if not loaded_os:
        pass
    apps.append(app)


def remove_app(name_or_screen: str):
    for app in apps:
        if app.app_name == name_or_screen or app.app_screen == name_or_screen:
            apps.remove(app)


def load():
    global loaded_os
    loaded_os = True
    # Loads the default apps
    settings_app = Application("Settings", "ST", "settings", 0x2B2B2B)
    dice_roller_app = Application("Dices", "DC", "dices", 0xE4080A)
    add_app(settings_app)
    add_app(dice_roller_app)
    osui.refresh_lvgl_app_objects(apps)


async def app_runner(app: Application):
    while True:
        if app.app_tick:
            await app.app_tick()
        await asyncio.sleep(1)  # Adjust the interval as needed


async def app_second_runner(app: Application):
    while True:
        if app.app_second:
            await app.app_second()
        await asyncio.sleep(1)


def open_app(app: Application):
    global focused_app
    close_app(focused_app)  # Close the current app if any
    focused_app = app
    # Load the app's initialization
    if app.app_tick:
        app.task = asyncio.create_task(app_runner(app))
    if app.app_second:
        asyncio.create_task(app_second_runner(app))
    # Load App UI
    osui.load_app_ui(app)


def close_app(app: Application):
    global focused_app
    if app:
        # Remove its update from the async pool
        if app.task:
            app.task.cancel()
        # Remove its UI from the screen
        osui.unload_app_ui(app)
        # Clear cache (implement cache clearing logic if needed)
        # Switch to the main screen
        osui.switch_to_main_screen()
        focused_app = None


async def os_update():
    while True:
        # Perform any OS-level updates here
        # For example, update the time display, check battery status, etc.
        await osui.update()


async def gc_coroutine(interval: int):
    """
    Runs a coroutine for a Garbage Collector.
    :param interval: The interval between each GC in seconds.
    """
    import gc
    gc.enable()
    while True:
        gc.collect()
        await asyncio.sleep(interval)


async def main():
    asyncio.run(os_update())
    asyncio.run(gc_coroutine(60)) # Run a 60-minute GC.

    while True:
        # Handling above-OS-Level stuff here, e.g. Notifications, App launch requests, etc.
        await asyncio.sleep(0.1)