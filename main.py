#!/usr/bin/python
# -*- coding: utf-8 -*-

import appindicator
from applet import Applet 
from settings import Settings 
import gtk


if __name__ == "__main__":
    ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status (appindicator.STATUS_ACTIVE)
    ind.set_attention_icon ("indicator-messages-new")	
    applet = Applet()
    ind.set_menu(applet.menu)

    gtk.main()

