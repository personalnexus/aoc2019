from typing import List
from intcode.instructions import MachineBase


class IntCodeComputer(MachineBase):

    def __init__(self, program: List[int]):
        super(IntCodeComputer, self).__init__(program)
        self.debug = False
        self._nextInstruction = 0

    def execute(self, inputs: List[int]):
        self._inputs.extend(inputs)
        while not self.halted:
            # Code 0: header
            instructionHeader = str(self.program[self._nextInstruction]).zfill(2)
            instructionCode = int(instructionHeader[-2:])
            parameterModes = instructionHeader[0:-2]

            # Codes 1-n: instruction parameters
            instruction = instructions.create(instructionCode, parameterModes, self._nextInstruction, self)

            if self.debug:
                instructionName = instruction.__class__.__name__.replace('Instruction', '')
                parameters = ','.join(instruction.getParameterValues())
                print(f'{self._nextInstruction} | {instructionName} | {parameters}')

            self._nextInstruction = instruction.execute()
            if self._output is not None:
                return self._output

    def executeAll(self, inputs: List[int]):
        allOutputs = []
        while not self.halted:
            output = self.execute(inputs)
            if self.halted:
                break
            allOutputs.append(output)
            inputs = []
        return allOutputs
