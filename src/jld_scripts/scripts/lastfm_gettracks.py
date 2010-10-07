"""
    Last.Fm - Fetches pages of tracks from a user's library
        
    Created on 2010-10-04
    @author: jldupont
"""
import os
import sys
import optparse
import urllib2
import urllib

from jld_scripts.system.oparser import OParser
from jld_scripts.system.messaging import UserMessaging
from jld_scripts.music.lastfm.parser_gettracks import parse
#from jld_scripts.system.path import get_dir_files
#from jld_scripts.music.id3 import known_frames

TIMEOUT = 4
LIBRARY_GETTRACKS_URL="http://ws.audioscrobbler.com/2.0/?method=library.gettracks&user=%s&page=%s&api_key=%s"
API_KEY="50fa3794354dd9d42fc251416f523388"

webhelp_url="http://www.systemical.com/doc/opensource/lastfm_gettracks"
sname="lastfm_gettracks"
susage="""Usage: %s [options] username

Fetches the XML data pages of tracks related to a user's library on Last.fm 
""" % sname
soptions=[
          #(["-c", "--clean"], {"dest":"clean", "help":"Clean the target directory before processing", "action":"store_true", "default":False})
           (["-q", "--quiet"],   {"dest":"quiet",  "help":"Quiets message generation on stdout", "action":"store_true", "default":False})         
           ,(["-p", "--page"],    {"dest":"page",   "help":"Specifies which page# to download", "action":"store", "default":False, "nargs":1})
          ,(["-w",  "--webhelp"], {"dest":"webhelp", "help":"Opens a online documentation", "action":"store_true", "default":False})
         ]

messages={ "args":        "Missing arguments"
          ,"error_path":  "Invalid path specified"
          ,"error_page":  "Invalid 'page' argument"
          ,"error_dir":   "Invalid path: cannot be a directory"
          ,"error_proc":  "Processing Error: %s"
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
    
    if len(args) != 2:
        um.error(messages["args"])
        sys.exit(1)

    try:      path=os.path.expanduser(args[1])
    except:   path=None

    try:      is_dir=os.path.isdir(path)
    except:
        um.error(messages["error_path"])
        sys.exit(1)
        
    ## if the user specified a directory, get all the .mp3 files then
    if is_dir:
        um.error(messages["error_dir"])
        sys.exit(1)

    page=None
    if options.page:
        try:    page=int(options.page)
        except:
            um.error(messages["error_page"])
            sys.exit(1)

    print "username: %s, path: %s, page: %s, all: %s" % (args[0], path, page, page is None)

    try:
        process(args[0], path, page, page is None)
    except Exception,e:
        um.error(messages["error_proc"] % e)
        sys.exit(1)
    
    sys.exit(0)

def fetch_page(username, page):
    ua=urllib.quote_plus(username.encode("utf-8"))
    url=LIBRARY_GETTRACKS_URL % (ua, page, API_KEY)
    raw=urllib2.urlopen(url, None, TIMEOUT)
    resp=raw.read()
    return resp

def process(username, path, page, all):
    if all:
        process_all(username, path)
    else:
        process_one(username, path, page)
      
def process_all(username, path):
    try:
        page1=fetch_page(username, 1)
        result=parse(page1, debug=False)
    except:
        raise
    
    try:
        props=result.page_props["tracks.attrs"]
    except:
        raise Exception("error recovering page properties")
    
    try:
        num_pages=props["totalPages"]
    except:
        raise Exception("missing 'totalPages' field")
    
    for page in range(2, num_pages):
        pass
    

def process_one(username, path, page):
    try:
        result=fetch_page(username, page)
        write_result(path, result)
    except:
        raise
        
    
def write_result(path, data):
    try:
        file=open(path, "w")
        file.write(data)
        file.close()
        return (True, [])
    except Exception, e:
        return (False, e)
        
def process_page(data):
    pass
    
            
if __name__=="__main__":
    main()
