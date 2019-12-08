from abc import ABC
from typing import List

import intcode.parameters


class AbstractMachine(ABC):

    def __init__(self, codes: List[int], inputs):
        self.codes = codes
        self.inputs = inputs if inputs is list else list(inputs)
        self.hasError = False
        self.output = None

    def popInput(self):
        return self.inputs.pop(0)


class Instruction(ABC):
    """Base class for instruction that provides access to parameters"""

    def __init__(self, parameterModes: str, index: int, machine: AbstractMachine):
        self.index = index
        self.machine = machine
        parameterCount = self.getParameterCount()
        parameterModes = parameterModes.zfill(parameterCount)
        self._parameters = [intcode.parameters.create(index + i, parameterModes[-i], machine.codes)
                            for i in range(1, parameterCount + 1)]

    def getParameterCount(self):
        raise NotImplementedError('must implement getParameterCount()')

    def execute(self):
        raise NotImplementedError('must implement execute()')


class AddInstruction(Instruction):
    """Adds parameters one and two and saves result in parameter three"""

    def getParameterCount(self):
        return 3

    def execute(self):
        value = self._parameters[0].get() + self._parameters[1].get()
        self._parameters[2].set(value)
        return True


class MultiplyInstruction(Instruction):
    """Multiplies parameters one and two and saves result in parameter three"""

    def getParameterCount(self):
        return 3

    def execute(self):
        value = self._parameters[0].get() * self._parameters[1].get()
        self._parameters[2].set(value)
        return True


class InputInstruction(Instruction):
    """takes a single integer as input and saves it to the position given by its only parameter"""

    def getParameterCount(self):
        return 1

    def execute(self):
        value = self.machine.popInput()
        self._parameters[0].set(value)
        return True


class OutputInstruction(Instruction):
    """outputs the value of its only parameter if the computer is not in an error state"""

    def getParameterCount(self):
        return 1

    def execute(self):
        value = self._parameters[0].get()
        self.machine.output = value
        if value != 0:
            if not self.machine.hasError:
                # the first non-zero value is the diagnostic code
                self.machine.hasError = True
            else:
                # another non-zero value indicates an error
                raise RuntimeError('An error occurred before instruction {0}. IO = {1}'.format(self.index, value))
        return True


class BreakInstruction(Instruction):
    """
    Simply stops further execution when executed. We could probably special case this instead
    of creating a new instruction instance.
    """

    def getParameterCount(self):
        return 0

    def execute(self):
        return False


_instructionClassesByCode = {1: AddInstruction,
                             2: MultiplyInstruction,
                             3: InputInstruction,
                             4: OutputInstruction,
                             99: BreakInstruction}


def create(instructionCode: int, parameterModes: str, index: int, machine: AbstractMachine):
    instructionClass = _instructionClassesByCode[instructionCode]
    result = instructionClass(parameterModes, index, machine)
    return result
