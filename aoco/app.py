from aoco.cmd import Cmd


class App:
    def __init__(self, cmd: Cmd):
        self.cmd = cmd

    def start(self):
        print("start")
        self.cmd.verify_initialization()
        self.cmd.select_day()
