"""
    squeezecenter_utils
        
    Created on 2010-10-21
    @author: jldupont
"""
#import os
import sys

APP_NAME="SqueezeCenter Utils"
ICON_NAME="squeezecenter.gif"
HELP_URL="http://www.systemical.com/doc/opensource/squeezecenter_utils"

###<<< DEVELOPMENT MODE SWITCHES
MSWITCH_OBSERVE_MODE=False
MSWITCH_DEBUGGING_MODE=False
MSWITCH_DEBUG_INTEREST=False
DEV_MODE=True
###>>>

import gobject
import dbus.glib
from dbus.mainloop.glib import DBusGMainLoop
import gtk



def main():
    try:
        gobject.threads_init()  #@UndefinedVariable
        dbus.glib.init_threads()
        DBusGMainLoop(set_as_default=True)
        
        from jld_scripts.system import base as base
        base.debug=DEV_MODE
        base.debug_interest=MSWITCH_DEBUG_INTEREST
        
        from jld_scripts.system import mswitch #@UnusedImport
        mswitch.observe_mode=MSWITCH_OBSERVE_MODE
        mswitch.debugging_mode=MSWITCH_DEBUGGING_MODE
        
        from jld_scripts.res import get_res_path
        icon_path=get_res_path()
        
        from jld_scripts.agents.tray import TrayAgent
        _ta=TrayAgent(APP_NAME, icon_path, ICON_NAME, HELP_URL)
        
        gtk.main()
        
    except Exception,e:
        from jld_scripts.agents.notifier import notify #@Reimport
        notify(APP_NAME, "There was an error: %s" % e)
        try:    gtk.main_quit()
        except: pass
        sys.exit(1)

