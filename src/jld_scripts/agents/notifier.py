"""
    Notifier Agent - Display notifications to the user
    
    Used to in situations when the user can act to correct a situation
    
    Uses 'pynotify' (desktop notification) to message
    the user in case of 'warning' and 'error' level log entries

    Messages Processed:
    ===================
    - "notify"
    - "logged"
    
    14Feb2011: added "urgency" level
    
    @author: jldupont
    Created on Jun 28, 2010
"""
try:
    import pynotify
except:
    pass

from jld_scripts.system.base import AgentThreadedBase

__all__=["NotifierAgent", "notify"]


def notify(app_name, msg, icon_name="important", urgency=pynotify.URGENCY_CRITICAL):
    try:
        pynotify.init(app_name)
        n=pynotify.Notification(app_name, msg, icon_name)
        n.set_urgency(urgency)
        n.show()
        return n
    except:
        print "%s: %s" % (app_name, msg)


class NotifierAgent(AgentThreadedBase):
    
    UMAP = { "normal":  pynotify.URGENCY_NORMAL
            ,"low":     pynotify.URGENCY_LOW
            ,"high":    pynotify.URGENCY_CRITICAL
            }
    
    def __init__(self, app_name, icon_name):
        AgentThreadedBase.__init__(self)
        self.app_name=app_name
        self.icon_name=icon_name
        pynotify.init(app_name)        

        self.types=["w", "e", "warning", "error"]
        
    def h_notify(self, msg, urgency=None):
        '''
        Direct access to the notification facility
        '''
        n=pynotify.Notification(self.app_name, msg, self.icon_name)
        if urgency is not None:
            n.set_urgency(self.UMAP.get(urgency, pynotify.URGENCY_NORMAL))
        n.show()
        
        
    def h_logged(self, _logtype, loglevel, msg):
        #print "Notifier.h_logged, logtype(%s)" % logtype
        if loglevel in self.types:
            
            n=pynotify.Notification(self.app_name, msg, self.icon_name)
            n.set_urgency(pynotify.URGENCY_CRITICAL)
            n.show()

## Usage           
"""
_=NotifierAgent(APP_NAME, ICON_NAME)
_.start()
"""        

if __name__=="__main__":
    notify("test", "test message!")
    