from reserveStation import ReserveStation
from multiplicationStation import MultiplicationStation
from divisionStation import DivisionStation
from additionStation import AdditionStation
from loadStation import LoadStation
from storeStation import StoreStation
from registers import Registers
from register import Register
from threading import Thread
from time import sleep
import string
import os
from tabulate import tabulate

multiplicationStation = MultiplicationStation(3)
divisionStation = DivisionStation(2)
additionStation = AdditionStation(4)
loadStation = LoadStation(6)
storeStation = StoreStation(6)
registers = Registers(10)
registersInt = Registers(10)
instructions = ['LD F4,0(R0)','LD F6,2(R0)','LD F7,4(R0)','LD F3,8(R0)', 'MULTD F2,F4,F6', 'MULTD F5,F7,F3','MULTD F8,F2,F5', 'MULTD F3,F5,F7', 'DIVD F9,F2,F6', 'ADDD F6,F8,F2', 'SD F2,0(F1)']
pc = 0
instructionInBus = False

def main():
    global pc
    for i in range(100):
        raw_input("presione enter para generar un clock")
        os.system('clear')
        cdbThread = Thread(target = CDBThread)
        instructioneFetcherThread = Thread(target = instructionFetcher)
        instructioneFetcherThread.start()
        cdbThread.start()
        pc += 1

        print "\nMultiplicacion - Estacion de Reserva"
        multiplicationStation.printRows()
        print "Division - Estacion de Reserva"
        divisionStation.printRows()
        print "Suma - Estacion de Reserva"
        additionStation.printRows()
        print "Registros"
        registers.printRegisters()

def CDBThread ():
    print "clock", pc
    global instructionInBus
    if pc < 3:
        return
    instructionInBus = False
    #   multiplication part
    clockToReserveStation(multiplicationStation)

    #   division part
    clockToReserveStation(divisionStation)
    
    #   addittion part
    clockToReserveStation(additionStation)
    
    #   load part
    clockToReserveStation(loadStation)
    
    #   store part
    storeStation.updateClock()
    if(storeStation.isOperating()):
        if(storeStation.isReady() and not instructionInBus):
            result = storeStation.flushToBus()
            instructionInBus = True
            storeStation.startOperation()
    else:
        storeStation.startOperation()

def instructionFetcher ():
    global pc
    if (pc >= len(instructions)):
        instruction = "NOP"
    else:
        instruction = instructions[pc]
    print "INSTRUCCION ENTRANTE: ", instruction
    regs = instruction.replace(",", " ").split(" ")
    # multiplication fetch
    if (regs[0] == "MULTD"):
        clockToFetchToReserveStation(multiplicationStation, regs)
            
    # division fetch
    if (regs[0] == "DIVD"):
        clockToFetchToReserveStation(divisionStation, regs)
            
    # addition fetch
    if (regs[0] == "ADDD"):
        clockToFetchToReserveStation(additionStation, regs)
            
    # load fetch
    if (regs[0] == "LD"):
        result = loadStation.getFreePosition()
        if(result[0] >= 0):
            registers.updateRegisterTag(result[1],obtainRegNumber(regs[1]))
            parsed = parseLoadRegister(regs[2])
            dirReg = registersInt.getRegister(parsed[0])
            loadStation.loadInstruction(dirReg.valueI + parsed[1], result[0])
        else:
            pc -= 1

    # store fetch
    if (regs[0] == "SD"):
        result = storeStation.getFreePosition()
        if(result[0] >= 0):
            storeValue = registers.getRegister(obtainRegNumber(regs[1]))
            parsed = parseLoadRegister(regs[2])
            dirReg = registersInt.getRegister(parsed[0])
            storeStation.loadInstruction(dirReg.valueI + parsed[1], storeValue.Qi, storeValue.valueI, result[0])
        else:
            pc -= 1

def updateRowsTags(tag, value):
    """
    Funcion encargada de actualizar los tags en todas las estaciones y los registros.
    """
    multiplicationStation.updateValueByTag(tag, value)
    divisionStation.updateValueByTag(tag, value)
    additionStation.updateValueByTag(tag, value)
    loadStation.updateValueByTag(tag, value)

def obtainRegNumber(regString):
    all=string.maketrans('','')
    nodigs=all.translate(all, string.digits)
    return int(regString.translate(all, nodigs))

def parseLoadRegister(register):
    reg = register.replace(')','(').split('(')
    all=string.maketrans('','')
    nodigs=all.translate(all, string.digits)
    return int(reg[1].translate(all, nodigs)), int(reg[0].translate(all, nodigs))

def clockToReserveStation(station):
    """
    Funcion encargada de darle clock a las estaciones de reserva, y verificar si se produjo el resultado
    y actualizar los registros y tags correspondientes.
    """
    global instructionInBus
    station.updateClock()
    if(station.isOperating()):
        if(station.isReady() and not instructionInBus):
            result = station.flushToBus()
            reg = Register("", result[1])
            registers.updateRegisterByTag(result[0], reg)
            updateRowsTags(result[0], result[1])
            station.startOperation()
            return True
    else:
        station.startOperation()
    return False

def clockToFetchToReserveStation(station, regs):
    """
    Funcion que intenta cargar el valor a una estacion de reserva, actualizando tags de registros y en la misma estacion.
    """
    global pc
    result = station.getFreePosition()
    if(result[0] >= 0):
        registers.updateRegisterTag(result[1],obtainRegNumber(regs[1]))
        operand1 = registers.getRegister(obtainRegNumber(regs[2]))
        operand2 = registers.getRegister(obtainRegNumber(regs[3]))
        station.loadInstruction(operand1.Qi, operand1.valueI, operand2.Qi, operand2.valueI, result[0])
        return True
    else:
        pc -= 1
        return False

if __name__ == '__main__':
    main()




