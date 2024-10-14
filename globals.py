from pdaos_lib import Application, AsyncJob, Modal, Notification

APPS: list[Application] = []
FOCUSED_APP: Application | None = None
OS_LOADED: bool = False
ASYNC_JOBS: list[AsyncJob] = []
QUEUED_MODALS: list[Modal] = []
QUEUED_NOTIFICATIONS: list[Notification] = []
TEMP_VARIABLES: dict[str, any] = {}

def get_app_by_name(name: str) -> Application | None:
    for app in APPS:
        if app.app_name == name:
            return app
    return None

def get_focused_app():
    global FOCUSED_APP
    return FOCUSED_APP

def set_focused_app(app: Application | None):
    global FOCUSED_APP
    FOCUSED_APP = app

def no_focused_app():
    global FOCUSED_APP
    return FOCUSED_APP is None

def set_temp_variable(key: str, value: any):
    TEMP_VARIABLES[key] = value

def get_temp_variable(key: str) -> any:
    return TEMP_VARIABLES.get(key)

def remove_temp_variable(key: str):
    TEMP_VARIABLES.pop(key, None)