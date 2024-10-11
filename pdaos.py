import gc

import globals
import osui
import asyncio

from globals import APPS, FOCUSED_APP, OS_LOADED, ASYNC_JOBS
from pdaos_lib import Application, AsyncJob


def has_focused_app() -> bool:
    return FOCUSED_APP is not None


def add_app(app: Application):
    if not OS_LOADED:
        pass
    APPS.append(app)


def remove_app(name_or_screen: str):
    for app in APPS:
        if app.app_name == name_or_screen or app.app_screen == name_or_screen:
            APPS.remove(app)


def load():
    globals.OS_LOADED = True
    # Loads the default apps
    settings_app = Application("Settings", "ST", "settings", 0x2B2B2B)
    dice_roller_app = Application("Dices", "DC", "dices", 0xE4080A)
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
    close_app(globals.FOCUSED_APP)  # Close the current app if any
    globals.FOCUSED_APP = app
    # Load the app's initialization
    # TODO New class-based object impl.
    # if app.app_tick:
    #     app.task = asyncio.create_task(app_runner(app))
    # if app.app_second:
    #     asyncio.create_task(app_second_runner(app))
    # Load App UI
    osui.load_app_ui(app)


def close_app(app: Application):
    if app:
        # Remove its update from the async pool
        if app.task:
            app.task.cancel()
        # Remove its UI from the screen
        osui.unload_app_ui(app)
        # Clear cache (implement cache clearing logic if needed)
        # Switch to the main screen
        osui.switch_to_main_screen()
        globals.FOCUSED_APP = None


async def os_update():
    """
    OS-Level Async Updates.
    """
    while True:
        # Perform any OS-level updates here
        # For example, update the time display, check battery status, etc.
        await osui.update() # UI Update Thread


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