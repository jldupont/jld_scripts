"""
    @author: jldupont
    @date: Jul 29, 2010
"""
import os
__all__=["M3uFile"]


class M3uFile(object):
    def __init__(self, path):
        self.path=os.path.expanduser(path)
        self.modif=None
        self.files=[]

    def refresh(self):
        """
        Verifies if the underlying .m3u changed
        since the last processing
        
        @return: False: no change, True: change detected
        """
        mtime=os.path.getmtime(self.path)
        
        if mtime==self.modif:
            return False
        
        self.modif=mtime       

        self._process()
        return True
        
    def _process(self):
        self.files=[]
        try:
            file=open(self.path, "r")
            for line in file:
                l=line.lstrip().rstrip("\n")
                if l.startswith("#"):
                    continue
                self.files.append(l)
        finally:
            try:    file.close()
            except: pass

    


if __name__=="__main__":
    mf=M3uFile("~/MyTopRated.m3u")
    mf.refresh()
    
    
