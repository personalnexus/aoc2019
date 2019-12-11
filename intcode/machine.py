from abc import ABC
from typing import List


class MachineBase(ABC):

    def __init__(self, program: List[int]):
        self.program = program
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.relativeBase = 0

    def popInput(self):
        return self.inputs.pop(0)
