import gc

import globals
import osui
import asyncio

from globals import APPS, FOCUSED_APP, OS_LOADED, ASYNC_JOBS, QUEUED_MODALS, QUEUED_NOTIFICATIONS, get_focused_app, set_focused_app
from pdaos_lib import Application, AsyncJob, LVGLToObjectBindings, Modal, Notification, DataManager, Config, \
    get_os_version, ConfigCategory, ConfigSetting, ConfigTypes


class AsyncJobsManager:
    async def run_async_jobs(self, identifier: str = None):
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

    async def stop_async_jobs(self, identifier: str = None):
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

    async def clear_async_jobs(self):
        ASYNC_JOBS.clear()
        gc.enable()
        gc.collect()

    async def schedule_async_job(self, job: AsyncJob, execute_now: bool = False):
        ASYNC_JOBS.append(job)
        if execute_now:
            job.execute()


class AppsManager:
    def open_app(self, app: Application):
        from globals import get_focused_app, set_focused_app, no_focused_app
        print(f"Called open_app. Debug: {app.get_process_id()}, {app.get_name()}, {no_focused_app()}")
        self.close_app(get_focused_app())  # Close the current app if any
        set_focused_app(app)
        # print(f"Set Focused App: {get_focused_app()}")
        osui.update_main_screen()
        # print(f"Set Focused App: {get_focused_app()}")
        get_focused_app().run(osui.get_application_screen_container())
        # print(f"Set Focused App: {get_focused_app()}")

    def close_app(self, app: Application):
        if app is None:
            return

        from globals import set_focused_app, no_focused_app
        set_focused_app(None)

        if app:
            m_AsyncJobs.stop_async_jobs(app.get_process_id())
            osui.remove_lvgl_object_binding(app.get_process_id(), delete_lvgl_object=True, do_gc=True)

        osui.update_main_screen()
        print(f"Called close_app(). Debug: {app.get_process_id()}, {app.get_name()}, {no_focused_app()}")

    def add_app(self, app: Application):
        if not OS_LOADED:
            pass
        APPS.append(app)

    def remove_app(self, name_or_screen: str):
        for app in APPS:
            if app.app_name == name_or_screen or app.app_screen == name_or_screen:
                APPS.remove(app)


class KeyboardManager:
    def is_keyboard_focused(self) -> bool:
        return osui.KB_FOCUSED

    def revoke_keybaord(self):
        osui.set_keyboard_state(False)

    async def use_keyboard(self, init_text: str = "") -> str:
        self.invoke_keyboard(init_text)
        while self.is_keyboard_focused():
            await asyncio.sleep(0.1)
        return self.get_keyboard_text()

    def invoke_keyboard(self, init_text: str = "", callback: callable = None):
        self.set_keyboard_text(init_text)
        osui.set_keyboard_state(True)

    def get_keyboard_text(self) -> str:
        return osui.get_keyboard_content()

    def set_keyboard_text(self, text: str):
        osui.set_keyboard_content(text)


class OSBindingsManager:
    def add_lvgl_object_binding(self, obj: any, identifier: str):
        osui.add_lvgl_object_binding(obj, identifier)

    def get_lvgl_object_binding(self, identifier: str) -> LVGLToObjectBindings | None:
        return osui.get_lvgl_object_binding(identifier)

    def remove_lvgl_object_binding(self, identifier: str, delete_lvgl_object: bool = True, do_gc: bool = False):
        osui.remove_lvgl_object_binding(identifier, delete_lvgl_object, do_gc)

    def refresh_lvgl_app_objects(self):
        osui.refresh_lvgl_app_objects(globals.APPS)


class OSUIManager:
    def push_modal(self, modal: Modal):
        QUEUED_MODALS.append(modal)

    def push_notif(self, notif: Notification):
        QUEUED_NOTIFICATIONS.append(notif)

    def to_home(self):
        from globals import no_focused_app
        if not no_focused_app():
            m_Apps.close_app(globals.get_focused_app())
        osui.update_main_screen()


class OSConfigManager(DataManager):
    def __init__(self):
        super().__init__("sys_conf.json")

    def load(self) -> any:
        data = super().load()
        if data is None:
            def connect_to_wifi_with_config_params():
                import connectivity as con
                m_Config.load()
                ssid: str = m_Config.get()["Internet"]["WiFi SSID"]
                pwd: str = m_Config.get()["Internet"]["WiFi Password"]
                con.connect_wifi(ssid, pwd)

            data = Config("PDA-OS Config", get_os_version(), [
                ConfigCategory("Internet", "Internet-related settings.", [
                    ConfigSetting("WiFi SSID", "SSID of the WiFi network to connect to.", "", ConfigTypes.VALUE),
                    ConfigSetting("WiFi Password", "Password of the WiFi network to connect to.", "", ConfigTypes.VALUE),
                    ConfigSetting("WiFi Autoconnect", "Automatically connect to the WiFi network on boot.", False, ConfigTypes.TOGGLE),
                    ConfigSetting("WiFi Autoconnect Timeout", "Timeout in seconds to wait for WiFi connection.", 10, ConfigTypes.VALUE),
                    ConfigSetting("Connect to WiFi", "Connect to the WiFi network.", False, ConfigTypes.ACTION)
                ]),
                ConfigCategory("Display", "Display-related settings.", [])
            ])

    def change(self, value: any, save: bool = False, *keys):
        if self.content is not None:
            current = self.content
            for arg in keys[:-1]:
                current = getattr(current, arg)
            setattr(current, keys[-1], value)
            if save:
                self.save()


m_AsyncJobs = AsyncJobsManager()
m_Apps = AppsManager()
m_Keyboard = KeyboardManager()
m_Bindings = OSBindingsManager()
m_OSUI = OSUIManager()
m_Config = OSConfigManager()

def load():
    import applications as apcs
    globals.OS_LOADED = True
    # Loads the default apps
    m_Apps.add_app(apcs.SettingsApplication())
    m_Apps.add_app(apcs.DiceApplication())
    m_Bindings.refresh_lvgl_app_objects()

    asyncio.run(m_AsyncJobs.run_async_jobs())


async def os_update():
    """
    OS-Level Async Updates.
    """
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