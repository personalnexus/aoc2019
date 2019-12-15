from abc import ABC
from intcode.machine import MachineBase
import intcode.parameters


class Instruction(ABC):
    """Base class for instruction that provides access to parameters"""

    def __init__(self, parameterModes: str, index: int, machine: MachineBase):
        self.index = index
        self.machine = machine
        parameterCount = self.getParameterCount()
        parameterModes = parameterModes.zfill(parameterCount)
        self._parameters = [intcode.parameters.create(index + i, int(parameterModes[-i]), machine)
                            for i in range(1, parameterCount + 1)]

    def getParameterCount(self):
        raise NotImplementedError('must implement getParameterCount()')

    def execute(self):
        return self.index + 1 + self.getParameterCount()

    def getParameterValues(self):
        return (str(p.get()) for p in self._parameters)


class TwoInOneOutParameterInstruction(Instruction):
    """Base class for instructions setting a third parameter based on some calculation on two input parameters"""

    def getParameterCount(self):
        return 3

    def execute(self):
        parameter0 = self._parameters[0].get()
        parameter1 = self._parameters[1].get()
        value = self.calculateParameterTwo(parameter0, parameter1)
        self._parameters[2].set(value)
        return super().execute()

    def calculateParameterTwo(self, parameter0: int, parameter1: int) -> int:
        raise NotImplementedError('must implement calculateParameterTwo()')


class AddInstruction(TwoInOneOutParameterInstruction):
    """Adds parameters zero and one and saves result in parameter two"""

    def calculateParameterTwo(self, parameter0: int, parameter1: int) -> int:
        return parameter0 + parameter1


class MultiplyInstruction(TwoInOneOutParameterInstruction):
    """Multiplies parameters zero and one and saves result in parameter two"""

    def calculateParameterTwo(self, parameter0: int, parameter1: int) -> int:
        return parameter0 * parameter1


class InputInstruction(Instruction):
    """takes a single integer as input and saves it to the position given by its only parameter"""

    def getParameterCount(self):
        return 1

    def execute(self):
        value = self.machine.popInput()
        self._parameters[0].set(value)
        return super().execute()


class OutputInstruction(Instruction):
    """outputs the value of its only parameter and stops execution"""

    def getParameterCount(self):
        return 1

    def execute(self):
        value = self._parameters[0].get()
        self.machine.setOutput(value)
        return super().execute()


class JumpIfTrueInstruction(Instruction):
    """Jump to the instruction given by the value of parameter 1 if parameter 0 is true"""

    def getParameterCount(self):
        return 2

    def execute(self):
        result = self._parameters[1].get() if self._parameters[0].get() != 0 else super().execute()
        return result


class JumpIfFalseInstruction(Instruction):
    """Jump to the instruction given by the value of parameter 1 if parameter 0 is false"""

    def getParameterCount(self):
        return 2

    def execute(self):
        result = self._parameters[1].get() if self._parameters[0].get() == 0 else super().execute()
        return result


class LessThanInstruction(TwoInOneOutParameterInstruction):
    """Return 1 if parameter zero is less than parameter one otherwise return 0"""

    def calculateParameterTwo(self, parameter0: int, parameter1: int) -> int:
        return 1 if parameter0 < parameter1 else 0


class EqualsInstruction(TwoInOneOutParameterInstruction):
    """Return 1 if parameter zero is equal to parameter one otherwise return 0"""

    def calculateParameterTwo(self, parameter0: int, parameter1: int) -> int:
        return 1 if parameter0 == parameter1 else 0


class RelativeBaseAdjustmentInstruction(Instruction):
    """Return 1 if parameter zero is equal to parameter one otherwise return 0"""

    def getParameterCount(self):
        return 1

    def execute(self):
        self.machine.relativeBase += self._parameters[0].get()
        return super().execute()


_instructionClassesByCode = {1: AddInstruction,
                             2: MultiplyInstruction,
                             3: InputInstruction,
                             4: OutputInstruction,
                             5: JumpIfTrueInstruction,
                             6: JumpIfFalseInstruction,
                             7: LessThanInstruction,
                             8: EqualsInstruction,
                             9: RelativeBaseAdjustmentInstruction}


def create(machine: MachineBase) -> Instruction:
    instructionClass = _instructionClassesByCode[machine.nextInstructionCode]
    result = instructionClass(machine.nextParameterModes, machine.nextInstructionIndex, machine)
    return result
