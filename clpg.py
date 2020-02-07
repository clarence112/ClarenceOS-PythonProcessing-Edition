def prepare():
    global processes
    processes = []
    global pticker
    pticker = 0
    return("CLPG: LOADED")

def rmods(mods):
    global modules
    modules = mods
    
def verify(path):
    program = loadStrings(path)
    if program[0] == "TYPE:SCRIPT":
        k = 0
        for i in program:
            j = i.split(" ", 1)
            if j[0] == "END":
                k = k - 1
            else:
                if k > -1:
                    for h in ["DEFINE", "IF", "WHILE"]:
                        if j[0] == h:
                            k = k + 1
        if k == 0:
            return(True)
        else:
            return("Missing " + str(k) + " 'END' statements")
    else:
        return("Not a script")
            

def addProcess(path, procid = "auto"):
    global processes
    global pticker
    if procid == "auto":
        processes.append(process(path, pticker))
    else:
        processes.append(process(path, procid))
    pticker = pticker + 1
    
def update():
    global processes
    statuses = []
    h = 0
    for i in range(len(processes)):
        satuses.append(processes[i].update())
    for i in range(len(statuses)):
        if statuses[i] == "terminated":
            del processes[i - h]
            h = h + 1
   
class process():
    
    def __init__(self, progpath, procid, parent = -1):
        self.parent = parent
        self.progpath = progpath
        self.progcode = loadStrings(progpath)
        self.procid = procid
        self.pcounter = 1
        self.stack = []
        self.ustack = []
        self.varlist = []
        self.state = False
        try:
            self.type = self.progcode[0].split(":", 1)[1]
        except:
            self.type = "NOHEADDER"
        self.funcs = []
        for h in range(len(self.progcode)):
            i = self.progcode[h]
            i = i.split(" ")
            if i[0] == "DEFINE":
                self.funcs.append([i[1], h])
            
            
    def getvar(self, inp):
        for i in self.varlist:
            if i[0] == inp:
                return(i[1])
        return(False)
    
    def setvar(self, inp, val):
        for i in range(len(self.varlist)):
            if self.varlist[i][0] == inp:
                self.varlist[i][1] = val
    
    def delvar(self, inp):
        for i in range(len(self.varlist)):
            if self.varlist[i][0] == inp:
                del self.varlist[i]
                return(True)
        return(False)
    
    def update(self):
        if self.type == "SCRIPT":
            currentline = self.progcode[self.pcounter].split(" ", 1)
            insruction = currentline[0]
            oprands = currentline[1].split(" ", 2)
            
            
            
        elif self.type == "DEAD":
            return("terminated")