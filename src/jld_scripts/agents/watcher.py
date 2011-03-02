"""
    Watcher agent
    
    Created on 2011-02-28

    @author: jldupont
    
    NOTES:
    ------
    
    * a "moved" message with a "src=None" signifies that a file/dir was moved to the target path
    * a "moved" message with "src!=None" signifies that a file/dir changed name
    
    Messages Out:
    * "removed" : (not reliable at the moment - do not use)
    * "deleted"
    * "created"
    * "moved"   : 1) can be generated as a result of "rename" - beware as the path might not be available anymore soon
                  2) furthermore, when a directory is "moved out" of the "watched dir", no event is generated...  
    * "renamed" : when a path is renamed from 'src' to 'path'
    
"""
import os
import pyinotify

from jld_scripts.system.base import AgentThreadedBase
from jld_scripts.system.mswitch import publish as mswitch_publish

__all__=[]


class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CLOSE_WRITE(self, event):
        self._handle("modified_closed", event)        
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
        
        ## filter-out the "moved" that are actually
        ##  name changes where the event was the "from" notification alone
        if msg_type=="moved":
            if src is not None:
                src_exists=os.path.exists(path)
                if src_exists:
                    mswitch_publish("watcher", "renamed", path, symlink_path, src)
                    return
                else:
                    mswitch_publish("watcher", "removed", path, symlink_path)
                    return                    
                        
            mswitch_publish("watcher", "moved", path, symlink_path)
            return
            
        mswitch_publish("watcher", msg_type, path, symlink_path, src)


class WatcherAgent(AgentThreadedBase):

    WAIT_FOR_RETRY_CREATE_WATCHED_DIR=60 #seconds
    WATCHED_DIR="~/.watched"

    def __init__(self):
        AgentThreadedBase.__init__(self)
        self.watched_dir=os.path.expanduser(self.WATCHED_DIR)
        self._createWatchedDir()
        self.wait_count=None
        
        self.lmoved=[]
        
        self.wm = pyinotify.WatchManager()
        self.mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_TO | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_FROM
        self.notifier = pyinotify.Notifier(self.wm, default_proc_fun=EventHandler(), timeout=1000)
        
        self._addDir(self.watched_dir)
        
    def beforeQuit(self):
        self.notifier.stop()

### ======================================================================================================
    def h_modified_closed(self, path, symlink, *_):
        print "! modified_closed (%s) symlink(%s)" % (path, symlink)

    def h_modified(self, path, symlink, *_):
        print "! modified (%s) symlink(%s)" % (path, symlink)
        
    def h_created(self, path, symlink, *_):
        print "! created (%s) symlink(%s)" % (path, symlink)

    def h_deleted(self, path, symlink, *_):
        print "! deleted (%s) symlink(%s)" % (path, symlink)

    def h_moved(self, path, symlink):
        #print "! moved (%s) symlink(%s) src(%s) cookie(%s)" % (path, symlink, src, cookie)
        print "! moved (%s) symlink(%s)" % (path, symlink)

    def h_renamed(self, path, symlink, src):
        #print "! moved (%s) symlink(%s) src(%s) cookie(%s)" % (path, symlink, src, cookie)
        print "! renamed (%s) symlink(%s) src(%s)" % (path, symlink, src)

    def h_removed(self, path, symlink):
        #print "! moved (%s) symlink(%s) src(%s) cookie(%s)" % (path, symlink, src, cookie)
        print "! removed (%s) symlink(%s)" % (path, symlink)

### ======================================================================================================

    def _addSymlinkDir(self, path):
        """
        Handles the addition of a symlinked directory
        """


    def _addDir(self, path):
        """
        Returns 'wd' watch descriptor
        """
        return self.wm.add_watch(self.watched_dir, self.mask, rec=True, auto_add=True)
        
    def _rmDir(self, wd):
        """
        Returns 'wd' dictionary
        """
        return self.wm.rm_watch(wd, rec=True, quiet=True)
        
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
