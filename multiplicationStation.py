from reserveStation import ReserveStation
from row import Row

class MultiplicationStation(ReserveStation):

    def __init__(self, size):
        super(MultiplicationStation, self).__init__(size)
        for i in range(size):
            row = Row("mult" + str(i))
            self.taskList.append(row)

    def flushToBus(self):
        """
        Funcion que devuelve el valor de la operacion realizada por la UF.
        """
        row = self.taskList[self.rowNumberFu]
        self.taskList[self.rowNumberFu].busy = False
        self.rowNumberFu = -1
        self.fuState = 0
        return row.tag, row.valueJ * row.valueK

    def isReady(self):
        if(self.fuState >= 8):
            return True
        else:
            return False