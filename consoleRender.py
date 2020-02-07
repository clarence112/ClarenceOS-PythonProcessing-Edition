import time
from textwrap import wrap

def prepare(loadfont, w, h):
    global confont
    confont = loadFont(loadfont)
    global syscolors
    syscolors = [0x00b0b3, 0xffffff]
    global dispwid 
    global disphei
    dispwid = w
    disphei = h
    return("TERM: LOADED")
    
def calclines(wwidth, wheight):
    return([floor(wwidth / 14), floor(wheight / 18)])
    
def console(textlog = ["TEST CONSOLE.", "NO INPUT DATA.", "`1234567890-=\\qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+|QWERTYUIOP{}ASDFGHJKL:" + '"' + "ZXCVBNM<>?"] , xpos = 0, ypos = 0, conwidth = 480, conheight = 360, needinput = False, conid = 0):
    textlog = fitterm(textlog, conwidth, conheight)
    if needinput:
        j = consoleBuffers[conid]
        if j[0] == "ROOT":
            textlog.append("CLOS@" + j[2].upper() + " >" + j[1])
        else:
            textlog.append(j[0] + "@" + j[2].upper() + " >" + j[1])
        if floor((millis() / 250) % 2) == 1:
            textlog[len(textlog) - 1] = textlog[len(textlog) - 1] + "_"
        else:
            textlog[len(textlog) - 1] = textlog[len(textlog) - 1] + "b"
            
    textFont(confont)
    textSize(18)
    fill(0x00, 0xb0, 0xb3)
    stroke(syscolors[0])
    rect(xpos, ypos, conwidth, conheight)
    fill(255, 255, 255)
    h = 18 + ypos
    for i in textlog:
        text(i, xpos, h)
        h = h + 18
        
def fitterm(inlog, wwidth, wheight):
    termsize = calclines(wwidth, wheight)
    outlog = []
    for i in inlog:
        h = wrap(i, termsize[0])
        for j in h:
            outlog.append(j)
    while len(outlog) >= termsize[1]:
        del outlog[0]
    return(outlog)
        
def systerm(syslog = ["H"], needinput = False):
    console(syslog, 0, 0, dispwid, disphei, needinput)
