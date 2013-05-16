import os

class Mounter:
    def __init__(self):
        pass
    def mount(self, account):
        command_line = "fusedav"
        command_line += " -u " + account["login"]
        command_line += " -p " + account["passwd"]
        command_line += " " + account["path"]
        command_line += " " + account["mount_point"]
        print command_line
        os.system(command_line)
