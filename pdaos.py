import gc

import globals
import osui
import asyncio
import json

from globals import QUEUED_MODALS, QUEUED_NOTIFICATIONS, get_focused_app, OS_LOADED, APPS, ASYNC_JOBS
from osui import update_main_screen, get_application_screen_container, remove_lvgl_object_binding, set_keyboard_state, \
    get_keyboard_content, set_keyboard_content, add_lvgl_object_binding, get_lvgl_object_binding, \
    refresh_lvgl_app_objects

from pdaos_lib import DataManager, Config, \
    get_os_version, ConfigCategory, ConfigSetting, ConfigTypes, Modal, Notification, Application, LVGLToObjectBindings, \
    AsyncJob

DEFAULT_CONFIG: Config = (
    Config("PDA-OS Config", get_os_version(), [
        ConfigCategory("Internet", "Internet-related settings.", [
            ConfigSetting("WiFi SSID", "SSID of the WiFi network to connect to.", "", ConfigTypes.VALUE),
            ConfigSetting("WiFi Password", "Password of the WiFi network to connect to.", "", ConfigTypes.VALUE),
            ConfigSetting("WiFi Autoconnect", "Automatically connect to the WiFi network on boot.", False, ConfigTypes.TOGGLE),
            ConfigSetting("WiFi Autoconnect Timeout", "Timeout in seconds to wait for WiFi connection.", 10, ConfigTypes.VALUE),
            ConfigSetting("Connect to WiFi", "Connect to the WiFi network.", "connect_to_wifi_with_config_params", ConfigTypes.ACTION)
        ]),
        ConfigCategory("Display", "Display-related settings.", [
            ConfigSetting("Backlight", "Backlight intensity.", 100, ConfigTypes.SLIDER, min=1, max=100),
            ConfigSetting("Dim Screen Duration", "The number of seconds of inactivity before dimming the screen automatically.", 20, ConfigTypes.SLIDER, min=10, max=60)
        ]),
        ConfigCategory("Synchronization", "Synchronization-related settings.", [
            ConfigSetting("Time", "Synchronize the time with an NTP server.", "config_sync_time", ConfigTypes.ACTION)
        ])
    ])
)


class OSConfigManager(DataManager):
    def __init__(self):
        super().__init__("sys_conf.json")
        self.content: Config = DEFAULT_CONFIG

    def load(self) -> any:
        temp = super().load()
        if temp is None:
            # def connect_to_wifi_with_config_params():
            #     import connectivity as con
            #     m_Config.load()
            #     ssid: str = m_Config.get()["Internet"]["WiFi SSID"]
            #     pwd: str = m_Config.get()["Internet"]["WiFi Password"]
            #     con.connect_wifi(ssid, pwd)

            self.content = DEFAULT_CONFIG
            self.save()
        else:
            self.content = Config()
            self.content.decode(temp)
        return self.content

    def save(self):
        if not self.content:
            print("No default data found. Proceeding to overwrite.")
        with open(self.file_name, 'w') as f:
            f.write(json.dumps(self.content.encode()))

    def change(self, value: any, save: bool = False, *keys):
        if self.content is not None:
            current = self.content
            for arg in keys[:-1]:
                current = getattr(current, arg)
            setattr(current, keys[-1], value)
            if save:
                self.save()


m_Config = OSConfigManager()

def load():
    # this is having errors
    from applications import SettingsApplication, DiceApplication
    globals.OS_LOADED = True
    # Loads the default apps
    AppsManager.add_app(SettingsApplication())
    AppsManager.add_app(DiceApplication())
    OSBindingsManager.refresh_lvgl_app_objects()

    asyncio.run(AsyncJobsManager.run_async_jobs())
    m_Config.load()


async def os_update():
    """OS-Level Async Updates."""
    pass
    # while True:
    #     # Perform any OS-level updates here
    #     # For example, update the time display, check battery status, etc.
    #     await osui.update() # UI Update Thread


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
    await osui.update() # Start OS-UI Async Updates
    asyncio.run(os_update())
    asyncio.run(gc_coroutine(60)) # Run a 60-second GC. Must use asyncio.run() to run in the background.

    # while True:
    #     # Handling above-OS-Level stuff here, e.g. Notifications, App launch requests, etc.
    #     await asyncio.sleep(0.1)


KB_FOCUSED: bool = False


class OSUIManager:
    @staticmethod
    def push_modal(modal: Modal):
        osui.push_modal(modal)

    @staticmethod
    def push_notif(notif: Notification):
        osui.push_notif(notif)

    @staticmethod
    def to_home():
        osui.to_home()


class AppsManager:
    @staticmethod
    def open_app(app: Application):
        osui.open_app(app)

    @staticmethod
    def close_app(app: Application):
        osui.close_app(app)

    @staticmethod
    def add_app(app: Application):
        if not OS_LOADED:
            pass
        APPS.append(app)

    @staticmethod
    def remove_app(name_or_screen: str):
        for app in APPS:
            if app.app_name == name_or_screen or app.app_screen == name_or_screen:
                APPS.remove(app)


class KeyboardManager:
    @staticmethod
    def is_keyboard_focused() -> bool:
        return KB_FOCUSED

    @staticmethod
    def revoke_keybaord():
        set_keyboard_state(False)

    @staticmethod
    async def use_keyboard(init_text: str = "") -> str:
        KeyboardManager.invoke_keyboard(init_text)
        while KeyboardManager.is_keyboard_focused():
            await asyncio.sleep(0.1)
        return KeyboardManager.get_keyboard_text()

    @staticmethod
    def invoke_keyboard(init_text: str = "", callback: callable = None):
        KeyboardManager.set_keyboard_text(init_text)
        set_keyboard_state(True)

    @staticmethod
    def get_keyboard_text() -> str:
        return get_keyboard_content()

    @staticmethod
    def set_keyboard_text(text: str):
        set_keyboard_content(text)


class OSBindingsManager:
    @staticmethod
    def add_lvgl_object_binding(obj: any, identifier: str):
        add_lvgl_object_binding(obj, identifier)

    @staticmethod
    def get_lvgl_object_binding(identifier: str) -> LVGLToObjectBindings | None:
        return get_lvgl_object_binding(identifier)

    @staticmethod
    def remove_lvgl_object_binding(identifier: str, delete_lvgl_object: bool = True, do_gc: bool = False):
        remove_lvgl_object_binding(identifier, delete_lvgl_object, do_gc)

    @staticmethod
    def refresh_lvgl_app_objects():
        refresh_lvgl_app_objects(APPS)


class AsyncJobsManager:
    @staticmethod
    async def run_async_jobs(identifier: str = None):
        """
        Run asynchronous jobs.

        If an identifier is provided, only the job with that identifier will be executed.
        Otherwise, all jobs in the ASYNC_JOBS list will be executed concurrently.

        :param identifier: Optional identifier of the job to execute.
        """
        if identifier is not None:
            for job in ASYNC_JOBS:
                job: AsyncJob
                if job.job_id == identifier:
                    job.execute()
        else:
            tasks = []
            for job in ASYNC_JOBS:
                job: AsyncJob
                tasks.append(job.create_task())
            if len(tasks) > 0:
                await asyncio.gather(*tasks)

    @staticmethod
    async def stop_async_jobs(identifier: str = None):
        """
        Stop asynchronous jobs.

        If an identifier is provided, only the job with that identifier will be stopped.
        Otherwise, all jobs in the ASYNC_JOBS list will be stopped.

        :param identifier: Optional identifier of the job to stop.
        """
        if identifier is not None:
            for job in ASYNC_JOBS:
                job: AsyncJob
                if job.job_id == identifier:
                    job.cancel()
        else:
            for job in ASYNC_JOBS:
                job.cancel()
                gc.enable()
                gc.collect()

    @staticmethod
    async def clear_async_jobs():
        ASYNC_JOBS.clear()
        gc.enable()
        gc.collect()

    @staticmethod
    async def schedule_async_job(job: AsyncJob, execute_now: bool = False):
        ASYNC_JOBS.append(job)
        if execute_now:
            job.execute()
