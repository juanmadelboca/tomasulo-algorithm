class Row(object):
    
    def __init__(self, tag):
        self.tag = tag
        self.opCode = 0
        self.Qj = ""
        self.valueJ = 0
        self.Qk = ""
        self.valueK = 0
        self.busy = False
    
    def isBusy(self):
        return self.busy