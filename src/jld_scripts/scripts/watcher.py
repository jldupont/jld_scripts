"""
    Watcher
        
    @created: 28 Feb 2011
    @author: jldupont
"""
import sys

APP_NAME="watcher Utils"
ICON_NAME="watcher.png"
HELP_URL="http://www.systemical.com/doc/opensource/watcher"
TIME_BASE=5000

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

gobject.threads_init()  #@UndefinedVariable
dbus.glib.init_threads()
DBusGMainLoop(set_as_default=True)

from jld_scripts.system import base as base
base.debug=DEV_MODE
base.debug_interest=MSWITCH_DEBUG_INTEREST

from jld_scripts.system import mswitch #@UnusedImport
mswitch.observe_mode=MSWITCH_OBSERVE_MODE
mswitch.debugging_mode=MSWITCH_DEBUGGING_MODE

from jld_scripts.agents.notifier import notify, NotifierAgent #@Reimport
from jld_scripts.agents.clock import Clock #@Reimport

def main():
    try:
        
        try:    
            import pyinotify #@UnresolvedImport @UnusedImport
        except: 
            raise Exception("package 'pyinotify' is required")
        
        from jld_scripts.res import get_res_path
        icon_path=get_res_path()
        
        from jld_scripts.agents.tray import TrayAgent
        _ta=TrayAgent(APP_NAME, icon_path, ICON_NAME, HELP_URL)

        import jld_scripts.agents.watcher_dbus #@UnusedImport
        import jld_scripts.agents.watcher #@UnusedImport
        
        _na=NotifierAgent(APP_NAME, ICON_NAME)
        _na.start()
        
        clk=Clock(TIME_BASE)
        gobject.timeout_add(TIME_BASE, clk.tick)
        
        gtk.main()
        
    except KeyboardInterrupt:
        mswitch.quit()
        try:    gtk.main_quit()
        except: pass
        
    except Exception,e:
        notify(APP_NAME, "There was an error: %s" % e)
        mswitch.quit()
        sys.exit(1)

