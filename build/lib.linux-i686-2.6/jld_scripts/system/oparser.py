"""
    @author: jldupont
    @date: Aug 3, 2010
"""
__all__=["OParser"]

from optparse import OptionParser    


class OParser(object):
    def __init__(self, usage, options):
        self.parser = OptionParser(usage=usage)
        self._process(options)
        
    def _process(self, options):
        for option in options:
            switches, kargs=option
            self.parser.add_option(*switches, **kargs)

    def parse(self):
        (options, args) = self.parser.parse_args()
        return (options, args)
        
    
