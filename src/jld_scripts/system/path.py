"""
    @author: jldupont
    @date: Aug 4, 2010
"""
import os

__all__=["safe_makedirs"]

def safe_makedirs(path, mode=0777, ex=False):
    try:
        os.makedirs(path, mode)
        return True
    except:
        result=os.path.isdir(path)
        if not ex:
            return result
        else:
            if not result:
                raise Exception()
