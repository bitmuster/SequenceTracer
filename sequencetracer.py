#! /usr/bin/python3

# 
# This work was inspired by Zooko O'Whielacronx's trace.py
#
# python3 sequencetracer.py  > diag.diag
# seqdiag3 -T svg diag.diag
#
import sys
import linecache

scipt_path = "/home/micha/Dump/CodeLand/AnyMate"
cmd = "AnyMate.main( ['AnyMate.py', '--nogui', 'greet', '../AnyMate/template.anymate'] ) "

scipt_path = "./"
cmd = "sample_code.main()"

sys.path.append(scipt_path)

#import AnyMate
import sample_code

stack=[]

def localtracer(frame, event, arg):
    #print (event)
    #print (type(frame))
    line=frame.f_lineno
    filename=frame.f_code.co_filename
    code=linecache.getline(filename, line)
    if event == "return":
        if len(stack)>=2:
            print( "    " + stack[-2][0] + " <-- " + stack[-1][0] + ";")
        del stack[-1]
    #print( "local ", event, filename, line, code)

def globaltrace(frame, event, arg):
    #print(event)
    #print(type(frame))
    line=frame.f_lineno
    filename=frame.f_code.co_filename
    name = frame.f_code.co_name
    code=linecache.getline(filename, line)
    if "self" in frame.f_locals:
        classname= frame.f_locals["self"].__class__.__qualname__
    else:
        classname="NN"
    #print( "global", event, filename, line, classname, name, code)
    if event=="call":
        if stack:
            print( "    " + stack[-1][0] + " -> ", end="" )
            stack.append((classname,name))
            print( stack[-1][0] + " [label = \"" +stack[-1][1] + "\"];")
        else:
            stack.append((classname,name))

    #print(stack)
    return localtracer




sys.settrace(globaltrace)

print("seqdiag {")

exec(cmd )

print("}")
