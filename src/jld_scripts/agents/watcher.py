"""
    Watcher agent
    
    Created on 2011-02-28

    @author: jldupont
"""
import os
import pyinotify

from jld_scripts.system.base import AgentThreadedBase
from jld_scripts.system.mswitch import publish as mswitch_publish

__all__=[]


class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CLOSE_WRITE(self, event):
        self._handle("modified", event)        
        #print "Close Write:", event.pathname
    
    def process_IN_CREATE(self, event):
        self._handle("created", event)
        #print "Creating:", event.pathname


    def process_IN_DELETE(self, event):
        """
        NOTE: only called when actually deleted i.e. not moved to Trash
        """
        self._handle("deleted", event)
        #print "Removing:", event.pathname

    def process_IN_MODIFY(self, event):
        self._handle("modified", event)
        #print "Modifying:", event.pathname

    def process_IN_MOVED_FROM(self, event):
        """
        Indicates from which file path a file was moved from
        
        NOTE: not reliable as 'src_pathname' isn't always present
        
        'src_pathname': the 'from'
        'pathname': the 'to'
        
        """
        self._handle("moved", event)        
        #print "MOVED FROM, STAT:", os.stat(event.pathname)
        

    def process_IN_MOVED_TO(self, event):
        """
        Indicates the 'from' & 'to'
        
        'pathname'
        
        NOTE: not reliable
        """
        self._handle("moved", event)
        #print "MOVED TO, STAT:", os.stat(event.pathname)
    
    def _handle(self, msg_type, event):
        path=event.pathname
        src=event.__dict__.get("src_pathname", None) if msg_type=="moved" else None
        symlink=os.path.islink(path)
        symlink_path=os.readlink(path) if symlink else None
        mswitch_publish("watcher", msg_type, path, symlink_path, src)


class WatcherAgent(AgentThreadedBase):

    WAIT_FOR_RETRY_CREATE_WATCHED_DIR=60 #seconds
    WATCHED_DIR="~/.watched"

    def __init__(self):
        AgentThreadedBase.__init__(self)
        self.watched_dir=os.path.expanduser(self.WATCHED_DIR)
        self._createWatchedDir()
        self.wait_count=None
        
        self.wm = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_TO | pyinotify.IN_CLOSE_WRITE #| pyinotify.ALL_EVENTS # | pyinotify.IN_MOVED_TO
        self.notifier = pyinotify.Notifier(self.wm, default_proc_fun=EventHandler(), timeout=1000)
        
        self.wdd = self.wm.add_watch(self.watched_dir, mask, rec=True, auto_add=True, do_glob=True)
        
    def beforeQuit(self):
        self.notifier.stop()
        
    def h_created(self, path, symlink, *_):
        print "! created (%s) symlink(%s)" % (path, symlink)

    def h_deleted(self, path, symlink, *_):
        print "! deleted (%s) symlink(%s)" % (path, symlink)

    def h_moved(self, path, symlink, src):
        print "! moved (%s) symlink(%s) src(%s)" % (path, symlink, src)

        
    def h___tick__(self, *_):
        """
        Attempts to create the 'watched dir' if instructed to
        """
        if self.notifier.check_events():
            self.notifier.read_events()
            self.notifier.process_events()
        
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
