Collection of python utility scripts

- m3u2symlinks
- id3info
- lastfm_gettracks
- squeezecenter_utils

More information available [here](http://www.systemical.com/doc/opensource/jld_scripts).

TODO
====

 * Auto-refresh Squeeze Box for squeezecenter_utils: when the server is restarte, the application looses synchronization with the server. 


Note
=====

When distributing using 'sdist' the MANIFEST.in is important in order to include resource files.


History
=======
0.7.6: better fix for squeezecenter_utils

0.7.5: squeezecenter_utils: now uses the most recent & first player discovered

0.7.4: fixed missing *.gif files in the setup egg

0.7.1: fixed string encoding issue in "m3u2symlinks"

0.7.0: added 'squeezecenter_utils'

0.6: added 'lastfm_gettracks'

0.5.5: added "TLEN" and "TPE2" support for id3info

0.5.4: corrected missing 'id3info' in /usr/bin