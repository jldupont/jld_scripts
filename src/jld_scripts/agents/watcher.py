"""
    Watcher agent
    
    Created on 2011-02-28

    @author: jldupont
"""
import os
import pyinotify

from jld_scripts.system.base import AgentThreadedBase

__all__=[]


class EventHandler(pyinotify.ProcessEvent):
    
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname

    def process_IN_MODIFY(self, event):
        print "Modifying:", event.pathname

    def process_IN_MOVED_FROM(self, event):
        """
        Indicates from which file path a file was moved from
        
        'name' : the 'from', just file name
        'pathname': the 'from' with complete path
        'path': the base path of the file
        
        NOT THAT USEFUL given 'IN_MOVED_TO'
        """
        print "> MOVED_FROM: filepath(%s)" % event.pathname
        

    def process_IN_MOVED_TO(self, event):
        """
        Indicates the 'from' & 'to'
        
        'src_pathname': the 'from'
        'pathname'  : the 'to'
        """
        print "> MOVED src(%s) TO dst(%s) " % (event.src_pathname, event.pathname)


class WatcherAgent(AgentThreadedBase):

    WAIT_FOR_RETRY_CREATE_WATCHED_DIR=60 #seconds
    WATCHED_DIR="~/.watched"

    def __init__(self):
        AgentThreadedBase.__init__(self)
        self.watched_dir=os.path.expanduser(self.WATCHED_DIR)
        self._createWatchedDir()
        self.wait_count=None
        
        self.wm = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_TO 
        self.notifier = pyinotify.ThreadedNotifier(self.wm, EventHandler())
        self.notifier.start()
        
        self.wdd = self.wm.add_watch(self.watched_dir, mask, rec=True, auto_add=True)
        
    def beforeQuit(self):
        self.notifier.stop()
        
    def h___tick__(self, *_):
        """
        Attempts to create the 'watched dir' if instructed to
        """
        if (self.wait_count is None):
            return
        self.wait_count-=1
        if (self.wait_count<=0):
            self._createWatchedDir()
        
    
    def _createWatchedDir(self):
        """
        if the 'watched' directory doesn't already exist
        """
        try:
            os.mkdir(self.watched_dir, 0700)
        except:
            pass
        
        
        
        
## Usage           
_=WatcherAgent()
_.start()
