"""
    Generate a hierarchy of symlinks from a .m3u playlist file
    
    Useful for creating backups of files listed in a .m3u file
    
    @author: jldupont
    @date: Aug 3, 2010
"""
import os
import sys

sname="m3u2symlinks"
susage="""Usage: %s [options] source.m3u dest_path""" % sname
soptions=[
          (["-c", "--clean"], {"dest":"clean", "help":"Clean the target directory before processing", "action":"store_true", "default":False})
         ,(["-q", "--quiet"], {"dest":"quiet", "help":"Quiets message generation on stdout", "action":"store_true", "default":False})
         ]

messages={ "args":"Missing arguments"
          }


def main():
    from jld_scripts.system.oparser import OParser
    from jld_scripts.system.messaging import UserMessaging

    o=OParser(susage, soptions)
    options, args=o.parse()
      
    um=UserMessaging(sname, options.quiet)
      
    if len(args) < 2:
        um.error(messages["args"])
        sys.exit(1)

        
    print options
    print args

main()
