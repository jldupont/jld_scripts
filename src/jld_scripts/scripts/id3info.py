"""
    @author: jldupont
    @date: Aug 9, 2010
"""
import os
import sys
import optparse
try:
    import mutagen #@UnusedImport
except:
    print "This script requires the 'mutagen' package available on PyPi"
    sys.exit(1)
    
from jld_scripts.system.oparser import OParser
from jld_scripts.system.messaging import UserMessaging
from jld_scripts.system.path import get_dir_files
#from jld_scripts.music.id3 import known_frames

webhelp_url="http://www.systemical.com/doc/opensource/id3info"
sname="id3info"
susage="""Usage: %s [options] path

Lists info for the given .mp3 files - resulting output in .m3u compatible format
""" % sname
soptions=[
          #(["-c", "--clean"], {"dest":"clean", "help":"Clean the target directory before processing", "action":"store_true", "default":False})
           (["-q", "--quiet"],    {"dest":"quiet",   "help":"Quiets message generation on stdout", "action":"store_true", "default":False})
          ,(["-u", "--usual"],    {"dest":"usual",   "help":"Checks for the 'usual' frames and reports others", "action":"store_true", "default":False})
          ,(["-a", "--all"],      {"dest":"all",     "help":"Lists all frames", "action":"store_true", "default":False})
          ,(["-d", "--del"],      {"dest":"delete",  "help":"Deletes 'unusual' frames", "action":"store_true", "default":False})
          ,(["-s", "--summary"],  {"dest":"summary", "help":"Generate summary information", "action":"store_true", "default":False})
          ,(["-w", "--webhelp"], {"dest":"webhelp", "help":"Opens a online documentation", "action":"store_true", "default":False})
         ]

messages={ "args":        "Missing arguments"
          ,"error_path":  "Invalid path specified"
          ,"zero_file":   "No file to process"
          ,"some_files":  "Processing %s file(s)"
          }

usual_frames=[  "TCON",  ## CONTENT TYPE
                "TPE1",  ## Artist 
                "TPE2",  ## BAND
                "TRCK",  ## Track#
                "TDRC",  ## YEAR 
                "TALB"   ## ALBUM
                ,"TIT2"  ## Track Title
                ,"TLAN"  ## Languages
                ,"TLEN"  ## LENGTH
                ]

def main():

    try:
        o=OParser(susage, soptions)
    except optparse.OptionError:
        print "! invalid option"
        sys.exit(1)
        
    options, args=o.parse()
    um=UserMessaging(sname, False, prepend="#")
    files=[]
      
    if options.webhelp:
        import webbrowser
        webbrowser.open(webhelp_url)
        sys.exit(0)
      
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
        
    if files is None:
        um.error(messages["error_path"])
        sys.exit(1)       
        
    if len(files) == 0:
        um.info(messages["zero_file"])
        sys.exit(0)
        
    um.info(messages["some_files"] % len(files))
    
    process(files, options)
    sys.exit(0)

def process(files, options):

    from mutagen.id3 import ID3
    
    for file in files:
        mp3file=ID3(file)
        frames=mp3file.__dict__["_DictProxy__dict"]
        to_delete=[]
        unusual=[]
        for frame_name in frames:
            
            if options.usual:
                if frame_name not in usual_frames:
                    unusual.append(frame_name)
                    if options.delete:
                        to_delete.append(frame_name)   
                    
        if options.all:
            print "# frames: %s" % frames
            print file

        if unusual and not options.delete:
            print "# unusual frame(s) '%s'" % unusual
            print file    

        if options.delete and to_delete:
            removal_succeeded=True
            for frame_name in to_delete:
                try:    
                    del mp3file[frame_name]
                except:
                    removal_succeeded=False 
                    print "# ERROR attempting to remove frame '%s'" % frame_name

            if removal_succeeded:
                print "# REMOVED unusual frame(s) '%s'" % unusual
                print file    
                
            try:           mp3file.save()
            except: print "# ERROR whilst attempting to save '%s'" % file
            
if __name__=="__main__":
    main()
