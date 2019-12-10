from abc import ABC
from typing import List


class MachineBase(ABC):

    def __init__(self, program: List[int], inputs: List[int]):
        self.program = program
        self.inputs = inputs[:]
        self.hasError = False
        self.output = []
        self.relativeBase = 0

    def popInput(self):
        return self.inputs.pop(0)
