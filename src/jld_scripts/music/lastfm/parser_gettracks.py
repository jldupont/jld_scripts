"""
   Parser for the API method 'library.getTracks' 
        
    Created on 2010-10-04
    @author: jldupont
"""

'''
Created on May 13, 2010

@author: jldupont
'''
# -*- coding: utf-8 -*-
from base import BaseHandler, process  

__all__=["parse"]


def parse(xml, debug=False):
    handler=Handler(debug)
    process(xml, handler)
    return handler

            

class Handler(BaseHandler):
    """
    User.getRecentTracks response handler
    
    Extracts the "track" elements
    """
    
    def __init__(self, debug=False):
        BaseHandler.__init__(self, debug)
        self.page_props={}
        self.tracks=[]
        self.currentTag={}
        self.sm= {
                   ("se", "lfm"):                    "do_skip"
        
                  ,("se", "tracks"):                "do_tracks"
                  ,("en", "tracks"):                "do_skip"
        
                  ,("se", "track"):                  "do_begin_track"
                  ,("en", "track"):                  "do_end_track"
                  
                  ,("se", "id"):                     "do_noop"
                  ,("se", "id", "en", "id"):         "do_grab_data"
                  
                  ,("se", "name"):                   "do_noop"
                  ,("se", "name", "en", "name"):     "do_grab_data"

                  ,("se", "url"):                    "do_noop"
                  ,("se", "url", "en", "url"):       "do_grab_data"

                  ,("se", "playcount"):                     "do_noop"       
                  ,("se", "playcount", "en", "playcount"):  "do_grab_data"

                  ,("se", "mbid"):                          "do_noop"
                  ,("se", "mbid", "en", "mbid"):            "do_grab_data"
            
            ## ARTIST      
                  ,("se", "artist"):                 "do_noop"
                  ,("se", "artist", "en", "artist"): "do_skip"
                  
                  ,("se", "artist", "se", "name"):                "do_noop"
                  ,("se", "artist", "se", "name", "en", "name"):  ("do_grab_artist_params", "artist.name")
                  
                  ,("se", "artist", "se", "mbid"):                "do_noop"  
                  ,("se", "artist", "se", "mbid", "en", "mbid"):  ("do_grab_artist_params", "artist.mbid")

                  ,("se", "artist", "se", "url"):                "do_noop"  
                  ,("se", "artist", "se", "url", "en", "url"):  ("do_grab_artist_params", "artist.url")

            ## ALBUM
                  ,("se", "album"):                "do_noop"
                  ,("se", "album", "en", "album"): "do_skip"

                  ,("se", "album", "se", "artist"):                "do_noop"
                  ,("se", "album", "se", "artist", "en", "artist"):  ("do_grab_album_params", "album.artist")

                  ,("se", "album", "se", "title"):                "do_noop"
                  ,("se", "album", "se", "title", "en", "title"):  ("do_grab_album_params", "album.title")
                  
                  ,("se", "album", "se", "mbid"):                "do_noop"  
                  ,("se", "album", "se", "mbid", "en", "mbid"):  ("do_grab_album_params", "album.mbid")

                  ,("se", "album", "se", "url"):                "do_noop"  
                  ,("se", "album", "se", "url", "en", "url"):  ("do_grab_album_params", "album.url")

                  }

    def do_tracks(self, event):
        self.do_grab_attrs(event)
        self.do_skip(event)
        self.page_props=self.props

    def do_begin_track(self, event):
        if self.debug:
            print "!!! do_begin_track"
        self.props={}
        self.do_skip(event)
        
    def do_end_track(self, _event):
        if self.debug:
            print "do_end_track"
        self.tracks.append(self.props)
        self.props={}
    

    def do_grab_artist_params(self, event, param):
        if self.debug:
            print "do_grab_artist_params: event: %s" % str(event)
        (_, data) = event
        self.props[param]=data
        self._pop(2)

    def do_grab_album_params(self, event, param):
        if self.debug:
            print "do_grab_album_params: event: %s" % str(event)
        (_, data) = event
        self.props[param]=data
        self._pop(2)

    def do_grab_tag_params(self, event, param):
        if self.debug:
            print "do_grab_tag_params: event: %s" % str(event)
        (_, data) = event
        self.currentTag[param] = data
        self._pop(2)

    def do_commit_tag(self, _event):
        self.tags=self.props.get("tags", [])
        if self.currentTag:
            self.tags.append(self.currentTag)
            self.props["tags"]=self.tags
            self.currentTag={}

## ================================================== Tests

if __name__=="__main__":

    """
    """


    r_test = u"""<?xml version="1.0" encoding="utf-8"?> 
<lfm status="ok"> 
<tracks user="jldupont" page="1" perPage="50" totalPages="186"> 
<track> 
    <name>Merging Oceans</name> 
    <playcount>101</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Rotersand/_/Merging+Oceans</url> 
    <duration>454000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Rotersand</name> 
        <mbid>797bcf41-0e02-431d-ab99-020e1cb3d0fd</mbid> 
        <url>http://www.last.fm/music/Rotersand</url> 
    </artist> 
                    <album> 
            <name>Merging Oceans</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B00008O89T.03.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B00008O89T.03.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B00008O89T.03.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B00008O89T.03.MZZZZZZZ.jpg</image> 
    </track> 
<track> 
    <name>Surviving (Synth Amok Remix)</name> 
    <playcount>98</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/NamNamBulu/_/Surviving+%28Synth+Amok+Remix%29</url> 
    <duration>0</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>NamNamBulu</name> 
        <mbid>aff48c86-899b-490f-b5e4-39e80d43465c</mbid> 
        <url>http://www.last.fm/music/NamNamBulu</url> 
    </artist> 
                    <album> 
            <name>Expansion</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B00024DORU.01.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B00024DORU.01.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B00024DORU.01.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B00024DORU.01.MZZZZZZZ.jpg</image> 
    </track> 
<track> 
    <name>Introspection</name> 
    <playcount>91</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Introspection</url> 
    <duration>243000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Mind.In.A.Box</name> 
        <mbid>6fe25812-9155-43a1-b5af-8371f90a4f59</mbid> 
        <url>http://www.last.fm/music/Mind.In.A.Box</url> 
    </artist> 
                    <album> 
            <name>Crossroads</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/9964547.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/9964547.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/9964547.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/9964547.jpg</image> 
    </track> 
<track> 
    <name>Protection</name> 
    <playcount>90</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Massive+Attack/_/Protection</url> 
    <duration>472000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Massive Attack</name> 
        <mbid>10adbe5e-a2c0-4bf3-8249-2b4cbf6e6ca8</mbid> 
        <url>http://www.last.fm/music/Massive+Attack</url> 
    </artist> 
                    <album> 
            <name>Collected CD1</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/37861757.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/37861757.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/37861757.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/37861757.jpg</image> 
    </track> 
<track> 
    <name>Safe From Harm</name> 
    <playcount>88</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Massive+Attack/_/Safe+From+Harm</url> 
    <duration>318000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Massive Attack</name> 
        <mbid>10adbe5e-a2c0-4bf3-8249-2b4cbf6e6ca8</mbid> 
        <url>http://www.last.fm/music/Massive+Attack</url> 
    </artist> 
                    <album> 
            <name>Collected CD1</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/37861757.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/37861757.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/37861757.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/37861757.jpg</image> 
    </track> 
<track> 
    <name>Change</name> 
    <playcount>85</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Change</url> 
    <duration>297000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Mind.In.A.Box</name> 
        <mbid>6fe25812-9155-43a1-b5af-8371f90a4f59</mbid> 
        <url>http://www.last.fm/music/Mind.In.A.Box</url> 
    </artist> 
                    <album> 
            <name>Lost Alone</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/8720709.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/8720709.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/8720709.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/8720709.jpg</image> 
    </track> 
<track> 
    <name>Amnesia</name> 
    <playcount>85</playcount> 
    <tagcount>2</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Amnesia</url> 
    <duration>441000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Mind.In.A.Box</name> 
        <mbid>6fe25812-9155-43a1-b5af-8371f90a4f59</mbid> 
        <url>http://www.last.fm/music/Mind.In.A.Box</url> 
    </artist> 
                    <album> 
            <name>Crossroads</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/9964547.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/9964547.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/9964547.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/9964547.jpg</image> 
    </track> 
<track> 
    <name>Vanishing Point</name> 
    <playcount>83</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/New+Order/_/Vanishing+Point</url> 
    <duration>316000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>New Order</name> 
        <mbid>f1106b17-dcbb-45f6-b938-199ccfab50cc</mbid> 
        <url>http://www.last.fm/music/New+Order</url> 
    </artist> 
                    <album> 
            <name>Technique</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/8641323.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/8641323.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/8641323.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/8641323.jpg</image> 
    </track> 
<track> 
    <name>Suffocate</name> 
    <playcount>82</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Minerve/_/Suffocate</url> 
    <duration>254000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Minerve</name> 
        <mbid>b93145c8-3734-4c19-91c4-8b4b6b34f2d9</mbid> 
        <url>http://www.last.fm/music/Minerve</url> 
    </artist> 
                    <album> 
            <name>Breathing Avenue</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
    </track> 
<track> 
    <name>What Your Soul Sings</name> 
    <playcount>81</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Massive+Attack/_/What+Your+Soul+Sings</url> 
    <duration>396000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Massive Attack</name> 
        <mbid>10adbe5e-a2c0-4bf3-8249-2b4cbf6e6ca8</mbid> 
        <url>http://www.last.fm/music/Massive+Attack</url> 
    </artist> 
                    <album> 
            <name>Collected CD1</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/37861757.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/37861757.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/37861757.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/37861757.jpg</image> 
    </track> 
<track> 
    <name>Afraid of Myself</name> 
    <playcount>80</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Minerve/_/Afraid+of+Myself</url> 
    <duration>246000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Minerve</name> 
        <mbid>b93145c8-3734-4c19-91c4-8b4b6b34f2d9</mbid> 
        <url>http://www.last.fm/music/Minerve</url> 
    </artist> 
                    <album> 
            <name>Breathing Avenue</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
    </track> 
<track> 
    <name>All The Things She Said</name> 
    <playcount>79</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Simple+Minds/_/All+The+Things+She+Said</url> 
    <duration>256000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Simple Minds</name> 
        <mbid>f41490ce-fe39-435d-86c0-ab5ce098b423</mbid> 
        <url>http://www.last.fm/music/Simple+Minds</url> 
    </artist> 
                    <album> 
            <name>The best of</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/51126317.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/51126317.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/51126317.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/51126317.jpg</image> 
    </track> 
<track> 
    <name>Lost Little Robot</name> 
    <playcount>79</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Beborn+Beton/_/Lost+Little+Robot</url> 
    <duration>335000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Beborn Beton</name> 
        <mbid>b982e7e7-bbed-4c86-91c4-db5267e3cc9b</mbid> 
        <url>http://www.last.fm/music/Beborn+Beton</url> 
    </artist> 
                    <album> 
            <name>Tales From Another World CD1</name> 
            <position></position> 
        </album> 
        <image size="small">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="medium">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="large">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="extralarge">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
    </track> 
<track> 
    <name>Don't You (Forget About Me)</name> 
    <playcount>77</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Simple+Minds/_/Don%27t+You+%28Forget+About+Me%29</url> 
    <duration>260000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Simple Minds</name> 
        <mbid>f41490ce-fe39-435d-86c0-ab5ce098b423</mbid> 
        <url>http://www.last.fm/music/Simple+Minds</url> 
    </artist> 
                    <album> 
            <name>Glittering Prize</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B000054A1L.01._SCMZZZZZZZ_.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B000054A1L.01._SCMZZZZZZZ_.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B000054A1L.01._SCMZZZZZZZ_.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B000054A1L.01._SCMZZZZZZZ_.jpg</image> 
    </track> 
<track> 
    <name>Speed Your Love To Me</name> 
    <playcount>77</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Simple+Minds/_/Speed+Your+Love+To+Me</url> 
    <duration>243000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Simple Minds</name> 
        <mbid>f41490ce-fe39-435d-86c0-ab5ce098b423</mbid> 
        <url>http://www.last.fm/music/Simple+Minds</url> 
    </artist> 
                    <album> 
            <name>The best of</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/51126317.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/51126317.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/51126317.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/51126317.jpg</image> 
    </track> 
<track> 
    <name>Sense Of Life</name> 
    <playcount>75</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Plastic/_/Sense+Of+Life</url> 
    <duration>333000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Plastic</name> 
        <mbid>2ae43e8b-8489-44d9-a50e-4c10a8f765d6</mbid> 
        <url>http://www.last.fm/music/Plastic</url> 
    </artist> 
                    <album> 
            <name>Black Colours</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
    </track> 
<track> 
    <name>Drive</name> 
    <playcount>73</playcount> 
    <tagcount>2</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Assemblage+23/_/Drive</url> 
    <duration>310000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Assemblage 23</name> 
        <mbid>1626de1a-509a-413f-82de-a362a2fd14a3</mbid> 
        <url>http://www.last.fm/music/Assemblage+23</url> 
    </artist> 
                    <album> 
            <name>Defiance</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/8679471.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/8679471.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/8679471.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/8679471.jpg</image> 
    </track> 
<track> 
    <name>Ignorance</name> 
    <playcount>73</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/NamNamBulu/_/Ignorance</url> 
    <duration>305000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>NamNamBulu</name> 
        <mbid>aff48c86-899b-490f-b5e4-39e80d43465c</mbid> 
        <url>http://www.last.fm/music/NamNamBulu</url> 
    </artist> 
                    <album> 
            <name>Distances</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0001KREF8.01.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0001KREF8.01.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0001KREF8.01.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0001KREF8.01.MZZZZZZZ.jpg</image> 
    </track> 
<track> 
    <name>Identity</name> 
    <playcount>71</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Identity</url> 
    <duration>343000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Mind.In.A.Box</name> 
        <mbid>6fe25812-9155-43a1-b5af-8371f90a4f59</mbid> 
        <url>http://www.last.fm/music/Mind.In.A.Box</url> 
    </artist> 
                    <album> 
            <name>Crossroads</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/9964547.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/9964547.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/9964547.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/9964547.jpg</image> 
    </track> 
<track> 
    <name>Unfinished Sympathy</name> 
    <playcount>70</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Massive+Attack/_/Unfinished+Sympathy</url> 
    <duration>307000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Massive Attack</name> 
        <mbid>10adbe5e-a2c0-4bf3-8249-2b4cbf6e6ca8</mbid> 
        <url>http://www.last.fm/music/Massive+Attack</url> 
    </artist> 
                    <album> 
            <name>Collected CD1</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/37861757.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/37861757.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/37861757.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/37861757.jpg</image> 
    </track> 
<track> 
    <name>Hidden</name> 
    <playcount>70</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Rotersand/_/Hidden</url> 
    <duration>0</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Rotersand</name> 
        <mbid>797bcf41-0e02-431d-ab99-020e1cb3d0fd</mbid> 
        <url>http://www.last.fm/music/Rotersand</url> 
    </artist> 
                        </track> 
<track> 
    <name>The Violence In Me</name> 
    <playcount>70</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Pride+and+Fall/_/The+Violence+In+Me</url> 
    <duration>277000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Pride and Fall</name> 
        <mbid>2872431f-2440-4cca-9a11-e96852b47394</mbid> 
        <url>http://www.last.fm/music/Pride+and+Fall</url> 
    </artist> 
                    <album> 
            <name>Elements Of Silence</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/12644903.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/12644903.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/12644903.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/12644903.jpg</image> 
    </track> 
<track> 
    <name>Need to Be Proud</name> 
    <playcount>69</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Echo+Image/_/Need+to+Be+Proud</url> 
    <duration>290000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Echo Image</name> 
        <mbid>13a94709-996a-48ab-a4bf-94e1f804ea04</mbid> 
        <url>http://www.last.fm/music/Echo+Image</url> 
    </artist> 
                    <album> 
            <name>Need To Be Proud</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0000544DP.01.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0000544DP.01.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0000544DP.01.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0000544DP.01.MZZZZZZZ.jpg</image> 
    </track> 
<track> 
    <name>Visions</name> 
    <playcount>69</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Plastic/_/Visions</url> 
    <duration>259000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Plastic</name> 
        <mbid>2ae43e8b-8489-44d9-a50e-4c10a8f765d6</mbid> 
        <url>http://www.last.fm/music/Plastic</url> 
    </artist> 
                    <album> 
            <name>Black Colours</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
    </track> 
<track> 
    <name>I Can't Feel You (Mesh remix)</name> 
    <playcount>69</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Camouflage/_/I+Can%27t+Feel+You+%28Mesh+remix%29</url> 
    <duration>419000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Camouflage</name> 
        <mbid>bc6b7d82-1d7b-4f48-b742-d32936f5d5c9</mbid> 
        <url>http://www.last.fm/music/Camouflage</url> 
    </artist> 
                    <album> 
            <name>I CAN'T FEEL YOU - REMIXES CDM</name> 
            <position></position> 
        </album> 
        <image size="small">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="medium">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="large">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="extralarge">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
    </track> 
<track> 
    <name>Falling</name> 
    <playcount>69</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Falling</url> 
    <duration>277000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Mind.In.A.Box</name> 
        <mbid>6fe25812-9155-43a1-b5af-8371f90a4f59</mbid> 
        <url>http://www.last.fm/music/Mind.In.A.Box</url> 
    </artist> 
                    <album> 
            <name>Lost Alone</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/8720709.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/8720709.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/8720709.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/8720709.jpg</image> 
    </track> 
<track> 
    <name>Shiver (Lime'n'dale Remix)</name> 
    <playcount>69</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Tristraum/_/Shiver+%28Lime%27n%27dale+Remix%29</url> 
    <duration>0</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Tristraum</name> 
        <mbid>3770898c-216f-4abd-a653-56f584805d2d</mbid> 
        <url>http://www.last.fm/music/Tristraum</url> 
    </artist> 
                    <album> 
            <name>The Synthetic Music Collection CD 4</name> 
            <position></position> 
        </album> 
        <image size="small">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="medium">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="large">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="extralarge">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
    </track> 
<track> 
    <name>Lies</name> 
    <playcount>68</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Plastic/_/Lies</url> 
    <duration>302000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Plastic</name> 
        <mbid>2ae43e8b-8489-44d9-a50e-4c10a8f765d6</mbid> 
        <url>http://www.last.fm/music/Plastic</url> 
    </artist> 
                    <album> 
            <name>Black Colours</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
    </track> 
<track> 
    <name>Foreigner (original version)</name> 
    <playcount>68</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/De%252FVision/_/Foreigner+%28original+version%29</url> 
    <duration>318000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>De/Vision</name> 
        <mbid>c72c1c3d-bf05-457f-a9f7-a642bae6ca91</mbid> 
        <url>http://www.last.fm/music/De%252FVision</url> 
    </artist> 
                    <album> 
            <name>Antiquity</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B000024VJ3.03.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B000024VJ3.03.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B000024VJ3.03.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B000024VJ3.03.MZZZZZZZ.jpg</image> 
    </track> 
<track> 
    <name>Sorry</name> 
    <playcount>68</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Assemblage+23/_/Sorry</url> 
    <duration>331000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Assemblage 23</name> 
        <mbid>1626de1a-509a-413f-82de-a362a2fd14a3</mbid> 
        <url>http://www.last.fm/music/Assemblage+23</url> 
    </artist> 
                    <album> 
            <name>Meta</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/3640507.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/3640507.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/3640507.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/3640507.jpg</image> 
    </track> 
<track> 
    <name>Closed Eyes</name> 
    <playcount>66</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Plastic/_/Closed+Eyes</url> 
    <duration>290000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Plastic</name> 
        <mbid>2ae43e8b-8489-44d9-a50e-4c10a8f765d6</mbid> 
        <url>http://www.last.fm/music/Plastic</url> 
    </artist> 
                    <album> 
            <name>Black Colours</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0000DCXTV.01._SCMZZZZZZZ_.jpg</image> 
    </track> 
<track> 
    <name>Clear</name> 
    <playcount>66</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Minerve/_/Clear</url> 
    <duration>264000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Minerve</name> 
        <mbid>b93145c8-3734-4c19-91c4-8b4b6b34f2d9</mbid> 
        <url>http://www.last.fm/music/Minerve</url> 
    </artist> 
                    <album> 
            <name>The Synthetic Music Collection CD 4</name> 
            <position></position> 
        </album> 
        <image size="small">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="medium">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="large">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="extralarge">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
    </track> 
<track> 
    <name>Escape</name> 
    <playcount>66</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Minerve/_/Escape</url> 
    <duration>278000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Minerve</name> 
        <mbid>b93145c8-3734-4c19-91c4-8b4b6b34f2d9</mbid> 
        <url>http://www.last.fm/music/Minerve</url> 
    </artist> 
                    <album> 
            <name>Breathing Avenue</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
    </track> 
<track> 
    <name>Merge</name> 
    <playcount>66</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Minerve/_/Merge</url> 
    <duration>300000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Minerve</name> 
        <mbid>b93145c8-3734-4c19-91c4-8b4b6b34f2d9</mbid> 
        <url>http://www.last.fm/music/Minerve</url> 
    </artist> 
                    <album> 
            <name>Breathing Avenue</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
    </track> 
<track> 
    <name>Only In My Mind</name> 
    <playcount>66</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Imperative+Reaction/_/Only+In+My+Mind</url> 
    <duration>285000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Imperative Reaction</name> 
        <mbid>96cd8ef6-2873-485f-843f-f3ced9839791</mbid> 
        <url>http://www.last.fm/music/Imperative+Reaction</url> 
    </artist> 
                    <album> 
            <name>As We Fall</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/12332627.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/12332627.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/12332627.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/12332627.jpg</image> 
    </track> 
<track> 
    <name>Mantrap - A Wish Come True</name> 
    <playcount>65</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Beborn+Beton/_/Mantrap+-+A+Wish+Come+True</url> 
    <duration>265000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Beborn Beton</name> 
        <mbid>b982e7e7-bbed-4c86-91c4-db5267e3cc9b</mbid> 
        <url>http://www.last.fm/music/Beborn+Beton</url> 
    </artist> 
                    <album> 
            <name>Tales From Another World (CD</name> 
            <position></position> 
        </album> 
        <image size="small">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="medium">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="large">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="extralarge">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
    </track> 
<track> 
    <name>Horror Show</name> 
    <playcount>65</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/The+Birthday+Massacre/_/Horror+Show</url> 
    <duration>246000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>The Birthday Massacre</name> 
        <mbid>83d8a06a-4145-444a-b4ae-49e1e986206f</mbid> 
        <url>http://www.last.fm/music/The+Birthday+Massacre</url> 
    </artist> 
                    <album> 
            <name>Violet</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/47629523.png</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/47629523.png</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/47629523.png</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/47629523.png</image> 
    </track> 
<track> 
    <name>Tragic Figure</name> 
    <playcount>65</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Assemblage+23/_/Tragic+Figure</url> 
    <duration>272000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Assemblage 23</name> 
        <mbid>1626de1a-509a-413f-82de-a362a2fd14a3</mbid> 
        <url>http://www.last.fm/music/Assemblage+23</url> 
    </artist> 
                    <album> 
            <name>Let The Wind Erase ME CDM</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/37010437.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/37010437.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/37010437.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/37010437.jpg</image> 
    </track> 
<track> 
    <name>Alone</name> 
    <playcount>65</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/NamNamBulu/_/Alone</url> 
    <duration>364000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>NamNamBulu</name> 
        <mbid>aff48c86-899b-490f-b5e4-39e80d43465c</mbid> 
        <url>http://www.last.fm/music/NamNamBulu</url> 
    </artist> 
                    <album> 
            <name>Alone</name> 
            <position></position> 
        </album> 
        <image size="small">http://cdbaby.name/n/a/namnambulu3.jpg</image> 
        <image size="medium">http://cdbaby.name/n/a/namnambulu3.jpg</image> 
        <image size="large">http://cdbaby.name/n/a/namnambulu3.jpg</image> 
        <image size="extralarge">http://cdbaby.name/n/a/namnambulu3.jpg</image> 
    </track> 
<track> 
    <name>Run For Your Life</name> 
    <playcount>64</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Run+For+Your+Life</url> 
    <duration>267000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Mind.In.A.Box</name> 
        <mbid>6fe25812-9155-43a1-b5af-8371f90a4f59</mbid> 
        <url>http://www.last.fm/music/Mind.In.A.Box</url> 
    </artist> 
                    <album> 
            <name>Crossroads</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/9964547.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/9964547.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/9964547.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/9964547.jpg</image> 
    </track> 
<track> 
    <name>Light</name> 
    <playcount>63</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Assemblage+23/_/Light</url> 
    <duration>266000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Assemblage 23</name> 
        <mbid>1626de1a-509a-413f-82de-a362a2fd14a3</mbid> 
        <url>http://www.last.fm/music/Assemblage+23</url> 
    </artist> 
                    <album> 
            <name>Defiance</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/8679471.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/8679471.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/8679471.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/8679471.jpg</image> 
    </track> 
<track> 
    <name>Stalkers</name> 
    <playcount>63</playcount> 
    <tagcount>2</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Stalkers</url> 
    <duration>372000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Mind.In.A.Box</name> 
        <mbid>6fe25812-9155-43a1-b5af-8371f90a4f59</mbid> 
        <url>http://www.last.fm/music/Mind.In.A.Box</url> 
    </artist> 
                    <album> 
            <name>Crossroads</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/9964547.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/9964547.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/9964547.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/9964547.jpg</image> 
    </track> 
<track> 
    <name>Morning Night and Day</name> 
    <playcount>62</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/New+Order/_/Morning+Night+and+Day</url> 
    <duration>307000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>New Order</name> 
        <mbid>f1106b17-dcbb-45f6-b938-199ccfab50cc</mbid> 
        <url>http://www.last.fm/music/New+Order</url> 
    </artist> 
                    <album> 
            <name>Waiting for the Sirens' Call</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/8678521.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/8678521.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/8678521.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/8678521.jpg</image> 
    </track> 
<track> 
    <name>By the Waters</name> 
    <playcount>62</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Rotersand/_/By+the+Waters</url> 
    <duration>367000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Rotersand</name> 
        <mbid>797bcf41-0e02-431d-ab99-020e1cb3d0fd</mbid> 
        <url>http://www.last.fm/music/Rotersand</url> 
    </artist> 
                    <album> 
            <name>Welcome To Goodbye</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/8737123.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/8737123.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/8737123.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/8737123.jpg</image> 
    </track> 
<track> 
    <name>Into The Night</name> 
    <playcount>62</playcount> 
    <tagcount>2</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Into+The+Night</url> 
    <duration>432000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Mind.In.A.Box</name> 
        <mbid>6fe25812-9155-43a1-b5af-8371f90a4f59</mbid> 
        <url>http://www.last.fm/music/Mind.In.A.Box</url> 
    </artist> 
                    <album> 
            <name>Crossroads</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/9964547.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/9964547.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/9964547.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/9964547.jpg</image> 
    </track> 
<track> 
    <name>Moments (Duett Version) (Feat. Endanger)</name> 
    <playcount>62</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/NamNamBulu/_/Moments+%28Duett+Version%29+%28Feat.+Endanger%29</url> 
    <duration>263000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>NamNamBulu</name> 
        <mbid>aff48c86-899b-490f-b5e4-39e80d43465c</mbid> 
        <url>http://www.last.fm/music/NamNamBulu</url> 
    </artist> 
                    <album> 
            <name>Alone</name> 
            <position></position> 
        </album> 
        <image size="small">http://cdbaby.name/n/a/namnambulu3.jpg</image> 
        <image size="medium">http://cdbaby.name/n/a/namnambulu3.jpg</image> 
        <image size="large">http://cdbaby.name/n/a/namnambulu3.jpg</image> 
        <image size="extralarge">http://cdbaby.name/n/a/namnambulu3.jpg</image> 
    </track> 
<track> 
    <name>Now or Never</name> 
    <playcount>61</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/NamNamBulu/_/Now+or+Never</url> 
    <duration>290000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>NamNamBulu</name> 
        <mbid>aff48c86-899b-490f-b5e4-39e80d43465c</mbid> 
        <url>http://www.last.fm/music/NamNamBulu</url> 
    </artist> 
                    <album> 
            <name>blind ep</name> 
            <position></position> 
        </album> 
        <image size="small">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="medium">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="large">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
        <image size="extralarge">http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png</image> 
    </track> 
<track> 
    <name>Fear</name> 
    <playcount>61</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Fear</url> 
    <duration>358000</duration> 
    <streamable fulltrack="0">1</streamable> 
        <artist> 
        <name>Mind.In.A.Box</name> 
        <mbid>6fe25812-9155-43a1-b5af-8371f90a4f59</mbid> 
        <url>http://www.last.fm/music/Mind.In.A.Box</url> 
    </artist> 
                    <album> 
            <name>Crossroads</name> 
            <position></position> 
        </album> 
        <image size="small">http://userserve-ak.last.fm/serve/34s/9964547.jpg</image> 
        <image size="medium">http://userserve-ak.last.fm/serve/64s/9964547.jpg</image> 
        <image size="large">http://userserve-ak.last.fm/serve/126/9964547.jpg</image> 
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/9964547.jpg</image> 
    </track> 
<track> 
    <name>My World (Exclusive)</name> 
    <playcount>60</playcount> 
    <tagcount>0</tagcount> 
    <mbid></mbid> 
    <url>http://www.last.fm/music/Colony+5/_/My+World+%28Exclusive%29</url> 
    <duration>220000</duration> 
    <streamable fulltrack="0">0</streamable> 
        <artist> 
        <name>Colony 5</name> 
        <mbid>0dc6a8e4-30d5-43a3-b3d2-98bdd8c43362</mbid> 
        <url>http://www.last.fm/music/Colony+5</url> 
    </artist> 
                    <album> 
            <name>Black</name> 
            <position></position> 
        </album> 
        <image size="small">http://images.amazon.com/images/P/B00008Z5E2.03.MZZZZZZZ.jpg</image> 
        <image size="medium">http://images.amazon.com/images/P/B00008Z5E2.03.MZZZZZZZ.jpg</image> 
        <image size="large">http://images.amazon.com/images/P/B00008Z5E2.03.MZZZZZZZ.jpg</image> 
        <image size="extralarge">http://images.amazon.com/images/P/B00008Z5E2.03.MZZZZZZZ.jpg</image> 
    </track> 
</tracks></lfm>
"""

    handler=Handler(debug=False)
    process(r_test, handler)
    print handler.tracks
    pp=handler.page_props["tracks.attrs"]
    print "perPage: %s, totalPages: %s" % (pp["perPage"], pp["totalPages"])
    
    """
    [{u'name': u'Merging Oceans', 'artist.name': u'Rotersand', u'url': u'http://www.last.fm/music/Rotersand/_/Merging+Oceans', 'artist.url': u'http://www.last.fm/music/Rotersand', u'mbid': u'', 'artist.mbid': u'797bcf41-0e02-431d-ab99-020e1cb3d0fd', u'playcount': u'101'}, 
    {u'name': u'Surviving (Synth Amok Remix)', 'artist.name': u'NamNamBulu', u'url': u'http://www.last.fm/music/NamNamBulu/_/Surviving+%28Synth+Amok+Remix%29', 'artist.url': u'http://www.last.fm/music/NamNamBulu', u'mbid': u'', 'artist.mbid': u'aff48c86-899b-490f-b5e4-39e80d43465c', u'playcount': u'98'}, {u'name': u'Introspection', 'artist.name': u'Mind.In.A.Box', u'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Introspection', 'artist.url': u'http://www.last.fm/music/Mind.In.A.Box', u'mbid': u'', 'artist.mbid': u'6fe25812-9155-43a1-b5af-8371f90a4f59', u'playcount': u'91'}, {u'name': u'Protection', 'artist.name': u'Massive Attack', u'url': u'http://www.last.fm/music/Massive+Attack/_/Protection', 'artist.url': u'http://www.last.fm/music/Massive+Attack', u'mbid': u'', 'artist.mbid': u'10adbe5e-a2c0-4bf3-8249-2b4cbf6e6ca8', u'playcount': u'90'}, {u'name': u'Safe From Harm', 'artist.name': u'Massive Attack', u'url': u'http://www.last.fm/music/Massive+Attack/_/Safe+From+Harm', 'artist.url': u'http://www.last.fm/music/Massive+Attack', u'mbid': u'', 'artist.mbid': u'10adbe5e-a2c0-4bf3-8249-2b4cbf6e6ca8', u'playcount': u'88'}, {u'name': u'Change', 'artist.name': u'Mind.In.A.Box', u'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Change', 'artist.url': u'http://www.last.fm/music/Mind.In.A.Box', u'mbid': u'', 'artist.mbid': u'6fe25812-9155-43a1-b5af-8371f90a4f59', u'playcount': u'85'}, {u'name': u'Amnesia', 'artist.name': u'Mind.In.A.Box', u'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Amnesia', 'artist.url': u'http://www.last.fm/music/Mind.In.A.Box', u'mbid': u'', 'artist.mbid': u'6fe25812-9155-43a1-b5af-8371f90a4f59', u'playcount': u'85'}, {u'name': u'Vanishing Point', 'artist.name': u'New Order', u'url': u'http://www.last.fm/music/New+Order/_/Vanishing+Point', 'artist.url': u'http://www.last.fm/music/New+Order', u'mbid': u'', 'artist.mbid': u'f1106b17-dcbb-45f6-b938-199ccfab50cc', u'playcount': u'83'}, {u'name': u'Suffocate', 'artist.name': u'Minerve', u'url': u'http://www.last.fm/music/Minerve/_/Suffocate', 'artist.url': u'http://www.last.fm/music/Minerve', u'mbid': u'', 'artist.mbid': u'b93145c8-3734-4c19-91c4-8b4b6b34f2d9', u'playcount': u'82'}, {u'name': u'What Your Soul Sings', 'artist.name': u'Massive Attack', u'url': u'http://www.last.fm/music/Massive+Attack/_/What+Your+Soul+Sings', 'artist.url': u'http://www.last.fm/music/Massive+Attack', u'mbid': u'', 'artist.mbid': u'10adbe5e-a2c0-4bf3-8249-2b4cbf6e6ca8', u'playcount': u'81'}, {u'name': u'Afraid of Myself', 'artist.name': u'Minerve', u'url': u'http://www.last.fm/music/Minerve/_/Afraid+of+Myself', 'artist.url': u'http://www.last.fm/music/Minerve', u'mbid': u'', 'artist.mbid': u'b93145c8-3734-4c19-91c4-8b4b6b34f2d9', u'playcount': u'80'}, {u'name': u'All The Things She Said', 'artist.name': u'Simple Minds', u'url': u'http://www.last.fm/music/Simple+Minds/_/All+The+Things+She+Said', 'artist.url': u'http://www.last.fm/music/Simple+Minds', u'mbid': u'', 'artist.mbid': u'f41490ce-fe39-435d-86c0-ab5ce098b423', u'playcount': u'79'}, {u'name': u'Lost Little Robot', 'artist.name': u'Beborn Beton', u'url': u'http://www.last.fm/music/Beborn+Beton/_/Lost+Little+Robot', 'artist.url': u'http://www.last.fm/music/Beborn+Beton', u'mbid': u'', 'artist.mbid': u'b982e7e7-bbed-4c86-91c4-db5267e3cc9b', u'playcount': u'79'}, {u'name': u"Don't You (Forget About Me)", 'artist.name': u'Simple Minds', u'url': u'http://www.last.fm/music/Simple+Minds/_/Don%27t+You+%28Forget+About+Me%29', 'artist.url': u'http://www.last.fm/music/Simple+Minds', u'mbid': u'', 'artist.mbid': u'f41490ce-fe39-435d-86c0-ab5ce098b423', u'playcount': u'77'}, {u'name': u'Speed Your Love To Me', 'artist.name': u'Simple Minds', u'url': u'http://www.last.fm/music/Simple+Minds/_/Speed+Your+Love+To+Me', 'artist.url': u'http://www.last.fm/music/Simple+Minds', u'mbid': u'', 'artist.mbid': u'f41490ce-fe39-435d-86c0-ab5ce098b423', u'playcount': u'77'}, {u'name': u'Sense Of Life', 'artist.name': u'Plastic', u'url': u'http://www.last.fm/music/Plastic/_/Sense+Of+Life', 'artist.url': u'http://www.last.fm/music/Plastic', u'mbid': u'', 'artist.mbid': u'2ae43e8b-8489-44d9-a50e-4c10a8f765d6', u'playcount': u'75'}, {u'name': u'Drive', 'artist.name': u'Assemblage 23', u'url': u'http://www.last.fm/music/Assemblage+23/_/Drive', 'artist.url': u'http://www.last.fm/music/Assemblage+23', u'mbid': u'', 'artist.mbid': u'1626de1a-509a-413f-82de-a362a2fd14a3', u'playcount': u'73'}, {u'name': u'Ignorance', 'artist.name': u'NamNamBulu', u'url': u'http://www.last.fm/music/NamNamBulu/_/Ignorance', 'artist.url': u'http://www.last.fm/music/NamNamBulu', u'mbid': u'', 'artist.mbid': u'aff48c86-899b-490f-b5e4-39e80d43465c', u'playcount': u'73'}, {u'name': u'Identity', 'artist.name': u'Mind.In.A.Box', u'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Identity', 'artist.url': u'http://www.last.fm/music/Mind.In.A.Box', u'mbid': u'', 'artist.mbid': u'6fe25812-9155-43a1-b5af-8371f90a4f59', u'playcount': u'71'}, {u'name': u'Unfinished Sympathy', 'artist.name': u'Massive Attack', u'url': u'http://www.last.fm/music/Massive+Attack/_/Unfinished+Sympathy', 'artist.url': u'http://www.last.fm/music/Massive+Attack', u'mbid': u'', 'artist.mbid': u'10adbe5e-a2c0-4bf3-8249-2b4cbf6e6ca8', u'playcount': u'70'}, {u'name': u'Hidden', 'artist.name': u'Rotersand', u'url': u'http://www.last.fm/music/Rotersand/_/Hidden', 'artist.url': u'http://www.last.fm/music/Rotersand', u'mbid': u'', 'artist.mbid': u'797bcf41-0e02-431d-ab99-020e1cb3d0fd', u'playcount': u'70'}, {u'name': u'The Violence In Me', 'artist.name': u'Pride and Fall', u'url': u'http://www.last.fm/music/Pride+and+Fall/_/The+Violence+In+Me', 'artist.url': u'http://www.last.fm/music/Pride+and+Fall', u'mbid': u'', 'artist.mbid': u'2872431f-2440-4cca-9a11-e96852b47394', u'playcount': u'70'}, {u'name': u'Need to Be Proud', 'artist.name': u'Echo Image', u'url': u'http://www.last.fm/music/Echo+Image/_/Need+to+Be+Proud', 'artist.url': u'http://www.last.fm/music/Echo+Image', u'mbid': u'', 'artist.mbid': u'13a94709-996a-48ab-a4bf-94e1f804ea04', u'playcount': u'69'}, {u'name': u'Visions', 'artist.name': u'Plastic', u'url': u'http://www.last.fm/music/Plastic/_/Visions', 'artist.url': u'http://www.last.fm/music/Plastic', u'mbid': u'', 'artist.mbid': u'2ae43e8b-8489-44d9-a50e-4c10a8f765d6', u'playcount': u'69'}, {u'name': u"I Can't Feel You (Mesh remix)", 'artist.name': u'Camouflage', u'url': u'http://www.last.fm/music/Camouflage/_/I+Can%27t+Feel+You+%28Mesh+remix%29', 'artist.url': u'http://www.last.fm/music/Camouflage', u'mbid': u'', 'artist.mbid': u'bc6b7d82-1d7b-4f48-b742-d32936f5d5c9', u'playcount': u'69'}, {u'name': u'Falling', 'artist.name': u'Mind.In.A.Box', u'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Falling', 'artist.url': u'http://www.last.fm/music/Mind.In.A.Box', u'mbid': u'', 'artist.mbid': u'6fe25812-9155-43a1-b5af-8371f90a4f59', u'playcount': u'69'}, {u'name': u"Shiver (Lime'n'dale Remix)", 'artist.name': u'Tristraum', u'url': u'http://www.last.fm/music/Tristraum/_/Shiver+%28Lime%27n%27dale+Remix%29', 'artist.url': u'http://www.last.fm/music/Tristraum', u'mbid': u'', 'artist.mbid': u'3770898c-216f-4abd-a653-56f584805d2d', u'playcount': u'69'}, {u'name': u'Lies', 'artist.name': u'Plastic', u'url': u'http://www.last.fm/music/Plastic/_/Lies', 'artist.url': u'http://www.last.fm/music/Plastic', u'mbid': u'', 'artist.mbid': u'2ae43e8b-8489-44d9-a50e-4c10a8f765d6', u'playcount': u'68'}, {u'name': u'Foreigner (original version)', 'artist.name': u'De/Vision', u'url': u'http://www.last.fm/music/De%252FVision/_/Foreigner+%28original+version%29', 'artist.url': u'http://www.last.fm/music/De%252FVision', u'mbid': u'', 'artist.mbid': u'c72c1c3d-bf05-457f-a9f7-a642bae6ca91', u'playcount': u'68'}, {u'name': u'Sorry', 'artist.name': u'Assemblage 23', u'url': u'http://www.last.fm/music/Assemblage+23/_/Sorry', 'artist.url': u'http://www.last.fm/music/Assemblage+23', u'mbid': u'', 'artist.mbid': u'1626de1a-509a-413f-82de-a362a2fd14a3', u'playcount': u'68'}, {u'name': u'Closed Eyes', 'artist.name': u'Plastic', u'url': u'http://www.last.fm/music/Plastic/_/Closed+Eyes', 'artist.url': u'http://www.last.fm/music/Plastic', u'mbid': u'', 'artist.mbid': u'2ae43e8b-8489-44d9-a50e-4c10a8f765d6', u'playcount': u'66'}, {u'name': u'Clear', 'artist.name': u'Minerve', u'url': u'http://www.last.fm/music/Minerve/_/Clear', 'artist.url': u'http://www.last.fm/music/Minerve', u'mbid': u'', 'artist.mbid': u'b93145c8-3734-4c19-91c4-8b4b6b34f2d9', u'playcount': u'66'}, {u'name': u'Escape', 'artist.name': u'Minerve', u'url': u'http://www.last.fm/music/Minerve/_/Escape', 'artist.url': u'http://www.last.fm/music/Minerve', u'mbid': u'', 'artist.mbid': u'b93145c8-3734-4c19-91c4-8b4b6b34f2d9', u'playcount': u'66'}, {u'name': u'Merge', 'artist.name': u'Minerve', u'url': u'http://www.last.fm/music/Minerve/_/Merge', 'artist.url': u'http://www.last.fm/music/Minerve', u'mbid': u'', 'artist.mbid': u'b93145c8-3734-4c19-91c4-8b4b6b34f2d9', u'playcount': u'66'}, {u'name': u'Only In My Mind', 'artist.name': u'Imperative Reaction', u'url': u'http://www.last.fm/music/Imperative+Reaction/_/Only+In+My+Mind', 'artist.url': u'http://www.last.fm/music/Imperative+Reaction', u'mbid': u'', 'artist.mbid': u'96cd8ef6-2873-485f-843f-f3ced9839791', u'playcount': u'66'}, {u'name': u'Mantrap - A Wish Come True', 'artist.name': u'Beborn Beton', u'url': u'http://www.last.fm/music/Beborn+Beton/_/Mantrap+-+A+Wish+Come+True', 'artist.url': u'http://www.last.fm/music/Beborn+Beton', u'mbid': u'', 'artist.mbid': u'b982e7e7-bbed-4c86-91c4-db5267e3cc9b', u'playcount': u'65'}, {u'name': u'Horror Show', 'artist.name': u'The Birthday Massacre', u'url': u'http://www.last.fm/music/The+Birthday+Massacre/_/Horror+Show', 'artist.url': u'http://www.last.fm/music/The+Birthday+Massacre', u'mbid': u'', 'artist.mbid': u'83d8a06a-4145-444a-b4ae-49e1e986206f', u'playcount': u'65'}, {u'name': u'Tragic Figure', 'artist.name': u'Assemblage 23', u'url': u'http://www.last.fm/music/Assemblage+23/_/Tragic+Figure', 'artist.url': u'http://www.last.fm/music/Assemblage+23', u'mbid': u'', 'artist.mbid': u'1626de1a-509a-413f-82de-a362a2fd14a3', u'playcount': u'65'}, {u'name': u'Alone', 'artist.name': u'NamNamBulu', u'url': u'http://www.last.fm/music/NamNamBulu/_/Alone', 'artist.url': u'http://www.last.fm/music/NamNamBulu', u'mbid': u'', 'artist.mbid': u'aff48c86-899b-490f-b5e4-39e80d43465c', u'playcount': u'65'}, {u'name': u'Run For Your Life', 'artist.name': u'Mind.In.A.Box', u'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Run+For+Your+Life', 'artist.url': u'http://www.last.fm/music/Mind.In.A.Box', u'mbid': u'', 'artist.mbid': u'6fe25812-9155-43a1-b5af-8371f90a4f59', u'playcount': u'64'}, {u'name': u'Light', 'artist.name': u'Assemblage 23', u'url': u'http://www.last.fm/music/Assemblage+23/_/Light', 'artist.url': u'http://www.last.fm/music/Assemblage+23', u'mbid': u'', 'artist.mbid': u'1626de1a-509a-413f-82de-a362a2fd14a3', u'playcount': u'63'}, {u'name': u'Stalkers', 'artist.name': u'Mind.In.A.Box', u'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Stalkers', 'artist.url': u'http://www.last.fm/music/Mind.In.A.Box', u'mbid': u'', 'artist.mbid': u'6fe25812-9155-43a1-b5af-8371f90a4f59', u'playcount': u'63'}, {u'name': u'Morning Night and Day', 'artist.name': u'New Order', u'url': u'http://www.last.fm/music/New+Order/_/Morning+Night+and+Day', 'artist.url': u'http://www.last.fm/music/New+Order', u'mbid': u'', 'artist.mbid': u'f1106b17-dcbb-45f6-b938-199ccfab50cc', u'playcount': u'62'}, {u'name': u'By the Waters', 'artist.name': u'Rotersand', u'url': u'http://www.last.fm/music/Rotersand/_/By+the+Waters', 'artist.url': u'http://www.last.fm/music/Rotersand', u'mbid': u'', 'artist.mbid': u'797bcf41-0e02-431d-ab99-020e1cb3d0fd', u'playcount': u'62'}, {u'name': u'Into The Night', 'artist.name': u'Mind.In.A.Box', u'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Into+The+Night', 'artist.url': u'http://www.last.fm/music/Mind.In.A.Box', u'mbid': u'', 'artist.mbid': u'6fe25812-9155-43a1-b5af-8371f90a4f59', u'playcount': u'62'}, {u'name': u'Moments (Duett Version) (Feat. Endanger)', 'artist.name': u'NamNamBulu', u'url': u'http://www.last.fm/music/NamNamBulu/_/Moments+%28Duett+Version%29+%28Feat.+Endanger%29', 'artist.url': u'http://www.last.fm/music/NamNamBulu', u'mbid': u'', 'artist.mbid': u'aff48c86-899b-490f-b5e4-39e80d43465c', u'playcount': u'62'}, {u'name': u'Now or Never', 'artist.name': u'NamNamBulu', u'url': u'http://www.last.fm/music/NamNamBulu/_/Now+or+Never', 'artist.url': u'http://www.last.fm/music/NamNamBulu', u'mbid': u'', 'artist.mbid': u'aff48c86-899b-490f-b5e4-39e80d43465c', u'playcount': u'61'}, {u'name': u'Fear', 'artist.name': u'Mind.In.A.Box', u'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Fear', 'artist.url': u'http://www.last.fm/music/Mind.In.A.Box', u'mbid': u'', 'artist.mbid': u'6fe25812-9155-43a1-b5af-8371f90a4f59', u'playcount': u'61'}, {u'name': u'My World (Exclusive)', 'artist.name': u'Colony 5', u'url': u'http://www.last.fm/music/Colony+5/_/My+World+%28Exclusive%29', 'artist.url': u'http://www.last.fm/music/Colony+5', u'mbid': u'', 'artist.mbid': u'0dc6a8e4-30d5-43a3-b3d2-98bdd8c43362', u'playcount': u'60'}]
    """