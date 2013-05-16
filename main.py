#!/usr/bin/python
# -*- coding: utf-8 -*-

import appindicator
from applet import Applet 
import gtk
from mounter import Mounter


if __name__ == "__main__":
    ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status (appindicator.STATUS_ACTIVE)
    ind.set_attention_icon ("indicator-messages-new")	

    mounter = Mounter()

    applet = Applet(mounter)
    ind.set_menu(applet.menu)

    gtk.main()

