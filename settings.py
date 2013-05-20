import os

class Settings:
    def __init__(self):
        homedir = os.environ['HOME']
        configdir = os.path.join(homedir, '.config')
        settings_path = os.path.join(configdir, 'userraid.ini')
        try:
            f = open(settings_path, 'rb')
            self.__dict__ = eval(f.read())
            f.close()
        except (IOError, SyntaxError), (code, descr):
            os.path.exists(configdir) or os.makedirs(configdir)
            # default settings
            self.__dict__ = {
                "services": {
                    "Ya.disk": {
                        "path": "https://webdav.yandex.ru"
                    },
                    "Dropbox": {
                        "path": "https://dav.dropdav.com"
                    }
                },
                "accounts": {}
            }
        self.settings_path = settings_path
        self.workdir = os.path.join(homedir, '.useraid')

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        try:
            f = open(self.settings_path, 'wb')
            f.write(repr(self.__dict__))
            f.close()
        except IOError, (code, descr):
            pass
