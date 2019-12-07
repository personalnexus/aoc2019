from typing import Callable
import intcode.parameters


class Instruction(object):

    def __init__(self, parameterModes: str, parameterCount: int, offset: int):
        parameterModes = parameterModes.zfill(parameterCount)
        self.parameters = [intcode.parameters.create(offset + i, parameterModes[-i - 1]) for i in range(parameterCount)]
        self.computer = None
        self.index: int = -1

    @property
    def parameterCount(self):
        return len(self.parameters)

    def execute(self):
        raise NotImplementedError('must implement execute()')


class TwoInOneOutParameterInstruction(Instruction):

    def __init__(self, parameterModes: str, offset: int, func: Callable[[int, int], int]):
        super(TwoInOneOutParameterInstruction, self).__init__(parameterModes, 3, offset)
        self._func = func

    def execute(self):
        value = self._func(self.parameters[0].getValue(self.computer.codes),
                           self.parameters[1].getValue(self.computer.codes))
        self.parameters[2].setValue(self.computer.codes, value)
        return True


class AddInstruction(TwoInOneOutParameterInstruction):

    def __init__(self, parameterModes: str, offset: int):
        super(AddInstruction, self).__init__(parameterModes, offset, lambda a, b: a + b)


class MultiplyInstruction(TwoInOneOutParameterInstruction):

    def __init__(self, parameterModes: str, offset: int):
        super(MultiplyInstruction, self).__init__(parameterModes, offset, lambda a, b: a * b)


class InputInstruction(Instruction):
    """takes a single integer as input and saves it to the position given by its only parameter"""

    def __init__(self, parameterModes: str, offset: int):
        super(InputInstruction, self).__init__(parameterModes, 1, offset)

    def execute(self):
        self.parameters[0].setValue(self.computer.codes, self.computer.io)
        return True


class OutputInstruction(Instruction):
    """outputs the value of its only parameter"""

    def __init__(self, parameterModes: str, offset: int):
        super(OutputInstruction, self).__init__(parameterModes, 1, offset)

    def execute(self):
        value = self.parameters[0].getValue(self.computer.codes)
        self.computer.io = value
        if value != 0:
            if not self.computer.hasError:
                # the first non-zero value is the diagnostic code
                self.computer.hasError = True
            else:
                # another non-zero value indicates an error
                raise RuntimeError('An error occurred before instruction {0}. IO = {1}'.format(self.index, value))
        return True


class BreakInstruction(Instruction):
    """
    Simply stops further execution when executed. We could probably special case this instead
    of creating a new instruction instance.
    """

    def __init__(self, parameterModes: str, offset: int):
        super(BreakInstruction, self).__init__(parameterModes, 0, offset)

    def execute(self):
        return False


_instructionClassesByCode = {1: AddInstruction,
                             2: MultiplyInstruction,
                             3: InputInstruction,
                             4: OutputInstruction,
                             99: BreakInstruction}


def create(instructionCode: int, parameterModes: str, index: int, computer):
    instructionClass = _instructionClassesByCode[instructionCode]
    result = instructionClass(parameterModes, index + 1)
    result.index = index - 1
    result.computer = computer
    return result
