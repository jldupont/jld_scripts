"""
    'Squeeze' Agent - controls Squeezebox Center
    
    Messages Processed:
    ===================
    - "mk_key_press"
    
    
    @author: jldupont
    Created on Oct 22, 2010
    
    TODO add notification when Player is not found?
"""
from jld_scripts.system.base import AgentThreadedBase

from pysqueezecenter.server import Server
from pysqueezecenter.player import Player

__all__=["SqueezeAgent"]

class SqueezeAgent(AgentThreadedBase):

    MAP={
            "mute":             "key_mute"
            ,"stop-cd":         "key_stop"
            ,"stop":            "key_stop"
            ,"next-song":       "key_next"
            ,"next":            "key_next"
            ,"previous-song":   "key_previous"
            ,"previous":        "key_previous"
            ,"play-pause":      "key_play"
            ,"play":            "key_play"
            ,"volume-up":       "key_volume_up"
            ,"volume-down":     "key_volume_down"
         }
    
    def __init__(self):
        AgentThreadedBase.__init__(self)
        self.cArtist=""
        self.cAlbum=""
        self.cTitle=""
        self._reconnect()
        self.current_source=(None, None)
        self.ignore=[]
        self.mode_sound_only=False
        self.debug=False
        
    def h___tick__(self, *_):
        if self.player is None:
            self._reconnect()
            
        self.announce()
        
    def announce(self):
        try:
            cArtist=self.player.get_track_artist()
            cAlbum=self.player.get_track_album()
            cTitle=self.player.get_track_current_title()
            tPath=self.player.get_track_path()
            
            if cArtist!=self.cArtist or cAlbum!=self.cAlbum or cTitle!=self.cTitle:
                self.pub("notify", "Artist: %s \nAlbum: %s\nTitle: %s " % (cArtist, cAlbum, cTitle))
                self.pub("track", cArtist, cAlbum, cTitle, tPath)
                self.cArtist=cArtist
                self.cAlbum=cAlbum
                self.cTitle=cTitle
        except:
            pass
        
        
    def _reconnect(self):
        try:
            self.sc = Server(hostname="127.0.0.1", port=9090)
            self.sc.connect()
            
            self.players = self.sc.get_players()
            self.player=self.players[0]
        except:
            self.player=None

        
    def h_mk_key_press(self, key, source, priority):
        """ 
        Direct access to the notification facility
        """
        if self.player is None:
            self._reconnect()
            
        ## we tried...
        if self.player is None:
            return
        
        if (source in self.ignore):
            return
        
        name, prio=self.current_source
        if name is not None:
            if (priority < prio):
                self.ignore.append(source)
                #print "* ignoring source: %s" % source
                return
        self.current_source=(source, priority)
            
        #print "> source: %s key: %s" % (source, key)
        
        #dispatch_name="key_%s" % key.replace("-", "_")
        dispatch_name=self.MAP.get(key, "not_found")
        try:    getattr(self, dispatch_name)()
        except:
            print "* not found: %s" % key
        
    def key_mute(self):
        self.player.set_muting( not self.player.get_muting() )
        
    def key_stop(self):
        if not self.mode_sound_only:
            self.player.stop()
            self.announce()
        
    def key_next(self):
        if not self.mode_sound_only:
            self.player.next()
            self.announce()
        
    def key_previous(self):
        if not self.mode_sound_only:
            self.player.prev()
            self.announce()
        
    def key_play(self):
        if not self.mode_sound_only:
            self.player.toggle()
        
    def key_volume_up(self):
        self.player.volume_up()

    def key_volume_down(self):
        self.player.volume_down()
        
    def h_mode_sound_only(self, state):
        """  Mode 'Sound only' control
        """ 
        self.mode_sound_only=state
        if self.debug:
            print "* Mode Sound Only: %s" % state

    def h_debug(self, state):
        #print "Debug mode: %s" % state
        self.debug=state
        
        
## Usage           
_=SqueezeAgent()
_.start()
    