"""
    @author: jldupont
    @date: Aug 9, 2010
"""
import os
import sys
try:
    import mutagen #@UnusedImport
except:
    print "This script requires the 'mutage' package available on PyPi"
    sys.exit(1)
    
from jld_scripts.system.oparser import OParser
from jld_scripts.system.messaging import UserMessaging
from jld_scripts.system.path import get_dir_files

sname="id3info"
susage="""Usage: %s [options] path

Lists info for the given .mp3 files
""" % sname
soptions=[
          #(["-c", "--clean"], {"dest":"clean", "help":"Clean the target directory before processing", "action":"store_true", "default":False})
          (["-q", "--quiet"],   {"dest":"quiet",   "help":"Quiets message generation on stdout", "action":"store_true", "default":False})
          ,(["-s", "--summary"],{"dest":"summary", "help":"Generate summary information", "action":"store_true", "default":False})
         ]

messages={ "args":        "Missing arguments"
          ,"error_path":  "Invalid path specified"
          ,"zero_file":   "No file to process"
          ,"some_files":  "Processing %s file(s)"
          }

def main():

    o=OParser(susage, soptions)
    options, args=o.parse()
    um=UserMessaging(sname, False)
    files=[]
      
    if len(args) < 1:
        um.error(messages["args"])
        sys.exit(1)

    try:      path=os.path.expanduser(args[0])
    except:   path=None

    try:
        ## is 'path' a directory or a file?
        is_dir=os.path.isdir(path)
        is_file=os.path.isfile(path)
    except:
        um.error(messages["error_path"])
        sys.exit(1)
        
    ## if the user specified a directory, get all the .mp3 files then
    if is_dir:
        files=get_dir_files(path)
        
    if is_file:
        files=[].append(path)
        
    if len(files) == 0:
        um.info(messages["zero_file"])
        sys.exit(0)
        
    um.info(messages["some_files"] % len(files))
    
    process(files, options.summary)

def process(files, summary):
    """
    """
    

if __name__=="__main__":
    main()
