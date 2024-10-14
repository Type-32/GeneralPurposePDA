from pdaos_lib import Application, AsyncJob, Modal, Notification

APPS: list[Application] = []
FOCUSED_APP: Application | None = None
OS_LOADED: bool = False
ASYNC_JOBS: list[AsyncJob] = []
QUEUED_MODALS: list[Modal] = []
QUEUED_NOTIFICATIONS: list[Notification] = []
