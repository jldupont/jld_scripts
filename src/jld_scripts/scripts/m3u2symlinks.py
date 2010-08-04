"""
    Generate a hierarchy of symlinks from a .m3u playlist file
    
    Useful for creating backups of files listed in a .m3u file
    
    /$targetdir/m/$artist/$album/$track.mp3
    /$targetdir/d/$artist/$album/$track.$x.mp3
    /$targetdir/u/u.$x.mp3
    
    @author: jldupont
    @date: Aug 3, 2010
"""
import os
import sys

from jld_scripts.system.oparser import OParser
from jld_scripts.system.messaging import UserMessaging
from jld_scripts.music.m3ufile import M3uFile

sname="m3u2symlinks"
susage="""Usage: %s [options] source.m3u dest_path""" % sname
soptions=[
          #(["-c", "--clean"], {"dest":"clean", "help":"Clean the target directory before processing", "action":"store_true", "default":False})
         (["-q", "--quiet"], {"dest":"quiet", "help":"Quiets message generation on stdout", "action":"store_true", "default":False})
         ]

messages={ "args":                  "Missing arguments"
          ,"m3ufile_notfound":      ".m3u input file not found"
          ,"targetdir_create":      "Attempting to create target directory"
          ,"targetdir_createfailed":"Failed to create target directory"
          ,"targetdir_success":     "Successfully created target directory"
          ,"m3u_readfailed":        "Failed to process .m3u input file"
          ,"mutagen_missing":       "Missing 'mutagen' python package"
          }


def main():

    o=OParser(susage, soptions)
    options, args=o.parse()
    um=UserMessaging(sname, options.quiet)
          
    if len(args) < 2:
        um.error(messages["args"])
        sys.exit(1)

    try:    m3ufile=os.path.expanduser(args[0])
    except: m3ufile=None
    
    try:    targetdir=os.path.expanduser(args[1])
    except: targetdir=None 

    if not os.path.isfile(m3ufile):
        um.error(messages["m3ufile_notfound"])
        sys.exit(1)

    if not os.path.isdir(targetdir):
        um.info(messages["targetdir_create"])
        try:
            os.mkdir(targetdir)
            um.info(messages["targetdir_success"])
        except:
            try:
                os.makedirs(targetdir)
                um.info(messages["targetdir_success"])
            except:
                um.error(messages["targetdir_createfailed"])
                sys.exit(1)

    try:
        import mutagen  #@UnusedImport
    except:
        um.error(messages["mutagen_missing"])
        sys.exit(1)
            
    ## ==================================================================
    
    m3u=M3uFile(m3ufile)
    try:
        m3u.refresh()
    except:
        um.error(messages["m3u_readfailed"])
        sys.exit(1)
        
    _process(um, m3u.files)
        
        
def _process(um, files):
    pass
    

if __name__=="__main__":
    main()
