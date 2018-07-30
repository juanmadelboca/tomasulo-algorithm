from reserveStation import ReserveStation
from loadStation import LoadStation
from storeStation import StoreStation
from registers import Registers
from register import Register
from threading import Thread
from time import sleep
import string
import os
from tabulate import tabulate

multiplicationStation = ReserveStation(3,"mult", 6, 'MULT')
divisionStation = ReserveStation(2,"div", 6, 'DIVD')
additionStation = ReserveStation(4,"add", 2, 'ADDD')
loadStation = LoadStation(6,"load", 4)
storeStation = StoreStation(6,"load", 4)
registers = Registers(10)
# instructions = ['LD F6, 0(R1)', 'LD F6, 0(R1)', 'MULT F0,F2,F4', 'SUBD F8,F6,F2', 'DIVD F10,F0,F6', 'ADDD F6,F8,F2']
instructions = ['LD F1,0(F1)', 'MULT F2,F4,F6', 'MULT F5,F7,F3','MULT F8,F2,F5', 'MULT F3,F5,F7', 'DIVD F9,F0,F6', 'ADDD F6,F8,F2', 'ST F2,0(F1)']
pc = 0
instructionInBus = False

def main():
    cdbThread = Thread(target = CDBThread)
    instructioneFetcherThread = Thread(target = instructionFetcher)
    global pc
    for i in range(100):
        raw_input("presione enter para generar un clock")
        os.system('clear')
        instructionFetcher ()
        CDBThread ()
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
    global instructionInBus
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
    else:
        storeStation.startOperation()

def instructionFetcher ():
    global pc
    if (pc >= len(instructions)):
        instruction = "NOP"
    else:
        instruction = instructions[pc]
    print "INSTRUCCION: ", instruction
    regs = instruction.replace(",", " ").split(" ")
    # multiplication fetch
    if (regs[0] == "MULT"):
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
            dirReg = registers.getRegister(parsed[0])
            loadStation.loadInstruction(parsed[0] + parsed[1], result[0])
        else:
            pc -= 1

    # store fetch
    if (regs[0] == "ST"):
        result = storeStation.getFreePosition()
        if(result[0] >= 0):
            storeValue = registers.getRegister(obtainRegNumber(regs[1]))
            parsed = parseLoadRegister(regs[2])
            dirReg = registers.getRegister(parsed[0])
            storeStation.loadInstruction(parsed[0] + parsed[1], storeValue.Qi, storeValue.valueI, result[0])
        else:
            pc -= 1
            
def updateRowsTags(tag, value):
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
    global instructionInBus
    station.updateClock()
    if(station.isOperating()):
        if(station.isReady() and not instructionInBus):
            result = station.flushToBus()
            reg = Register("", result[1])
            registers.updateRegisterByTag(result[0], reg)
            updateRowsTags(result[0], result[1])
            return True
    else:
        station.startOperation()
    return False
def clockToFetchToReserveStation(station, regs):
    global pc
    result = station.getFreePosition()
    if(result[0] >= 0):
        registers.updateRegisterTag(result[1],obtainRegNumber(regs[1]))
        operand1 = registers.getRegister(obtainRegNumber(regs[2]))
        operand2 = registers.getRegister(obtainRegNumber(regs[3]))
        station.loadInstruction(operand1.Qi, operand1.valueI, operand2.Qi, operand2.valueI, result[0])
    else:
        pc -= 1

if __name__ == '__main__':
    main()




