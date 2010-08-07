"""
    @author: jldupont
    @date: Aug 3, 2010
"""
__all__=["UserMessaging"]


class UserMessaging(object):
    
    itpl="(info) %s"
    wtpl="(warning) %s"
    etpl="(error) %s"
    
    def __init__(self, name, quiet):
        self.quiet=quiet
        self.name=name
        
    def info(self, msg):
        self._maybeOutput( self.itpl % msg )
        
    def warning(self, msg):
        self._maybeOutput( self.wtpl % msg )
        
    def error(self, msg):
        self._maybeOutput( self.etpl % msg )
        
    ## =====================================
    
    def _maybeOutput(self, msg):
        if not self.quiet:
            print "%s: %s" % (self.name, msg)
                