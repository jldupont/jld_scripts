"""
    Watcher agent
    
    Created on 2011-02-28

    @author: jldupont
"""
from jld_scripts.system.base import AgentThreadedBase

__all__=["WatcherAgent"]

class WatcherAgent(AgentThreadedBase):

    def __init__(self):
        AgentThreadedBase.__init__(self)
        
    def h___tick__(self, *_):
        pass
        
        
## Usage           
_=WatcherAgent()
_.start()
