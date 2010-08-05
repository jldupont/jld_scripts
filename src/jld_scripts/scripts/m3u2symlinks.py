"""
    Generate a hierarchy of symlinks from a .m3u playlist file
    
    Useful for creating backups of files listed in a .m3u file
    
    /$targetdir/m/$artist/$album/$track.mp3
    /$targetdir/d/$artist/$album/$track.$x.mp3
    /$targetdir/u/u.$x.mp3
    
    Use case #1:
    - user exports .m3u file from media player
    - user launches 'm3u2symlinks'
    - user backups resulting file hierarchy
    
    Use case #2: user refreshes an already processed .m3u file
    = User might have modified ID3 tags in some files
    - multiple symlinks pointing to same file...
      - remove all but most recent symlink   
    
    Cases:
    - broken symlink(s): use external tool to manage
    - dups: listed under the /$targetdir/d directory
    - mp3 file without id3 tag header: listed under /$targetdir/u
    - mp3 file with missing id3 fields:
      - missing $artist: listed under /u
      - missing $album: listed in /m/$artist
      - missing $track: listed in /m/$artist/$album

    
    @author: jldupont
    @date: Aug 3, 2010
"""
import os
import sys

from jld_scripts.system.oparser import OParser
from jld_scripts.system.messaging import UserMessaging
from jld_scripts.music.m3ufile import M3uFile
from jld_scripts.music.mp3file import get_id3_params
from jld_scripts.system.path import safe_makedirs

sname="m3u2symlinks"
susage="""Usage: %s [options] source.m3u dest_path""" % sname
soptions=[
          #(["-c", "--clean"], {"dest":"clean", "help":"Clean the target directory before processing", "action":"store_true", "default":False})
          (["-q", "--quiet"],   {"dest":"quiet",   "help":"Quiets message generation on stdout", "action":"store_true", "default":False})
          ,(["-v", "--verbose"],{"dest":"verbose", "help":"Generate progress information", "action":"store_true", "default":False})
         ,(["-r", "--refresh"], {"dest":"refresh", "help":"Refresh any existing symlink", "action":"store_true", "default":False})
         ,(["-g", "--gen"],     {"dest":"gen",     "help":"Generate summary .m3u files",  "action":"store_true", "default":False})
         ]

messages={ "args":                  "Missing arguments"
          ,"m3ufile_notfound":      ".m3u input file not found"
          ,"targetdir_create":      "Attempting to create target directory"
          ,"targetdir_createfailed":"Failed to create target directory"
          ,"targetdir_success":     "Successfully created target directory"
          ,"m3u_readfailed":        "Failed to process .m3u input file"
          ,"mutagen_missing":       "Missing 'mutagen' python package"
          ,"top_fail":              "Failed to create top level directories in target directory"
          ,"artist_dir_failed":      "Creating 'artist' directory: %s"
          ,"error_symlink":          "Creating symlink: %s"
          ,"error_genmusic":         "Generating music symlinks: %s"
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

    ## Create $targetdir directory hierarchy (if needed)

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
    try:
        _create_top_level_dirs(targetdir)
    except:
        um.error(messages["top_fail"])
        sys.exit(1)
    
    ## ==================================================================    
    m3u=M3uFile(m3ufile)
    try:
        m3u.refresh()
    except:
        um.error(messages["m3u_readfailed"])
        sys.exit(1)
        
    music, unknown, dups=_process(um, targetdir, m3u.files)
    
    #print "*** music: ", music
    #print "*** unknown: ", unknown
    #print "*** dups: ", dups

    try:
        _gen_music_dir(options.verbose, um, targetdir, music, options.refresh)
    except Exception, e:
        um.error(messages["error_genmusic"] % e)
        
def _gen_music_dir(verbose, um, targetdir, music, refresh):
    for link_name, entry in music.iteritems():
        file, details=entry
        artist, album, _title = details
        if verbose:
            print "> processing music file: %s" % file
            
        ## generate album sub-dir
        ad=os.path.join(targetdir, "m", artist, album)
        
        ## don't worry if we can't create the 'album' sub-dir just yet
        safe_makedirs(ad)

        link_path=os.path.join(targetdir, "m", artist, album, link_name)
        
        exists=os.path.islink(link_path)
        if exists:
            if verbose:
                print "! symlink exists: %s" % link_path
            if refresh:
                try:    os.unlink(link_path)
                except: pass

        if not exists or (exists and refresh):                
            try:
                os.symlink(file, link_path)
            except:
                um.error(messages["error_symlink"] % link_path)
                sys.exit(1)
            
        

def _create_top_level_dirs(targetdir):
    m=os.path.join(targetdir, "m")
    u=os.path.join(targetdir, "u")
    d=os.path.join(targetdir, "d")
    
    safe_makedirs(m, ex=True)
    safe_makedirs(u, ex=True)
    safe_makedirs(d, ex=True)

        
def _process(um, targetdir, files):
    
    valid=[]
    unknown=[]
    dups=[]
    music={}
    
    artists=[]
    
    ## Gather ID3 information
    for file in files:
        try:
            artist, album, title=get_id3_params(file)
            
            ea=artist.encode("UTF-8").replace("/", "_").strip()
            eb=album.encode("UTF-8").replace("/", "_").strip()
            valid.append((file, (ea, eb, title.strip())))
        except:
            unknown.append(file)

    ## Assign Link Name to valid entries
    for entry in valid:
        file, details=entry
        artist, album, title=details
        ln="%s-%s-%s.mp3" % (artist, album, title)
        link_name=ln.encode("UTF-8").replace("/", "_")
        list=music.get(link_name, [])
        
        ## we'll handle dups later
        list.append((file, details))
        music[link_name]=list
        
        ## collect artists to facilitate directory hierarchy creation
        if artist not in artists:
            ea=artist.encode("UTF-8").replace("/", "_")
            artists.append(ea)
        
    ## Manage Dups
    for entry in music.iteritems():
        link_name, list=entry
        first=list[0]
        if len(list) > 1:
            count=1
            for item in list:
                file, details=item
                new_link_name="%s.%s" % (link_name, count)
                count+=1
                dups.append((new_link_name, file))
        music[link_name]=first
            
                
    ## create top level artist directories
    for artist in artists:
        ma=os.path.join(targetdir, "m", artist)
        if not safe_makedirs(ma):
            um.error(messages["artist_dir_failed"] % ma)
            sys.exit(1)
        
        da=os.path.join(targetdir, "d", artist)
        if not safe_makedirs(da):
            um.error(messages["artist_dir_failed"] % da)
            sys.exit(1)
        
    return music, unknown, dups


if __name__=="__main__":
    main()
