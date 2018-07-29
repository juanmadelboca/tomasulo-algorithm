from row import Row
from tabulate import tabulate


class ReserveStation(object):
    
    def __init__(self, size, tag, opClocks, opCode):
        self.rowNumberFu = -1
        self.opClocks = opClocks
        self.opCode = opCode
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
        if(self.opCode == 'ADDD'):
            row = self.taskList[self.rowNumberFu]
            self.taskList[self.rowNumberFu].busy = False
            self.rowNumberFu = -1
            self.fuState = 0
            return row.tag, row.valueJ + row.valueK

        if(self.opCode == 'DIVD'):
            row = self.taskList[self.rowNumberFu]
            self.taskList[self.rowNumberFu].busy = False
            self.rowNumberFu = -1
            self.fuState = 0
            return row.tag, row.valueJ / row.valueK

        if(self.opCode == 'MULT'):
            row = self.taskList[self.rowNumberFu]
            self.taskList[self.rowNumberFu].busy = False
            self.rowNumberFu = -1
            self.fuState = 0
            return row.tag, row.valueJ * row.valueK

    def startOperation(self):
        if(self.rowNumberFu < 0):
            for i in range(self.size):
                if(self.taskList[i].isBusy() and self.taskList[i].Qj == "" and self.taskList[i].Qk == ""):
                    self.rowNumberFu = i
                    return
                    
    def updateValueByTag(self, tag, value):
        for i in range(self.size):
            if(self.taskList[i].Qj == tag):
                self.taskList[i].Qj = ""
                self.taskList[i].valueJ = value
            if(self.taskList[i].Qk == tag):
                self.taskList[i].Qk = ""
                self.taskList[i].valueK = value
                    
    def loadInstruction(self, Qj, valueJ, Qk, valueK, position):
        row = self.taskList[position]
        row.Qj = Qj
        row.valueJ = valueJ
        row.Qk = Qk
        row.valueK = valueK

    def printRows(self):
        arr = self.iterateRows()
        print tabulate(arr, headers = ['tag', 'opCode', 'Qj', 'valueJ', 'Qk', 'valueK', 'busy'])

    def iterateRows(self):
        arr = []
        for i in range(self.size):
            temp = []
            row = self.taskList[i]
            temp.append(row.tag)
            temp.append(row.opCode)
            temp.append(row.Qj)
            temp.append(row.valueJ)
            temp.append(row.Qk)
            temp.append(row.valueK)
            temp.append(row.busy)
            arr.append(temp)
        return arr