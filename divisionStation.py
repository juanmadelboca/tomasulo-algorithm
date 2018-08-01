from reserveStation import ReserveStation
from row import Row

class DivisionStation(ReserveStation):

    def __init__(self, size):
        super(DivisionStation, self).__init__(size)
        for i in range(size):
            row = Row("div" + str(i))
            self.taskList.append(row)

    def flushToBus(self):
        """
        Funcion que devuelve el valor de la operacion realizada por la UF.
        """
        row = self.taskList[self.rowNumberFu]
        self.taskList[self.rowNumberFu].busy = False
        self.rowNumberFu = -1
        self.fuState = 0
        return row.tag, row.valueJ / row.valueK

    def isReady(self):
        if(self.fuState >= 12):
            return True
        else:
            return False