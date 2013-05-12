#!/usr/bin/python
# -*- coding: utf-8 -*-

import gobject
import gtk
import appindicator
from AddMountPoint import * 

accounts = {
	"a-slash2003@yandex.ru" : {
		"service": "yandex",
		"login": "a-slash2003@yandex.ru",
		"passwd": "rvclrvcl",
	},
	"ferus.tigris@yandex.ru" : {
		"service": "yandex",
		"login": "ferus.tigris@yandex.ru",
		"passwd": "rvclrvcl",
	},
	"ferus.tigris@gmail.com" : {
		"service": "dropbox",
		"login": "ferus.tigris@gmail.com",
		"passwd": "0000000",
	}
}

def addMountPoint(w, buf):
	addMountPoint = AddMountPoint();

if __name__ == "__main__":
	ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
	ind.set_status (appindicator.STATUS_ACTIVE)
	ind.set_attention_icon ("indicator-messages-new")
		# create a menu
	menu = gtk.Menu()
		# create some
	for account_name in accounts:
		account = accounts[account_name];
		buf = account["service"] + ": " + account["login"]
		menu_items = gtk.MenuItem(buf)
		menu_items.connect("activate", addMountPoint, None)
		menu.append(menu_items)
		menu_items.show()
	ind.set_menu(menu)
	gtk.main()

