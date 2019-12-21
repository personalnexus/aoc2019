from typing import List
from intcode.instructions import MachineBase


def springScriptToIntCodeInputs(assemblyInstructions: List[str]):
    """
        Converts the ASCII assembly instructions of SpringScript to integer inputs for an IntCodeComputer. Automatically
        includes new-lines and the final WALK instruction.
    """
    if len(assemblyInstructions) > 15:
        raise ValueError("SpringScript is limited to 15 assembly instructions")
    inputs = [ord(c) for c in '\n'.join(assemblyInstructions)]
    inputs.extend(map(ord, "\nWALK\n"))
    return inputs


class IntCodeComputer(MachineBase):

    def __init__(self, program: List[int]):
        super(IntCodeComputer, self).__init__(program)
        self.debug = False
        # This will set the halted flag when the program consists of only a halt instruction
        self._getNextInstructionDetails()

    def executeAll(self, inputs: List[int]):
        allOutputs = []
        while not self.halted:
            output = self.execute(inputs)
            allOutputs.append(output)
            inputs = []
        return allOutputs

    def execute(self, inputs: List[int]):
        self._inputs.extend(inputs)
        while not self.halted:
            instruction = instructions.create(self)

            if self.debug:
                instructionName = instruction.__class__.__name__.replace('Instruction', '')
                parameters = ','.join(instruction.getParameterValues())
                print(f'{self.nextInstructionIndex}\t{instructionName}\t{parameters}')

            self.nextInstructionIndex = instruction.execute()
            self._getNextInstructionDetails()

            if self._output is not None:
                output = self._output
                self._output = None
                return output

    def _getNextInstructionDetails(self):
        instructionHeader = str(self.program[self.nextInstructionIndex]).zfill(2)
        self.nextInstructionCode = int(instructionHeader[-2:])
        self.nextParameterModes = instructionHeader[0:-2]
        if self.nextInstructionCode in (0, 99):
            self.halted = True
