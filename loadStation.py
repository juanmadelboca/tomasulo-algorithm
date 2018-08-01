"""
Clase Load, encargada traer de la memoria datos y ponerlos en registros
"""
from tabulate import tabulate
from random import randint
import string


class LoadStation(object):
    def __init__(self, size):
        self.rowNumberFu = -1
        self.fuState = 0
        self.taskList = []
        self.size = size
        for i in range(size):
            row = Row("load" + str(i))
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
        if(self.fuState >= 1):
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
        count = 0
        while count <= row.dir:
            ret = file_object.readline()
            count = count + 1
        file_object.close()
        return row.tag, int(ret)

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
                    
    def loadInstruction(self, dir, position):
        """
        Carga una instruccion con todo lo que necesita en la estacion de reserva (valores y tags).
        """
        row = self.taskList[position]
        row.dir = dir

    def updateValueByTag(self, tag, value):
        """
        Recorre la estacion de reserva y actualiza los valores que correspondan con la etiqueta de la
        operacion que a sido terminada.
        """
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
