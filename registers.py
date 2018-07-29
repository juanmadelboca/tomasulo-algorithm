from register import Register
from tabulate import tabulate


class Registers(object):
    
    def __init__(self, size):
        self.registerList = []
        self.size = size
        register = Register("", 2)
        for i in range(size):
            self.registerList.append(register)
    
    def getRegister(self, number):
        return self.registerList[number]

    def editRegister(self, register, number):
        self.registerList[number] = register

    def updateRegisterTag(self,tag, number):
        reg = Register(tag, self.registerList[number].valueI)
        self.editRegister(reg, number)

    def updateRegisterByTag(self, tag, register):
        for i in range(self.size):
            if(self.registerList[i].Qi == tag):
                self.editRegister(register, i)


    def printRegisters(self):
        regs = self.iterateRegisters()
        print tabulate(regs, headers = ['Qi', 'valueI'])

    def iterateRegisters(self):
        arr = []
        for i in range(self.size):
            temp = []
            reg = self.registerList[i]
            temp.append(reg.Qi)
            temp.append(reg.valueI)
            arr.append(temp)
        return arr