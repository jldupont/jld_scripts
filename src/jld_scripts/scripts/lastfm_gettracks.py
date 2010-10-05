"""
    Last.Fm - Fetches pages of tracks from a user's library
        
    Created on 2010-10-04
    @author: jldupont
"""
import os
import sys
import optparse

from jld_scripts.system.oparser import OParser
from jld_scripts.system.messaging import UserMessaging
from jld_scripts.system.path import get_dir_files
#from jld_scripts.music.id3 import known_frames

webhelp_url="http://www.systemical.com/doc/opensource/lastfm_gettracks"
sname="lastfm_gettracks"
susage="""Usage: %s [options] username [directory path]

Fetches the XML data pages of tracks related to a user's library on Last.fm 
""" % sname
soptions=[
          #(["-c", "--clean"], {"dest":"clean", "help":"Clean the target directory before processing", "action":"store_true", "default":False})
           (["-q", "--quiet"],   {"dest":"quiet",  "help":"Quiets message generation on stdout", "action":"store_true", "default":False})
           ,(["-a", "--all"],    {"dest":"all",    "help":"Fetches all pages", "action":"store_true", "default":False})           
           ,(["-d", "--dir"],    {"dest":"path",   "help":"Specifies the destination path", "action":"store", "default":False, "nargs":1})
           ,(["-p", "--page"],    {"dest":"page",   "help":"Specifies which page# to download", "action":"store", "default":False, "nargs":1})
          ,(["-w",  "--webhelp"], {"dest":"webhelp", "help":"Opens a online documentation", "action":"store_true", "default":False})
         ]

messages={ "args":        "Missing arguments"
          ,"error_path":  "Invalid path specified"
          ,"error_dir":   "Invalid directory path"
          ,"error_page":  "Invalid 'page' argument"
          }


def main():

    try:
        o=OParser(susage, soptions)
    except optparse.OptionError, e:
        print "! invalid option: %s" % e
        sys.exit(1)
        
    options, args=o.parse()
    um=UserMessaging(sname, False)
      
    if options.webhelp:
        import webbrowser
        webbrowser.open(webhelp_url)
        sys.exit(0)
    
    if len(args) != 1:
        um.error(messages["args"])
        sys.exit(1)

    dest_path=os.getcwd()
    if options.path:
        dest_path=options.path
        
    try:      path=os.path.expanduser(dest_path)
    except:   path=None

    try:
        ## is 'path' a directory or a file?
        is_dir=os.path.isdir(path)
    except:
        um.error(messages["error_path"])
        sys.exit(1)
        
    ## if the user specified a directory, get all the .mp3 files then
    if not is_dir:
        um.error(messages["error_dir"])
        sys.exit(1)

    page=1
    if options.page:
        try:    page=int(options.page)
        except:
            um.error(messages["error_page"])
            sys.exit(1)

    process(path, page, options.all)

def process(path, page, all):
    """
    """
    
            
if __name__=="__main__":
    main()
