from pdaos_lib import Application, AsyncJob, Modal, Notification

APPS: list[Application] = []
FOCUSED_APP: Application | None = None
OS_LOADED: bool = False
ASYNC_JOBS: list[AsyncJob] = []
QUEUED_MODALS: list[Modal] = []
QUEUED_NOTIFICATIONS: list[Notification] = []
TEMP_VARIABLES: dict[str, any] = {}
SIGNATURE_METHODS: dict[str, callable] = {}

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

def set_signature_method(key: str, method: callable):
    SIGNATURE_METHODS[key] = method

def get_signature_method(key: str) -> callable:
    return SIGNATURE_METHODS.get(key)

def remove_signature_method(key: str):
    SIGNATURE_METHODS.pop(key, None)