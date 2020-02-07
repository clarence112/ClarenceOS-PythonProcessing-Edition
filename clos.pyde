add_library('minim') #for sound
import time          #for delays during startup, may end up switching to millis() and while loops

# ^^ libraries ^^ ----------------------------------------------------------------------------------------------------------------------

def setup():
    global modules
    modules = []
    global prevcycle
    prevcycle = False
    global syscolors                 #Stores definitions for commonly used colors
    syscolors = [0x00b0b3, 0xffffff] #Console background, White
    global sysmode                   #Stores the state of the system's state machine
    sysmode = 0                      #Initializes to the startup state 
    global syslog                    #Stores the log of the system console
    syslog = []                      #Initializes the system console with a message, currently blank.
    global consoleBuffers                                                                                                                         #Stores the state of the TTYs
    consoleBuffers = [["ROOT", "", "/"], ["NOUSER", "", "/"], ["NOUSER", "", "/"], ["NOUSER", "", "/"], ["NOUSER", "", "/"], ["NOUSER", "", "/"]] #[User, keyboard buffer, working directory]
    global errors                           #Stores a list of fatal and non-fatal system errors
    errors = ['~~~SYSTEM ERROR REPORT~~~']  #Initializes error list with a headder

    size(60, 60)
    fullScreen()
    looptest = True
    while looptest:
        try:
            size(displayWidth, displayHeight)
            looptest = False
        except:
            pass
    background(syscolors[0])
    global minim
    minim = Minim(this)
    global sysbeep
    sysbeep = minim.loadSample("sysbeep.wav")
    noCursor()
    time.sleep(0.5)
    sysbeep.trigger()
    time.sleep(2)
    
# ^^ prepare ^^----------------------------------------------------------------------------------------------------------------------

def report():
    global syslog
    for i in errors:
        syslog.append(i)

def draw():
    global sysmode
    global syslog
    global errors
    global timedelay
    global bootscript
    global prevcycle
    global modules
    
    if sysmode == 0:
        try:
            bootlogo = loadStrings("osroot/splash.txt")
            for i in bootlogo:
                syslog.append(i)
        except Exception, e:
            errors.append(str(e).upper())
        try:
            global consoleRender
            import consoleRender
            syslog.append(consoleRender.prepare("console.vlw", displayWidth, displayHeight))
            syslog.append('KERNEL: LINKED TO CLI DRIVER (MODULE "TERM")')
            modules.append("term")
        except Exception, e:
            errors.append(str(e).upper())
        sysmode = 1
        
    if sysmode == 1:
        try:
            global clpg
            import clpg
            syslog.append(clpg.prepare())
            syslog.append('KERNEL: LINKED TO PROGRAM INTERPRETER (MODULE "CLPG")')
            modules.append("clpg")
            sysmode = 2
        except Exception, e:
            syslog.append('KERNEL: FATAL ERROR: CANNOT LOAD MODULE "CLPG". SYSTEM CANNOT BOOT.')
            syslog.append('KERNEL: THE SPECIFIC ERROR THAT CAUSED THIS PROBLEM IS AS FOLLOWS:')
            errors.append(str(e).upper())
            sysmode = 255
            
    if sysmode == 2:
        try:
            global fileDriver
            import fileDriver
            syslog.append(fileDriver.prepare())
            syslog.append('KERNEL: LINKED TO FILESYSTEM DRIVER (MODULE "FS")')
            modules.append("fs")
            sysmode = 3
        except Exception, e:
            syslog.append('KERNEL: FATAL ERROR: CANNOT LOAD MODULE "FS". SYSTEM CANNOT BOOT.')
            syslog.append('KERNEL: THE SPECIFIC ERROR THAT CAUSED THIS PROBLEM IS AS FOLLOWS:')
            errors.append(str(e).upper())
            sysmode = 255
            
    if sysmode == 3:
        try:
            global windowManager
            import windowManager
            syslog.append(windowManager.prepare())
            syslog.append('KERNEL: LINKED TO GUI DRIVER (MODULE "WM")')
            modules.append("wm")
            sysmode = 4
        except Exception, e:
            errors.append(str(e).upper())
    
    if sysmode == 4:
        clpg.rmods(modules)
        timedelay = millis()
        syslog.append('KERNEL: PRESS "B" TO SELECT BOOT SCRIPT OR WAIT 5 SECONDS...')
        sysmode = 5
    
    if sysmode == 5:
        if timedelay + 5000 <= millis():
            bootscript = "init.clpg"
            sysmode = 6
        elif ((keyPressed) and (str(key).lower() == "b")):
            syslog.append('KERNEL: SELECT A BOOT SCRIPT FROM THE OPTIONS BELOW. YOU CANNOT BOOT A SCRIPT THAT IS NOT IN THE FILESYSTEM ROOT AND DOES NOT START WITH "TYPE:SCRIPT"')
            h = 0
            for i in fileDriver.ls():
                syslog.append(str(h) + ": " + str(i).upper())
                h = h + 1
            syslog.append("PRESS A NUMBER FROM 0 TO " + str(h - 1))
            prevcycle = True
            sysmode = 7
            
    if sysmode == 6:
        syslog.append('KERNEL: LOADING "' + bootscript.upper() + '"...')
        syslog.append('KERNEL: VERIFYING BOOT SCRIPT SYNTAX INTEGRITY...')
        i = clpg.verify("/osroot/" + bootscript)
        if i == True:
            sysmode = 8
        else:
            errors.append(i.upper())
            sysmode = 255
        
    if sysmode == 7:
        if keyPressed:
            if not prevcycle:
                try:
                    h = str(fileDriver.ls()[int(key)])
                    if fileDriver.isdir(h):
                        syslog.append('KERNEL: THAT IS NOT A FILE')
                    elif fileDriver.ext(h).lower() == "clpg":
                        bootscript = h
                        sysmode = 6
                    else:
                        syslog.append('KERNEL: THAT IS NOT A VALID FILE TYPE')
                except:
                    syslog.append('KERNEL: NOT A VAILID OPTION')
                    
    if sysmode == 8:
        clpg.addProcess("/osroot/" + bootscript)
        syslog.append('KERNEL: BOOTING!')
        consoleRender.systerm(syslog)
        time.sleep(1)
        sysmode = 256
    
    if sysmode == 254:
        time.sleep(1)
        sysbeep.trigger()
        time.sleep(1)
        sysbeep.trigger()
        time.sleep(1)
        sysbeep.trigger()
        time.sleep(2)

    if sysmode <= 255:
        if sysmode == 255:
            report()
            sysmode = 254
        try:
            consoleRender.systerm(syslog)
        except:
            pass
            
    if sysmode == 256:
        if clpg.update() == 0:
            sysmode = 254
        try:
            windowManager.update()
        except:
            pass
            
    prevcycle = keyPressed
        
#----------------------------------------------------------------------------------------------------------------------
    
def stop():
    sysbeep.close()
    minim.stop()
