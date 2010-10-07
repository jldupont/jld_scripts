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

TIMEOUT = 30
LIBRARY_GETTRACKS_URL="http://ws.audioscrobbler.com/2.0/?method=library.gettracks&user=%s&page=%s&api_key=%s"
API_KEY="50fa3794354dd9d42fc251416f523388"

webhelp_url="http://www.systemical.com/doc/opensource/lastfm_gettracks"
sname="lastfm_gettracks"
susage="""Usage: %s [options] username

Fetches the XML data pages of tracks related to a user's library on Last.fm 
NOTE: make sure the user's profile is set to 'public'
""" % sname
soptions=[
          #(["-c", "--clean"], {"dest":"clean", "help":"Clean the target directory before processing", "action":"store_true", "default":False})
           (["-q", "--quiet"],   {"dest":"quiet",  "help":"Quiets message generation on stdout", "action":"store_true", "default":False})         
           ,(["-p", "--page"],    {"dest":"page",   "help":"Specifies which page# to download", "action":"store", "default":False, "nargs":1})
          ,(["-w",  "--webhelp"], {"dest":"webhelp", "help":"Opens a online documentation", "action":"store_true", "default":False})
         ]

messages={ "args":        "Invalid arguments"
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
    
    if len(args) != 1:
        um.error(messages["args"])
        sys.exit(1)

    page=None
    if options.page:
        try:    page=int(options.page)
        except:
            um.error(messages["error_page"])
            sys.exit(1)

    #print "username: %s, path: %s, page: %s, all: %s" % (args[0], path, page, page is None)

    try:
        process(args[0], page, page is None, options.quiet)
    except Exception,e:
        um.error(messages["error_proc"] % e)
        sys.exit(1)
    
    sys.exit(0)

def fetch_page(username, page):
    """
    Fetches 1 page from library.gettracks on Last.fm
    """
    ua=urllib.quote_plus(username.encode("utf-8"))
    url=LIBRARY_GETTRACKS_URL % (ua, page, API_KEY)
    raw=urllib2.urlopen(url, None, TIMEOUT)
    resp=raw.read()
    return resp

def process(username, page, all, quiet):
    if all:
        process_all(username, quiet)
    else:
        process_one(username, page)
      
def process_all(username, quiet):

    ## start with page 1 to get # of pages in total
    num_pages_raw, data=process_page(username, 1)
    
    try: num_pages=int(num_pages_raw)
    except:
        raise Exception("problem with 'totalPages' parameter")
    
    if not quiet:
        print "# number of pages: %s" % num_pages
    
    for page in range(2, num_pages):
        if not quiet:
            print "# processing page: %s" % page
        _, pdata=process_page(username, page)
        write_result(pdata)
            
    
    write_result(data)
    

def process_one(username, page):
    _, data=process_page(username, page)
    write_result(data)

    
def write_result(data):
    for line in data:
        formatted_line=format_line(line)
        print formatted_line
        
    
def format_line(line_data):
    n=line_data["name"]
    a=line_data["artist.name"]
    p=line_data["playcount"]
    return "%s %s %s\r" % (a, n, p)
    
def process_page(username, page):
    """
    Fetches 1 page, parses it, extracts data
    """
    try:
        page1=fetch_page(username, page)
        result=parse(page1, debug=False)
    except Exception, e:
        raise Exception("error fetching/processing page %s: %s" % (page, e))
    
    try:
        props=result.page_props["tracks.attrs"]
    except:
        raise Exception("error recovering page properties")
    
    try:
        data=result.tracks
    except:
        raise Exception("error recovering page data")
    
    try:
        num_pages=props["totalPages"]
    except:
        raise Exception("missing 'totalPages' field")
    
    return (num_pages, data)

            
if __name__=="__main__":
    main()
