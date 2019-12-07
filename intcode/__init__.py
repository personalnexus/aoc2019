import intcode.instructions


class IntCodeComputer(object):

    def __init__(self, codes, io):
        self.codes = codes
        self.io = io
        self.hasError = False

    def execute(self):
        i = 0
        instruction = None
        while i < len(self.codes):
            # Code 0: header
            instructionHeader = str(self.codes[i]).zfill(2)
            instructionCode = int(instructionHeader[-2:])
            parameterModes = instructionHeader[0:-2]

            # Codes 1-n: instruction parameters
            instruction = instructions.create(instructionCode, parameterModes, i, self)
            i += 1 + instruction.parameterCount

            if not instruction.execute():
                break
