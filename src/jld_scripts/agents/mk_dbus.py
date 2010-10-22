"""
    MediaKeys Dbus Agent
    
    Messages Generated:
    - "mk_key_press"
    
    Created on 2010-10-22
    @author: jldupont
"""
import dbus.service
print dbus.__file__
    
from jld_scripts.system.base import AgentThreadedBase
from jld_scripts.system import mswitch

__all__=[]


class MKSignalRx(dbus.service.Object):

    PATH=None
    
    def __init__(self, agent):
        dbus.service.Object.__init__(self, dbus.SystemBus(), self.PATH) ## not sure we need this just to receive signals...
        self.agent=agent
        
        dbus.SystemBus().add_signal_receiver(self.sCondition,
                                       signal_name="Condition",
                                       dbus_interface="org.freedesktop.Hal.Device",
                                       bus_name=None,
                                       path=None
                                       )            
    def sCondition(self, *p):
        """
        DBus signal handler
        """
        if len(p) == 2:
            if (p[0]=="ButtonPressed"):
                mswitch.publish(self.agent, "mk_key_press", p[1])



class DbusAgent(AgentThreadedBase):
    
    def __init__(self):
        AgentThreadedBase.__init__(self)

        self.srx=MKSignalRx(self)
                   
_=DbusAgent()
_.start()
