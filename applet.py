import gobject
import gtk
from add_service import AddServiceDialog
from settings import Settings 

class Applet:
    accounts = {}
    settings = Settings()
    def saveNewAccount(self, service, sobject):
        print "SAVE", service
        self.accounts[service] = sobject
        self.settings.accounts = self.accounts
        exit(0)
    def addMountPoint(self, w, buf):
        self.dialog = AddServiceDialog(self.saveNewAccount)
    def editMountPoint(self, w, buf):
        pass
    def quitSoftRaid(self, w, buf):
        exit(0)
    def __init__(self):
        accounts = self.settings.accounts
        
        # create a menu
        menu = gtk.Menu()

        menu_items = gtk.MenuItem("Add service")
        menu_items.connect("activate", self.addMountPoint, None)
        menu.append(menu_items)
        menu_items.show()
        # create some
        for account_name in accounts:
            menu_items = gtk.MenuItem(account_name)
            menu_items.connect("activate", self.editMountPoint, None)
            menu.append(menu_items) 
            menu_items.show()

        menu_items = gtk.MenuItem("Quit SoftRaid")
        menu_items.connect("activate", self.quitSoftRaid, None)
        menu.append(menu_items)
        menu_items.show()
        self.menu = menu
