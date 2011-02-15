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
    
    def __init__(self):
        AgentThreadedBase.__init__(self)
        self.cArtist=""
        self.cAlbum=""
        self.cTitle=""
        self._reconnect()
        
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

        
    def h_mk_key_press(self, key):
        """ 
        Direct access to the notification facility
        """
        if self.player is None:
            self._reconnect()
            
        ## we tried...
        if self.player is None:
            return

        dispatch_name="key_%s" % key.replace("-", "_")
        try:    getattr(self, dispatch_name)()
        except: pass
        
    def key_mute(self):
        self.player.set_muting( not self.player.get_muting() )
        
    def key_stop_cd(self):
        self.player.stop()
        self.announce()
        
    def key_next_song(self):
        self.player.next()
        self.announce()
        
    def key_previous_song(self):
        self.player.prev()
        self.announce()
        
    def key_play_pause(self):
        self.player.toggle()
        
    def key_volume_up(self):
        self.player.volume_up()

    def key_volume_down(self):
        self.player.volume_down()
        
## Usage           
_=SqueezeAgent()
_.start()
    