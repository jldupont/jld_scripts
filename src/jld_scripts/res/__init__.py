"""
    @author: Jean-Lou Dupont
"""
import os

def get_res_path(filename=None):
    path = os.path.dirname(__file__)
    if filename is not None:
        path=os.path.abspath(path+os.path.sep+filename)
    return path


if __name__=="__main__":
    #print get_res_path("squeezecenter.gif")
    print get_res_path()
    