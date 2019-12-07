from abc import ABC
from typing import List


class Parameter(ABC):

    def __init__(self, index: int):
        self._index = index

    def getValue(self, codes: List[int]):
        raise NotImplementedError()

    def setValue(self, codes: List[int], value: int):
        raise NotImplementedError()


class PositionalParameter(Parameter):

    def getValue(self, codes: List[int]):
        position = codes[self._index]
        result = codes[position]
        return result

    def setValue(self, codes: List[int], value: int):
        position = codes[self._index]
        codes[position] = value


class ImmediateParameter(Parameter):

    def getValue(self, codes: List[int]):
        result = codes[self._index]
        return result

    def setValue(self, codes: List[int], value: int):
        codes[self._index] = value


_parameterClassesByMode = {0: PositionalParameter,
                           1: ImmediateParameter}


def create(index: int, modeString: str) -> Parameter:
    mode = int(modeString)
    parameterClass = _parameterClassesByMode[mode]
    parameter = parameterClass(index)
    return parameter
