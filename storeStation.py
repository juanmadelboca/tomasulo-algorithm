"""
Clase Store, encargada de guardar en memoria datos que estan en registros
"""
from tabulate import tabulate
from random import randint


class StoreStation(object):
    
    def __init__(self, size):
        self.rowNumberFu = -1
        self.fuState = 0
        self.taskList = []
        self.size = size
        for i in range(size):
            row = Row("st" + str(i))
            self.taskList.append(row)

    def getFreePosition(self):
        """
        Si hay lugar en la estacion de reserva devuelve la posicion, de lo contrario devulve -1
        """
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
        if(self.fuState >= 4):
            return True
        else:
            return False

    def flushToBus(self):
        """
        Funcion que devuelve el valor de la operacion realizada por la UF.
        """
        row = self.taskList[self.rowNumberFu]
        self.taskList[self.rowNumberFu].busy = False
        self.rowNumberFu = -1
        self.fuState = 0
        file_object  = open("memory.txt", "r")
        data = file_object.readlines()
        data[row.dir] = str(row.valueI) + '\n'
        file_object.close()
        file_object  = open("memory.txt", "w")
        file_object.writelines( data )
        file_object.close()
        return

    def startOperation(self):
        """
        Chequea que instruccion dentro de la estacion de reserva tiene todo los valores necesarios
        para ejecutarse y coloca la operacion en la Unidad funcional
        """
        if(self.rowNumberFu < 0):
            for i in range(self.size):
                if(self.taskList[i].isBusy()):
                    self.rowNumberFu = i
                    return
                    
    def loadInstruction(self, dir, Qi, valueI, position):
        """
        Carga una instruccion con todo lo que necesita en la estacion de reserva (valores y tags).
        """
        row = self.taskList[position]
        row.dir = dir
        row.Qi = Qi
        row.valueI = valueI

    def updateValueByTag(self, tag, value):
        """
        Recorre la estacion de reserva y actualiza los valores que correspondan con la etiqueta de la
        operacion que a sido terminada.
        """
        for i in range(self.size):
            if(self.taskList[i].Qi == tag):
                self.taskList[i].Qi = ""
                self.taskList[i].valueI = value

class Row(object):

    def __init__(self, tag):
        self.tag = tag
        self.dir = 0
        self.valueI = 0
        self.Qi = ""
        self.busy = False
    
    def isBusy(self):
        return self.busy