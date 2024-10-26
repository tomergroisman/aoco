from aoco.app import App
from aoco.cmd import Cmd
from aoco.constants import STORAGE_FILENAME
from aoco.services.storage import StorageService


storage_service = StorageService(STORAGE_FILENAME)

cmd = Cmd(storage_service=storage_service)
app = App(cmd=cmd)
app.start()
