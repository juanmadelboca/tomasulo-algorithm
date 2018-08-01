"""
Clase Estacion de reserva a partir de esta clase se crean multiplicacion, division y suma
"""
from tabulate import tabulate


class ReserveStation(object):
    
    def __init__(self, size):
        self.rowNumberFu = -1
        self.fuState = 0
        self.taskList = []
        self.size = size

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

    def startOperation(self):  
        """
        Chequea que instruccion dentro de la estacion de reserva tiene todo los valores necesarios
        para ejecutarse y coloca la operacion en la Unidad funcional
        """
        if(self.rowNumberFu < 0):
            for i in range(self.size):
                if(self.taskList[i].isBusy() and self.taskList[i].Qj == "" and self.taskList[i].Qk == ""):
                    self.rowNumberFu = i
                    return
                    
    def updateValueByTag(self, tag, value): 
        """
        Recorre la estacion de reserva y actualiza los valores que correspondan con la etiqueta de la
        operacion que a sido terminada.
        """
        for i in range(self.size):
            if(self.taskList[i].Qj == tag):
                self.taskList[i].Qj = ""
                self.taskList[i].valueJ = value
            if(self.taskList[i].Qk == tag):
                self.taskList[i].Qk = ""
                self.taskList[i].valueK = value
                    
    def loadInstruction(self, Qj, valueJ, Qk, valueK, position): 
        """
        Carga una instruccion con todo lo que necesita en la estacion de reserva (valores y tags).
        """
        row = self.taskList[position]
        row.Qj = Qj
        row.valueJ = valueJ
        row.Qk = Qk
        row.valueK = valueK

    def printRows(self):
        arr = self.iterateRows()
        print tabulate(arr, headers = ['tag', 'Qj', 'valueJ', 'Qk', 'valueK', 'busy', 'R'], tablefmt='fancy_grid')

    def iterateRows(self): 
        """
        Transforma la estacion de reserva en un arreglo bidimensional, para poder utilizar la libreria tabulate.
        """
        arr = []
        for i in range(self.size):
            temp = []
            row = self.taskList[i]
            temp.append(row.tag)
            temp.append(row.Qj)
            temp.append(row.valueJ)
            temp.append(row.Qk)
            temp.append(row.valueK)
            temp.append(row.busy)
            if(self.rowNumberFu == i):
                temp.append(u'\u2713')
            else:
                temp.append("")

            arr.append(temp)
        return arr