from tabulate import tabulate
from random import randint


class LoadStation(object):
    
    def __init__(self, size, tag, opClocks):
        self.rowNumberFu = -1
        self.opClocks = opClocks
        self.fuState = 0
        self.taskList = []
        self.size = size
        for i in range(size):
            row = Row(tag + str(i))
            self.taskList.append(row)

    def getFreePosition(self):
        for i in range(self.size):
            if(not self.taskList[i].isBusy()):
                self.taskList[i].busy = True
                return i, self.taskList[i].tag
        return -1,""

    def loadRow(self, row, position):
        self.taskList[position] = row

    def isOperating(self):
        if(self.rowNumberFu >= 0):
            return True

    def updateClock(self):
        if(self.rowNumberFu >= 0):
            self.fuState += 1

    def isReady(self):
        if(self.fuState >= self.opClocks):
            return True
        else:
            return False

    def flushToBus(self):
        row = self.taskList[self.rowNumberFu]
        self.taskList[self.rowNumberFu].busy = False
        self.rowNumberFu = -1
        self.fuState = 0
        return row.tag, randint(0, 9)

    def startOperation(self):
        if(self.rowNumberFu < 0):
            for i in range(self.size):
                if(self.taskList[i].isBusy()):
                    self.rowNumberFu = i
                    return
                    
    def loadInstruction(self, dir, position):
        row = self.taskList[position]
        row.dir = dir

    def updateValueByTag(self, tag, value):
        for i in range(self.size):
            if(self.taskList[i].dir == tag):
                self.taskList[i].dir = value

class Row(object):

    def __init__(self, tag):
        self.tag = tag
        self.dir = 0
        self.value = 0
        self.busy = False
    
    def isBusy(self):
        return self.busy