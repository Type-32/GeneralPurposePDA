import gc

import globals
import osui
import asyncio

from globals import APPS, FOCUSED_APP, OS_LOADED, ASYNC_JOBS, QUEUED_MODALS, QUEUED_NOTIFICATIONS, get_focused_app, set_focused_app
from pdaos_lib import Application, AsyncJob, LVGLToObjectBindings, Modal, Notification

KB_FINISH_CALLBACK: list[callable] = []

def add_app(app: Application):
    if not OS_LOADED:
        pass
    APPS.append(app)


def remove_app(name_or_screen: str):
    for app in APPS:
        if app.app_name == name_or_screen or app.app_screen == name_or_screen:
            APPS.remove(app)


def load():
    import applications as apcs
    globals.OS_LOADED = True
    # Loads the default apps
    settings_app = apcs.SettingsApplication()
    dice_roller_app = apcs.DiceApplication()
    add_app(settings_app)
    add_app(dice_roller_app)
    osui.refresh_lvgl_app_objects(APPS)

    asyncio.run(run_async_jobs())


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


async def clear_async_jobs():
    ASYNC_JOBS.clear()
    gc.enable()
    gc.collect()

async def schedule_async_job(job: AsyncJob, execute_now: bool = False):
    ASYNC_JOBS.append(job)
    if execute_now:
        job.execute()


def schedule_onetime_kb_callback(callback: callable):
    KB_FINISH_CALLBACK.append(callback)


def open_app(app: Application):
    from globals import get_focused_app, set_focused_app, no_focused_app
    print(f"Called open_app. Debug: {app.get_process_id()}, {app.get_name()}, {no_focused_app()}")
    close_app(get_focused_app())  # Close the current app if any
    set_focused_app(app)
    # print(f"Set Focused App: {get_focused_app()}")
    osui.update_main_screen()
    # print(f"Set Focused App: {get_focused_app()}")
    get_focused_app().run(osui.get_application_screen_container())
    # print(f"Set Focused App: {get_focused_app()}")


def is_keyboard_focused() -> bool:
    return osui.KB_FOCUSED


def revoke_keybaord():
    osui.set_keyboard_state(False)


def close_app(app: Application):
    if app is None:
        return

    from globals import set_focused_app, no_focused_app
    set_focused_app(None)

    if app:
        stop_async_jobs(app.get_process_id())
        osui.remove_lvgl_object_binding(app.get_process_id(), delete_lvgl_object=True, do_gc=True)

    osui.update_main_screen()
    print(f"Called close_app(). Debug: {app.get_process_id()}, {app.get_name()}, {no_focused_app()}")


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


def add_lvgl_object_binding(obj: any, identifier: str):
    osui.add_lvgl_object_binding(obj, identifier)


def get_lvgl_object_binding(identifier: str) -> LVGLToObjectBindings | None:
    return osui.get_lvgl_object_binding(identifier)


def remove_lvgl_object_binding(identifier: str, delete_lvgl_object: bool = True, do_gc: bool = False):
    osui.remove_lvgl_object_binding(identifier, delete_lvgl_object, do_gc)


def push_modal(modal: Modal):
    QUEUED_MODALS.append(modal)


def push_notif(notif: Notification):
    QUEUED_NOTIFICATIONS.append(notif)


def to_home():
    from globals import no_focused_app
    if not no_focused_app():
        close_app(globals.get_focused_app())
    osui.update_main_screen()


async def use_keyboard(init_text: str = "") -> str:
    osui.set_keyboard_content(init_text)
    osui.set_keyboard_state(True)
    while osui.KB_FOCUSED:
        await asyncio.sleep(0.1)
    return osui.get_keyboard_content()


def invoke_keyboard(init_text: str = "", callback: callable = None):
    osui.set_keyboard_content(init_text)
    osui.set_keyboard_state(True)


def get_keyboard_text() -> str:
    return osui.get_keyboard_content()


async def main():
    await osui.update() # Start OS-UI Async Updates
    asyncio.run(os_update())
    asyncio.run(gc_coroutine(60)) # Run a 60-second GC. Must use asyncio.run() to run in the background.

    # while True:
    #     # Handling above-OS-Level stuff here, e.g. Notifications, App launch requests, etc.
    #     await asyncio.sleep(0.1)