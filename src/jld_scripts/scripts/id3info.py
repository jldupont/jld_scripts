"""
    @author: jldupont
    @date: Aug 9, 2010
"""
import os
import sys
try:
    import mutagen #@UnusedImport
except:
    print "This script requires the 'mutagen' package available on PyPi"
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

frames={    
  "PCNT":"Play counter"
  ,"POPM":"Popularimete"
  ,"POSS":"Position synchronisation frame"
  ,"RBUF":"Recommended buffer size"
  ,"RVA2":"Relative volume adjustment (2)"
  ,"RVRB":"Reverb"
  ,"SEEK":"Seek frame"
  ,"SIGN":"Signature frame"
  ,"SYLT":"Synchronised lyric/text"
  ,"SYTC":"Synchronised tempo codes"
  ,"TALB":"Album/Movie/Show title"
  ,"TBPM":"BPM (beats per minute)"
  ,"TCOM":"Composer"
  ,"TCON":"Content type"
  ,"TCOP":"Copyright message"
  ,"TDEN":"Encoding time"
  ,"TDLY":"Playlist delay"
  ,"TDOR":"Original release time"
  ,"TDRC":"Recording time"
  ,"TDRL":"Release time"
  ,"TDTG":"Tagging time"
  ,"TENC":"Encoded by"
  ,"TEXT":"Lyricist/Text writer"
  ,"TFLT":"File type"
  ,"TIPL":"Involved people list"
  ,"TIT1":"Content group description"
  ,"TIT2":"Title/songname/content description"
  ,"TIT3":"Subtitle/Description refinement"
  ,"TKEY":"Initial key"
  ,"TLAN":"Language(s)"
  ,"TLEN":"Length"
  ,"TMCL":"Musician credits list"
  ,"TMED":"Media type"
  ,"TMOO":"Mood"
  ,"TOAL":"Original album/movie/show title"
  ,"TOFN":"Original filename"
  ,"TOLY":"Original lyricist(s)/text writer(s)"
  ,"TOPE":"Original artist(s)/performer(s)"
  ,"TOWN":"File owner/licensee"
  ,"TPE1":"Lead performer(s)/Soloist(s)"
  ,"TPE2":"Band/orchestra/accompaniment"
  ,"TPE3":"Conductor/performer refinement"
  ,"TPE4":"Interpreted, remixed, or otherwise modified by"
  ,"TPOS":"Part of a set"
  ,"TPRO":"Produced notice"
  ,"TPUB":"Publisher"
  ,"TRCK":"Track number/Position in set"
  ,"TRSN":"Internet radio station name"
  ,"TRSO":"Internet radio station owner"
  ,"TSOA":"Album sort order"
  ,"TSOP":"Performer sort order"
  ,"TSOT":"Title sort order"
  ,"TSRC":"ISRC (international standard recording code)"
  ,"TSSE":"Software/Hardware and settings used for encoding"
  ,"TSST":"Set subtitle"
  ,"TXXX":"User defined text information frame"
  ,"UFID":"Unique file identifier"
  ,"USER":"Terms of use"
  ,"USLT":"Unsynchronised lyric/text transcription"
  ,"WCOM": "Commercial information"
  ,"WCOP":"Copyright/Legal information"
  ,"WOAF":"Official audio file webpage"
  ,"WOAR":"Official artist/performer webpage"
  ,"WOAS":"Official audio source webpage"
  ,"WORS":"Official Internet radio station homepage"
  ,"WPAY":"Payment"
  ,"WPUB":"Publishers official webpage"
  ,"WXXX":"User defined URL link frame"           
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
    from mutagen.id3 import ID3
    
    for file in files:
        mp3file=ID3(file)
        print mp3file.__dict__

if __name__=="__main__":
    main()
