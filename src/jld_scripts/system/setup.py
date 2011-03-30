'''
Created on 2011-03-30

@author: jldupont
'''
import gobject
import dbus.glib
from dbus.mainloop.glib import DBusGMainLoop

gobject.threads_init()  #@UndefinedVariable
dbus.glib.init_threads()
DBusGMainLoop(set_as_default=True)
