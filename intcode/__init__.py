from intcode.instructions import AbstractMachine


class IntCodeComputer(AbstractMachine):

    def execute(self):
        nextInstruction = 0
        while nextInstruction < len(self.codes):
            # Code 0: header
            instructionHeader = str(self.codes[nextInstruction]).zfill(2)
            instructionCode = int(instructionHeader[-2:])
            parameterModes = instructionHeader[0:-2]

            # Codes 1-n: instruction parameters
            instruction = instructions.create(instructionCode, parameterModes, nextInstruction, self)

            nextInstruction = instruction.execute()
            if nextInstruction is None:
                break
