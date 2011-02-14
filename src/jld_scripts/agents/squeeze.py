"""
    'Squeeze' Agent - controls Squeezebox Center
    
    Messages Processed:
    ===================
    - "mk_key_press"
    
    
    @author: jldupont
    Created on Oct 22, 2010
"""
from jld_scripts.system.base import AgentThreadedBase

from pysqueezecenter.server import Server
from pysqueezecenter.player import Player

__all__=["SqueezeAgent"]

class SqueezeAgent(AgentThreadedBase):
    
    def __init__(self):
        AgentThreadedBase.__init__(self)
        
        
    def h_mk_key_press(self, key):
        """ 
        Direct access to the notification facility
        """
        sc = Server(hostname="127.0.0.1", port=9090)
        sc.connect()
                
        players = sc.get_players()
        self.player=players[0]
        
        dispatch_name="key_%s" % key.replace("-", "_")
        try:    getattr(self, dispatch_name)()
        except: pass
        
    def key_mute(self):
        self.player.set_muting( not self.player.get_muting() )
        
    def key_stop_cd(self):
        self.player.stop()
        
    def key_next_song(self):
        self.player.next()
        
    def key_previous_song(self):
        self.player.prev()
        
    def key_play_pause(self):
        self.player.toggle()
        
    def key_volume_up(self):
        self.player.volume_up()

    def key_volume_down(self):
        self.player.volume_down()
        
## Usage           
_=SqueezeAgent()
_.start()
    