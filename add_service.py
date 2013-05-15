#!/usr/bin/python
# -*- coding: utf-8 -*-

import gobject
import gtk

class AddServiceDialog:
    def __init__(self, save_callback):
        self.save_callback = save_callback

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL);
        self.window.set_position(gtk.WIN_POS_CENTER);
        self.window.show()
        
        layout = gtk.VBox()
        self.window.add(layout)
        layout.show()

        self.combo = gtk.Combo()
        slist = [ "Ya.disk", "DropBox"]
        self.combo.set_popdown_strings(slist)
        self.combo.show()
        layout.add(self.combo)

        self.username = gtk.Entry(max=0)
        self.username.set_text('username')
        self.username.set_editable(True)
        self.username.show()
        layout.add(self.username)

        self.password = gtk.Entry(max=0)
        self.password.set_text('password')
        self.password.set_editable(True)
        self.password.show()
        layout.add(self.password)

        button_ok = gtk.Button('Add service')
        button_ok.show()
        button_ok.connect("clicked", self.save, None)
        layout.add(button_ok)
    def save(self, w, buf):
        path = ''
        service = self.combo.entry.get_text() + ": " + self.username.get_text()
        if service == "Ya.disk":
            path = 'https://webdav.yandex.ru'
        else:
            path = 'https://dav.dropdav.com'
        sobject = {
            "service": service,
            "path": path,
            "login": self.username.get_text(),
            "passwd": self.password.get_text()
        }
        self.save_callback(service, sobject)
        self.window.hide()
