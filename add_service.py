#!/usr/bin/python
# -*- coding: utf-8 -*-

import gobject
import gtk

class AddServiceDialog:
    def __init__(self, services, save_callback):
        self.save_callback = save_callback
        self.services = services

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL);
        self.window.set_position(gtk.WIN_POS_CENTER);
        self.window.show()
        
        layout = gtk.VBox()
        self.window.add(layout)
        layout.show()

        self.combo = gtk.Combo()
        slist = []
        for service in self.services:
            slist.append(service)
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
        path = self.combo.entry.get_text()
        service_name = self.combo.entry.get_text()
        if service_name in self.services:
            service = self.services[service_name]
            path = service["path"]
        account_object = {
            "service": service_name,
            "path": path,
            "mount_point": "/home/asd/raid",
            "login": self.username.get_text(),
            "passwd": self.password.get_text()
        }
        self.save_callback(service_name + ": " + self.username.get_text(), account_object)
        self.window.hide()
