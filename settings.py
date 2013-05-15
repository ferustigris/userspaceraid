import os

class Settings:
    settings_path = '~/.config/userraid.ini'
    def __init__(self):
        try:
            f = open(self.settings_path, 'rb')
            self.__dict__ = eval(f.read())
            f.close()
        except (IOError, SyntaxError), (code, descr):
            os.path.exists(u'~/.config') or os.makedirs(u'~/.config')
            # default settings
            self.__dict__ = {
                                'name': u'Charles',
                                'second_name': u'Chaplin'
                            }

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        try:
            f = open(self.settings_path, 'wb')
            f.write(repr(self.__dict__))
            f.close()
        except IOError, (code, descr):
            pass
