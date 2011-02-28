'''
    Watcher Dbus
    
    Generates the required DBus signals
    
    Created on 2011-02-28

    @author: jldupont
'''
import dbus.service
    
from jld_scripts.system.base import AgentThreadedBase

__all__=[]


class SignalTx(dbus.service.Object):

    PATH="/Watcher"
    
    def __init__(self, agent):
        dbus.service.Object.__init__(self, dbus.SessionBus(), self.PATH)
        self.agent=agent
        
    @dbus.service.signal(dbus_interface="com.jldupont.watcher", signature="s")
    def PathChanged(self, path):
        pass


class DbusAgent(AgentThreadedBase):
    
    def __init__(self):
        AgentThreadedBase.__init__(self)

        self.stx=SignalTx(self)
        
    def h_path_changed(self, path):
        self.stx.PathChanged(path)
                   
_=DbusAgent()
_.start()
