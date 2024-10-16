import asyncio
import typing
import json

LIB_VER: str = "0.0.0"
OS_VER: str = "0.0.0"

def get_os_version() -> str:
    return OS_VER

def get_library_version() -> str:
    return LIB_VER


# from typing import TypeVar, Generic, Type

# T = TypeVar('T', bound='IEncodable')

class DataManager:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.content: any = self.load()

    def load(self) -> any:
        try:
            with open(self.file_name, 'r') as f:
                data = f.read()
                return json.loads(data)
        except Exception as e:
            print(f'Exception occurred while loading the file: {e}')
            return None

    def save(self):
        if self.content:
            with open(self.file_name, 'w') as f:
                f.write(json.dumps(self.content))

    def get(self) -> any:
        return self.content

    def set(self, content: any):
        self.content = content
        self.save()


class AsyncJob:
    def __init__(self, job_id: str, job: callable):
        self.job_id = job_id
        self.job = job
        self.task: asyncio.Task = None

    def is_running(self) -> bool:
        """
        Checks if the task is currently running.
        :return: True if the task is running, otherwise False.
        """
        return self.task is not None

    def execute(self):
        """
        Executes the given coroutine job asynchronously.
        """
        if self.is_running():
            print("Task is already running.")
            pass

        async def thread_task():
            await self.create_task()

        try:
            asyncio.run(thread_task())
        except Exception as e:
            print("Task is cancelled or has encountered an error: ", e)

    def create_task(self):
        """
        Creates a new task for the job.
        :return: The Task object.
        """
        if self.is_running():
            print("Warning: There is a duplicated task. There will be potential conflicts between two tasks.")

        self.task = asyncio.create_task(self.job())
        return self.task

    def cancel(self, msg: str | None = None):
        """
        Cancels the running task.
        :param msg: The message for cancelling the task.
        """
        self.task.cancel(msg)
        del self.task
        self.task = None


class Application:
    def __init__(self, name: str = "Untitled App", icon: str = "??", screen: str = "untitled_screen", color: int = 0x5385ED):
        self.app_name = name
        self.app_icon = icon
        self.app_screen = screen
        self.app_color = color

    def get_name(self):
        return self.app_name

    def get_icon(self):
        return self.app_icon

    def get_screen(self):
        return self.app_screen

    def get_color(self):
        return self.app_color

    def get_process_id(self):
        return f"app_{id(self)}"

    def run(self, container: any):
        pass


class IEncodable:
    def encode(self) -> str:
        return json.dumps(self.__dict__)

    def decode(self, data: str):
        self.__dict__ = json.loads(data)


class IIdentifiable:
    def identifier(self) -> str:
        pass

    def find(self) -> any:
        pass


class ConfigTypes:
    TOGGLE = "toggle"
    VALUE = "value"
    SLIDER = "slider"
    DROPDOWN = "dropdown"
    ACTION = "action"


class ConfigSetting(IEncodable):
    def __init__(self, setting_name: str, setting_description: str, default_value: any, option_type: str):
        self.setting_name = setting_name
        self.setting_description = setting_description
        self.setting_value = default_value
        self.option_type = option_type
        # Allowed option types: "toggle" | "value" | "slider" | "dropdown" | "action"


class ConfigCategory(IEncodable):
    def __init__(self, category_name: str, category_description: str, category_items: list[ConfigSetting]):
        self.category_name = category_name
        self.category_description = category_description
        self.category_items = category_items


class Config(IEncodable):
    def __init__(self, config_name: str, config_semver: str, config_categories: list[ConfigCategory]):
        self.config_name = config_name
        self.config_semver = config_semver
        self.config_categories = config_categories


class LVGLToObjectBindings:
    def __init__(self, obj: any, identifier: str):
        self.obj = obj
        self.identifier = identifier

    def get(self) -> any:
        return self.obj


class Modal(IIdentifiable):
    def __init__(self, title: str, message: str, buttons: list[str], callbacks=None):
        if callbacks is None:
            self.callbacks: list[callable] = []
        else:
            self.callbacks = callbacks
        self.title = title
        self.message = message
        self.buttons = buttons

    def identifier(self):
        return f"modal-{id(self)}"


class Notification(IIdentifiable):
    def __init__(self, title: str, message: str, duration: int = 3, click_callback: callable = None):
        self.title = title
        self.message = message
        self.click_callback = click_callback
        self.duration = duration

    def identifier(self):
        return f"notification-{id(self)}"


def notif_identifier_hash(obj: Notification) -> str:
    return f"notification-{id(obj)}"