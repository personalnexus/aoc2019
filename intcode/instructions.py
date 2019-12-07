from typing import Callable
import intcode.parameters


class Instruction(object):

    def __init__(self, parameterModes: str, parameterCount: int, offset: int, computer):
        parameterModes = parameterModes.zfill(parameterCount)
        self.parameters = [intcode.parameters.create(offset + i, parameterModes[-i - 1]) for i in range(parameterCount)]
        self._computer = computer

    @property
    def parameterCount(self):
        return len(self.parameters)

    def execute(self):
        raise NotImplementedError('must implement execute()')


class TwoInOneOutParameterInstruction(Instruction):

    def __init__(self, parameterModes: str, offset: int, computer, func: Callable[[int, int], int]):
        super(TwoInOneOutParameterInstruction, self).__init__(parameterModes, 3, offset, computer)
        self._func = func

    def execute(self):
        value = self._func(self.parameters[0].getValue(self._computer.codes),
                           self.parameters[1].getValue(self._computer.codes))
        self.parameters[2].setValue(self._computer.codes, value)
        return True


class AddInstruction(TwoInOneOutParameterInstruction):

    def __init__(self, parameterModes: str, offset: int, computer):
        super(AddInstruction, self).__init__(parameterModes, offset, computer, lambda a, b: a + b)


class MultiplyInstruction(TwoInOneOutParameterInstruction):

    def __init__(self, parameterModes: str, offset: int, computer):
        super(MultiplyInstruction, self).__init__(parameterModes, offset, computer, lambda a, b: a * b)


class InputInstruction(Instruction):
    """takes a single integer as input and saves it to the position given by its only parameter"""

    def __init__(self, parameterModes: str, offset: int, computer):
        super(InputInstruction, self).__init__(parameterModes, 1, offset, computer)

    def execute(self):
        self.parameters[0].setValue(self._computer.codes, self._computer.IO)
        return True


class OutputInstruction(Instruction):
    """outputs the value of its only parameter"""

    def __init__(self, parameterModes: str, offset: int, computer):
        super(OutputInstruction, self).__init__(parameterModes, 1, offset, computer)

    def execute(self):
        self._computer.io = self.parameters[0].getValue(self._computer.codes)
        return True


class BreakInstruction(Instruction):
    """
    Simply stops further execution when executed. We could probably special case this instead
    of creating a new instruction instance.
    """

    def __init__(self, parameterModes: str, offset: int, computer):
        super(BreakInstruction, self).__init__(parameterModes, 0, offset, computer)

    def execute(self):
        return False


_instructionClassesByCode = {1: AddInstruction,
                             2: MultiplyInstruction,
                             3: InputInstruction,
                             4: OutputInstruction,
                             99: BreakInstruction}


def create(instructionCode: int, parameterModes: str, parameterOffset: int, computer):
    instructionClass = _instructionClassesByCode[instructionCode]
    result = instructionClass(parameterModes, parameterOffset, computer)
    return result
