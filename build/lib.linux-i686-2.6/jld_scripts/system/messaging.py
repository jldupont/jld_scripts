"""
    @author: jldupont
    @date: Aug 3, 2010
"""
__all__=["UserMessaging"]


class UserMessaging(object):
    
    itpl="(info) %s"
    wtpl="(warning) %s"
    etpl="(error) %s"
    
    def __init__(self, name, quiet, prepend=""):
        self.quiet=quiet
        self.name=name
        self.prepend=prepend
        
    def info(self, msg):
        self._maybeOutput( self.itpl % msg )
        
    def warning(self, msg):
        self._maybeOutput( self.wtpl % msg )
        
    def error(self, msg):
        self._maybeOutput( self.etpl % msg )
        
    ## =====================================
    
    def _maybeOutput(self, msg):
        if not self.quiet:
            print "%s%s: %s" % (self.prepend, self.name, msg)
                