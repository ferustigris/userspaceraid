import gobject
import gtk
from add_service import AddServiceDialog
from settings import Settings 

class Applet:
    def saveNewAccount(self, service, sobject):
        print "SAVE", service
        self.accounts[service] = sobject
        self.settings.accounts = self.accounts
        self._addMenuItem(service, self.editAccount)
    def addNewAccount(self, w, buf):
        self._dialog = AddServiceDialog(self.saveNewAccount)
    def editAccount(self, w, buf):
        pass
    def quitSoftRaid(self, w, buf):
        exit(0)
    def _addMenuItem(self, text, callback):
        menu_items = gtk.MenuItem(text)
        menu_items.connect("activate", callback, None)
        self.menu.append(menu_items)
        menu_items.show()
    def __init__(self):
        self.settings = Settings()
        self.accounts = self.settings.accounts
        
        # create a menu
        self.menu = gtk.Menu()

        self._addMenuItem("Add service", self.addNewAccount)
        self._addMenuItem("Quit SoftRaid", self.quitSoftRaid)
        for account_name in self.accounts:
            print "load ", account_name
            self._addMenuItem(account_name, self.editAccount)
