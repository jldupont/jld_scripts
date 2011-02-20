"""
    Last.Fm - Fetches pages of tracks from a user's library
        
    Created on 2010-10-04
    @author: jldupont
"""
#import os
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
           (["-v", "--verbose"],  {"dest":"verbose",  "help":"More information to stdout", "action":"store_true", "default":False})         
           ,(["-p", "--page"],    {"dest":"page",     "help":"Specifies which page# to download", "action":"store", "default":False, "nargs":1})
           ,(["-f", "--fwd"],     {"dest":"fwd",      "help":"Go forward from 'page' i.e. download all starting from 'page'", "action":"store_true", "default":False})
          ,(["-w",  "--webhelp"], {"dest":"webhelp",  "help":"Opens a online documentation", "action":"store_true", "default":False})
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
    um=UserMessaging(sname, False, prepend="#")
      
    if options.webhelp:
        import webbrowser
        webbrowser.open(webhelp_url)
        sys.exit(0)
    
    if len(args) != 1:
        um.error(messages["args"])
        sys.exit(1)

    """
    -p and -f    : download all from 'page' onwards
    -p           : download only 'page'
    -f           : download all from page 1
    *no options* : download all from page 1 
    """

    all_pages=True
    page=1
    if options.page:
        try:    
            page=int(options.page)
        except:
            um.error(messages["error_page"])
            sys.exit(1)

    if not options.fwd and options.page:
        all_pages=False

    if options.verbose:
        print "## username: %s, page: %s, all: %s" % (args[0], page, all_pages)

    try:
        process(args[0], page, all_pages, options.verbose)
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

def process(username, page, all, verbose):
    if all:
        process_all(username, page, verbose)
    else:
        process_one(username, page, verbose)
      
def process_all(username, from_page, verbose):

    ## start with page 1 to get # of pages in total
    num_pages_raw, data=process_page(username, from_page)
    
    try: num_pages=int(num_pages_raw)
    except:
        raise Exception("problem with 'totalPages' parameter")

    if from_page > num_pages:
        raise Exception("Invalid start page")
    
    if verbose:
        print "# number of pages: %s" % num_pages
        print "# processing page: %s" % from_page
    
    write_result(data)
    
    for page in range(from_page+1, num_pages+1):
        if verbose:
            print "# processing page: %s" % page
        _, pdata=process_page(username, page)
        write_result(pdata)
            
    
    write_result(data)
    

def process_one(username, page, verbose):
    if verbose:
        print "# Processing page: %s" % page
    _, data=process_page(username, page)
    write_result(data)

    
def write_result(data):
    for line in data:
        formatted_line=format_line(line)
        print formatted_line.encode("utf8")
        
    
def format_line(line_data):
    a=format_item( line_data["artist.name"])
    n=format_item( line_data["name"] )
    p=format_item( line_data["playcount"] )
    return "%s  %s  %s\r" % (a, n, p)
    
def format_item(item):
    while True:
        item=item.replace("  ", " ")
        if item.find("  ")==-1:
            break
    return item
    
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
