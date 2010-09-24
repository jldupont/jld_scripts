"""
    Path related utilities
    
    @author: jldupont
    @date: Aug 4, 2010
"""
import os

__all__=["safe_makedirs", "get_dir_files"]

def safe_makedirs(path, mode=0777, ex=False):
    """
    Creates a directory hierarchy
    
    @return: True if directory existed or created successfully
    @return: False if directory cannot be created
    @exception: if directory can't be created AND ex=True
    """
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


def get_dir_files(path, ext="mp3"):
    """
    Retrieves the list of files with extension `ext`
    in the path specified.
    
    If the path specified isn't a directory, the usual
    exception will be raised.
    """
    list=os.listdir(path)
    result=[]
    for item in list:
        name=os.path.basename(item)
        try:
            bits=name.split(".")
            extension=bits[-1:][0].lower()
        except:
            extension=None
        if ext==extension:
            result.append(os.path.join(path, name))
    return result
