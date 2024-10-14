import asyncio
from abc import abstractmethod
from asyncio import Future

import micropython
import ujson

LIB_VER: str = "0.0.0"
OS_VER: str = "0.0.0"

def get_os_version() -> str:
    return OS_VER

def get_library_version() -> str:
    return LIB_VER


from typing import TypeVar, Generic, Type

T = TypeVar('T', bound='IEncodable')

class DataManager(Generic[T]):
    def __init__(self, cls: Type[T], file_name: str = "data.json"):
        self.cls = cls
        self.file_name = file_name
        self.content: T = self.load()

    def load(self) -> T:
        try:
            with open(self.file_name, 'r') as f:
                data = f.read()
                obj = self.cls()
                obj.decode(data)
                return obj
        except Exception as e:
            print(f'Exception occurred while loading the file: {e}')
            return self.cls()

    def save(self):
        if self.content:
            with open(self.file_name, 'w') as f:
                f.write(self.content.encode())

    def get(self) -> T:
        return self.content

    def set(self, content: T):
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
        return f"app_{self.__hash__()}"

    @abstractmethod
    async def run(self, container: any):
        pass


class IEncodable:
    def encode(self) -> str:
        return ujson.dumps(self.__dict__)

    def decode(self, data: str):
        self.__dict__ = ujson.loads(data)


class ConfigSetting(IEncodable):
    def __init__(self, setting_name: str, setting_description: str, default_value: any = None):
        self.setting_name = setting_name
        self.setting_description = setting_description
        self.setting_value = default_value


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


class OSConfigManager(DataManager[Config]):
    def __init__(self, config_name: str = "sys_conf.json"):
        super().__init__(Config, config_name)

    def change(self, value: any, save: bool = False, *keys):
        if self.content is not None:
            current = self.content
            for arg in keys[:-1]:
                current = getattr(current, arg)
            setattr(current, keys[-1], value)
            if save:
                self.save()


class LVGLToObjectBindings:
    def __init__(self, obj: any, identifier: str):
        self.obj = obj
        self.identifier = identifier

    def get(self) -> any:
        return self.obj


class Modal:
    def __init__(self, title: str, message: str, buttons: list[str], callbacks=None):
        if callbacks is None:
            self.callbacks: list[callable] = []
        else:
            self.callbacks = callbacks
        self.title = title
        self.message = message
        self.buttons = buttons


class Notification:
    def __init__(self, title: str, message: str, duration: int = 3, click_callback: callable = None):
        self.title = title
        self.message = message
        self.click_callback = click_callback
        self.duration = duration


def notif_identifier_hash(obj: Notification) -> str:
    return f"notification-{obj.__hash__()}"