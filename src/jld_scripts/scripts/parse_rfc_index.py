#!/usr/bin/env python
"""
    Created on 2012-12-25
    @author: jldupont
"""

import sys
import functools

def coroutine(func):
    """
    Decorator used for coroutine declaration
    """
    @functools.wraps(func)
    def start(*args, **kwargs):
        cr=func(*args, **kwargs)
        cr.next()
        return cr
    return start


def build_pipeline(blocks, ctx, pipe=None):
    for block in reversed(blocks):
        if pipe is None:
            pipe=block(ctx)
        else:
            pipe=block(ctx, pipe)
    return pipe

# ------------------------------------------------------

@coroutine
def top(gctx, nxt):
    """
    Skip the top lines
    
    - skip 2x "~~~" lines
    - wait for for 1st line that doesn't begin with blank or empty
    
    """
    in_header=True
    passed_tildes=0
    try:
        while True:
            msg=(yield)
            (code, (linenum, line))=msg
            
            if not in_header or code!="line":
                nxt.send(msg)
                continue
            
            line=line.strip()
            
            if passed_tildes>1:
                if len(line)==0:
                    continue

                bits=line.split(" ")
                if (len(bits)>3):
                    in_header=False
                    nxt.send(msg)
                    continue
                
            else:
                if line.startswith("~~"):
                    passed_tildes=passed_tildes+1
                    continue

    except Exception, e:
        sys.stderr.write("top: linenum(%s): %s" % (linenum, str(e)))
        

@coroutine
def acc_entry(gctx, nxt):
    """
    Accumulate entry
        Separator is empty line
    """
    try:
        acc=[]
        while True:
            msg=(yield)
            (code, (linenum, line))=msg
            line=line.strip()
            if len(line)==0:
                nxt.send(("entry", acc))
                acc=[]
                continue
            else:
                acc.append(line)
                continue

    except Exception, e:
        sys.stderr.write("in_list: linenum(%s): %s" % (linenum, str(e)))
        
        
@coroutine
def entry(gctx):
    try:
        while True:
            msg=(yield)
            (code, entry)=msg
            print entry

    except Exception, e:
        sys.stderr.write("in_list: entry(%s): %s" % (entry, str(e)))


def main():
    ctx={}
    liste=[top, 
           acc_entry,
           entry
           ]
    p=build_pipeline(liste, ctx)
    
    linenum=0
    for line in sys.stdin:
        p.send(("line", (linenum, line)))
        linenum=linenum+1

main()
