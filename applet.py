import gobject
import gtk
from add_service import AddServiceDialog
from settings import Settings 

class Applet:
    def saveNewAccount(self, service, sobject):
        print "SAVE", service
        self.accounts[service] = sobject
        self.settings.accounts = self.accounts
        self.addMenuItem(service, self.editMountPoint)
    def addMountPoint(self, w, buf):
        self.dialog = AddServiceDialog(self.saveNewAccount)
    def editMountPoint(self, w, buf):
        pass
    def quitSoftRaid(self, w, buf):
        exit(0)
    def addMenuItem(self, text, callback):
        menu_items = gtk.MenuItem(text)
        menu_items.connect("activate", callback, None)
        self.menu.append(menu_items)
        menu_items.show()
    def __init__(self):
        self.settings = Settings()
        self.accounts = self.settings.accounts
        
        # create a menu
        self.menu = gtk.Menu()

        self.addMenuItem("Add service", self.addMountPoint)
        self.addMenuItem("Quit SoftRaid", self.quitSoftRaid)
        for account_name in self.accounts:
            print "load ", account_name
            self.addMenuItem(account_name, self.editMountPoint)
