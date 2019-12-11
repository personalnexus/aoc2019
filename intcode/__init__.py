from typing import List
from intcode.instructions import MachineBase


class IntCodeComputer(MachineBase):

    def __init__(self, program: List[int]):
        super(IntCodeComputer, self).__init__(program)
        self.debug = False

    def execute(self, inputs: List[int]):
        self.inputs = inputs[:]
        self.outputs = []
        nextInstruction = 0
        initialProgramLength = len(self.program)
        while (nextInstruction is not None) and (nextInstruction < len(self.program)):
            # Code 0: header
            instructionHeader = str(self.program[nextInstruction]).zfill(2)
            instructionCode = int(instructionHeader[-2:])
            parameterModes = instructionHeader[0:-2]

            # Codes 1-n: instruction parameters
            instruction = instructions.create(instructionCode, parameterModes, nextInstruction, self)

            if self.debug:
                instructionName = instruction.__class__.__name__.replace('Instruction', '')
                parameters = ','.join(instruction.getParameterValues())
                print(f'{nextInstruction} | {instructionName} | {parameters}')

            nextInstruction = instruction.execute()

        # trim the extra memory created during execution
        self.program = self.program[:initialProgramLength]
