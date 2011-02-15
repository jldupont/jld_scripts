'''
    Clock Agent
    
    Created on 2011-02-14

    @author: jldupont
'''
from Queue import Queue
from jld_scripts.system import mswitch
from jld_scripts.system.base import process_queues, message_processor

__all__=["Clock"]

class Clock(object):
    
    LOW_PRIORITY_MESSAGE_BURST_SIZE=5
    
    def __init__(self, time_base):
        """
        @param time_base: in milliseconds
        """
        self.time_base=time_base 
        self.ticks_second=time_base/1000

        self.iq=Queue()
        self.isq=Queue()
        mswitch.subscribe("__main__", self.iq, self.isq)

        self.tick_count=1
        self.sec_count=0
        self.min_count=0
        self.hour_count=0
        self.day_count=0

        self.interests={}
        self.responsesInterests=[]

    def pub(self, msgType, *pargs, **kargs):
        mswitch.publish("__main__", msgType, *pargs, **kargs)
        
    def tick(self, *_):
        """
        Performs message dispatch
        """
        tick_min=False
        tick_hour=False
        tick_day=False
        tick_second = (self.tick_count % self.ticks_second) == 0 
        self.tick_count += 1
        
        if tick_second:
            self.sec_count += 1

            tick_min=(self.sec_count % 60)==0
            if tick_min:
                self.min_count += 1
                
                tick_hour=(self.min_count % 60)==0
                if tick_hour:
                    self.hour_count += 1
                    
                    tick_day=(self.hour_count % 24)==0
                    if tick_day:
                        self.day_count += 1
        
        #print "tick! ", tick_second
        mswitch.publish("__main__", "__tick__", self.ticks_second, 
                        tick_second, tick_min, tick_hour, tick_day, 
                        self.sec_count, self.min_count, self.hour_count, self.day_count)
        
        #(src_agent, agent_name, agent_id, 
        #  interest_map, responsesInterestList, 
        #  iq, isq, processor, low_priority_burst_size=5)
        quit=process_queues(False, self, "__main__", "__main__", 
                       self.interests, self.responsesInterests,
                       self.iq, self.isq, message_processor 
                       )
        ## for gobject... just in case
        return True
