from pdaos_lib import Application, AsyncJob

APPS: list[Application] = []
FOCUSED_APP: Application | None = None
OS_LOADED: bool = False
ASYNC_JOBS: list[AsyncJob] = []
