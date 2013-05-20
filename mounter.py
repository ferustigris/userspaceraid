import os
import urllib
import popen2
import signal

class Mounter:
    pids = []

    def __init__(self):
        pass

    def __del__(self):
        self.umount_all()

    def mount(self, settings, account):
        if not 'mount_point' in account:
            dir = account["path"] + account['login']
            account['mount_point'] = os.path.join(settings.workdir, dir)

        mount_point = urllib.quote(account['mount_point'])
        os.path.exists(mount_point) or os.makedirs(mount_point)

        mount = popen2.Popen3([
            "fusedav",
            "-u", account["login"],
            "-p", account["passwd"],
            account["path"],
            mount_point
        ])
        self.pids.append(mount.pid)
        print "pid=", mount.pid

    def umount_all(self):
        for pid in self.pids:
            print "pid=", pid
            os.kill(pid, signal.SIGTERM) or os.kill(pid, signal.SIGKILL)
        self.pids = []
