#!/usr/bin/env python
"""
    Parse RFC text

    Created on 2012-12-25
    @author: jldupont
    
Format:
    
    [optional] blank lines
    Header
    Blank line(s)
    Title line(s)
    Blank line(s)
    Text
    
Header:
    Contains date in various formats, right-hand side
    May contain "References:" 
    May contain "Updates: "
    May contain "Category: "
    
RFC
    RFC XXXX
    RFC-XXXX
   
DATE:
    Month YYYY
    dd Month YYYY
    dd-Month'-YY
    
"""

import sys, os, re, json
import functools

MONTHS=[
        "january", "february", "march", 
        "april", "may", "june", 
        "july", "august", "september", 
        "october", "november", "december",
        
        "jan", "feb", "mar", 
        "apr", "may", "jun",
        "jul", "aug", "sep",
        "oct", "nov", "dec"
        ]

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
def top(_gctx, nxt):
    """   
    """
    try:
        linenum=0
        while True:
            msg=(yield)
            (_code, (filename, lines))=msg
            nxt.send(("start", filename))
            for line in lines:
                line=line.strip()
                nxt.send(("line", (linenum, line)))
                linenum=linenum+1
            nxt.send(("end", filename))
            

    except Exception, e:
        sys.stderr.write("top: excep: %s filename=%s" % (str(e), filename))
        

@coroutine
def proc1(_gctx, nxt):
    """
    [Blank line(s)]
    Header fields
    Blank line(s)
    Title line(s)
    Blank line(s)
    """
    try:
        state="top"
        linenum="?"
        current_filename=None
        header=[]
        while True:
            msg=(yield)
            (code, data)=msg
            if code=="start":
                state="top"
                header=[]
                current_filename=data
                nxt.send(msg)
                continue
            if code=="end":
                state="top"
                nxt.send(("end", data))
                continue
            if code=="line":
                linenum, line=data
                
                if state=="top":
                    if len(line)==0:
                        continue
                    state="header"
                    header.append(line)
                    continue
                if state=="header":
                    if len(line)==0:
                        state="blanks2"
                        continue
                    header.append(line)
                    continue
                if state=="blanks2":
                    if len(line)==0:
                        continue
                    state="title"
                    continue
                if state=="title":
                    if len(line)==0:
                        continue
                    state="blanks3"
                    continue
                if state=="blanks3":
                    if len(line)==0:
                        continue
                    nxt.send(("header", header))
                    state="body"
                    nxt.send(("body", line))
                    continue
                if state=="body":
                    nxt.send(("body", line))
                    continue
                
            

    except Exception, e:
        sys.stderr.write("proc1: exc(%s): filename: %s, linenum: %s" % (str(e), current_filename, linenum))
        

@coroutine
def header_parser(_gctx, nxt):
    try:
        current_filename=None
        while True:
            msg=(yield)
            (code, entry)=msg
            
            if code=="start":
                current_filename=entry
                nxt.send(msg)
                continue
            
            if code=="end" or code=="body":
                nxt.send(msg)
                continue
            
            if code=="header":
                header_lines=entry
                ##print "%s: header: %s" % (current_filename, entry)
                ##date=header[-1]
                ##print "%s , %s" % (current_filename, date)
                    
                tokens=tokenize(header_lines)
                    
                result=[("src", current_filename)]
                while True:
                    try:     typ, token=tokens.pop(0)
                    except:  break
                    
                    if typ=="s":
                        ## grab next token to complete
                        if token.startswith("category:"):
                            _t, n=tokens.pop(0)
                            result.append(("cat", n))
                            continue
                        
                        if token.startswith("updates:"):
                            result, tokens=handle_case_updates(result, tokens)
                            continue
                        
                    if typ=="d":
                        result.append((typ, token))
                        continue
                    
                    if typ=="m":
                        ntype, ntoken=tokens.pop(0)
                        if ntype=="i":
                            result.append(("d", "%s %s" % (token, ntoken)))
                            continue
                        continue
                    
                nxt.send(("header_entries", result))
                

    except Exception, e:
        sys.stderr.write("header_parser: entry(%s): %s" % (entry, str(e)))

@coroutine
def body(_gctx, nxt):
    """
    Finds 
        RFC xxxx
        RFC-xxxx
        RFCxxxx
        
        in the body
    """
    try:
        refs=[]
        
        while True:
            msg=(yield)
            (code, entry)=msg
            
            if code=="start":
                refs=[]
            
            if code=="end":
                nxt.send(("refs", set(refs)))
            
            if code=="body":
                line=entry
                these_refs=find_refs(line)
                refs.extend(these_refs)
                continue
                
            nxt.send(msg)

    except Exception, e:
        sys.stderr.write("tail: entry(%s): %s" % (entry, str(e)))
    
        
@coroutine
def tail(_gctx):
    try:
        current_rfc=None
        entry=[]
        while True:
            msg=(yield)
            (code, data)=msg
            
            if code=="start":
                entry=[]
                current_rfc=data
                continue
            
            if code=="header_entries":
                entry.extend(data)
                continue
                
            if code=="refs":
                data=data-set(current_rfc)
                entry.append(("refs", data))
                continue
                
            if code=="end":
                result={}
                for el in entry:
                    code, data=el
                    if code=="refs":
                        data=list(data)
                    result[code]=data
                
                print json.dumps(result)
                continue
            

    except Exception, e:
        sys.stderr.write("tail: entry(%s): %s" % (entry, str(e)))


def tokenize(lines):
    result=[]
    for hline in lines:
        line=hline.strip().lower()
        line=line.replace(",", " ")
        parts=line.split(" ")
    
        for el in parts:
            el=el.strip(".#,")
            if len(el)==0:
                continue
            try:   
                i=int(el)
                result.append(("i", i))
                continue
            except:
                pass
            
            if el in MONTHS:
                result.append(("m", el))
                continue
            
            ## maybe date of form "dd-mm-yy"
            bits=el.split("-")
            if len(bits)==3:
                result.append(("d", el))
                continue
            
            ## drop single characters e.g. '#'
            if len(el)==1:
                continue
            
            result.append(("s", el))

        result.append(("eol", None))
        
    return result

def handle_case_updates(result, tokens):
    """
        Updates: RFC # xxx
        Updates: xxxx, xxxx, xxxx    
    """
    liste=[]
    ntype, ntoken=tokens.pop(0)
    
    if not ntype=="eol":
        if ntype=="s":
            if ntoken.startswith("rfc"):
                ntype, ntoken=tokens.pop(0)
                pass
                
        while True:
            
            if ntype=="i":
                liste.append(ntoken)
                ntype, ntoken=tokens.pop(0)
                continue
            tokens.insert(0,(ntype, ntoken))
            break
        
        result.append(("upd", liste))
    
    return result, tokens


   
REGEX=re.compile( r'(rfc[\s-]?([0-9]+))+')

def find_refs(line):
    result=[]
    line=line.lower()
    line=line.replace("rfc ", "rfc-")
    parts=line.split(" ")
    for part in parts:
        match=REGEX.match(part)
        try:    
            ref=match.groups()[0].replace("-", "")
            if ref not in result:
                result.append(ref)
        except: 
            pass
    return result
        
     

def main():
    ctx={}
    liste=[top, 
           proc1,
           header_parser,
           body,
           tail
           ]
    p=build_pipeline(liste, ctx)
    
    for line in sys.stdin:
        lines=line.split("\t")
        filename=lines.pop(0)
        filename_next=os.path.splitext(filename)[0]
        p.send(("file", (filename_next, lines)))


main()
