def prepare():
    global os
    import os
    return("FS: LOADED")

def ext(fname):
    fname = fname.split(".")
    return(fname[len(fname) - 1])

def isdir(dir):
    if os.path.isdir(os.getcwd() + "/data/osroot/" + dir):
        return(True)
    elif os.path.isdir(os.getcwd() + "\\data\\osroot\\" + dir.replace("/", "\\")):
        return(True)
    else:
        return(False)

def ls(dir = ""):
    try:
        h = os.listdir(os.getcwd() + "/data/osroot/" + dir)
    except:
        h = os.listdir(os.getcwd() + "\\data\\osroot\\" + dir.replace("/", "\\"))
    return(h)

def cd(cdir, ndir):
    if isdir(cdir + ndir):
        return(cdir + ndir)
    else:
        return(cdir)
