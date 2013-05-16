import gobject
import gtk
from add_service import AddServiceDialog
from settings import Settings 

class Applet:
    def saveNewAccount(self, service, account_object):
        print "SAVE", service
        self.accounts[service] = account_object
        self.settings.accounts = self.accounts

        self._addMenuItem(service, self.editAccount)
        
        self.addNewServices(account_object)
        self.mounter.mount(account_object)
    def addNewServices(self, service_object):
        service_name = service_object["service"]
        if not service_name in self.services:
            self.services[service_name] = {
                "path": service_object["path"]
            }
            self.settings.services = self.services
    def addNewAccount(self, w, buf):
        self._dialog = AddServiceDialog(self.services, self.saveNewAccount)
    def editAccount(self, w, buf):
        pass
    def quitSoftRaid(self, w, buf):
        exit(0)
    def _addMenuItem(self, text, callback):
        menu_items = gtk.MenuItem(text)
        menu_items.connect("activate", callback, None)
        self.menu.append(menu_items)
        menu_items.show()
    def __init__(self, mounter):
        self.mounter = mounter

        self.settings = Settings()
        self.accounts = self.settings.accounts
        self.services = self.settings.services

        # create a menu
        self.menu = gtk.Menu()

        self._addMenuItem("Add service", self.addNewAccount)
        self._addMenuItem("Quit SoftRaid", self.quitSoftRaid)
        for account_name in self.accounts:
            print "load ", account_name
            mounter.mount(self.accounts[account_name])
            self._addMenuItem(account_name, self.editAccount)
