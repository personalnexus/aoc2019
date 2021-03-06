from abc import ABC
from collections import defaultdict
from typing import List, Optional


class MachineBase(ABC):

    def __init__(self, program: List[int]):
        self.program = defaultdict(int, [(i, program[i]) for i in range(len(program))])
        self._inputs: List[int] = []
        self._output: Optional[int] = None
        self.relativeBase = 0
        self.halted = False
        self.nextInstructionIndex = 0
        self.nextInstructionCode = 0
        self.nextParameterModes = ''
        self.inputsProvider = None

    def popInput(self):
        return self.inputsProvider() if self.inputsProvider is not None else self._inputs.pop(0)

    def setOutput(self, output: int):
        self._output = output
