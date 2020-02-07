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
        statuses.append(processes[i].update())
    for i in range(len(statuses)):
        if statuses[i] == "terminated":
            del processes[i - h]
            h = h + 1
    return(len(processes))
   
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
    
    def checkmods(self, inp):
        global modules
        for i in modules:
            if i == inp:
                return(True)
        return(False)
    
    def update(self):
        if self.type == "SCRIPT":
            currentline = self.progcode[self.pcounter].split(" ", 1)
            insruction = currentline[0]
            try:
                oprands = currentline[1].split(" ", 2)
            except:
                oprands = ""
            
            if instruction == "REQUIRE":
                
                if oprands[0] == "<":
                    if not (self.checkmods(oprands[1])):
                        self.type = "DEAD"
                else:
                    if not (self.checkmods(self.getvar(oprands[0]))):
                        self.type = "DEAD"
                self.pcounter = self.pcounter + 1
                
            elif instruction == "DEFINE":
                
                i = 1
                while i > 0:
                    self.pcounter = self.pcounter + 1
                    if self.pcounter > len(self.progcode):
                        i = 0
                        self.type = "DEAD"
                    elif self.progcode[self.pcounter] == "END":
                        i = i - 1
                    else:
                        for i in ["IF", "WHILE"]:
                            if i == self.progcode[self.pcounter].split(" ", 1)[0]:
                                i = i + 1
                
            elif instruction == "CHECKMOD":
                pass
            elif instruction == "IF":
                pass
            elif instruction == "WHILE":
                pass
            elif instruction == "ELSE":
                pass
            elif instruction == "END":
                pass
            elif instruction == "OUTPUT":
                pass
            elif instruction == "CREATEVAR":
                pass
            elif instruction == "DELETEVAR":
                pass
            elif instruction == "SETVAR":
                pass
            elif instruction == "SPAWN":
                pass
            elif instruction == "JUMP":
                pass
            elif instruction == "JUMPS":
                pass
            elif instruction == "FNISH":
                pass
                
            else:
                self.pcounter = self.pcounter + 1
                if self.pcounter > len(self.progcode):
                    self.type = "DEAD"
            
            
            
        elif self.type == "DEAD":
            return("terminated")
