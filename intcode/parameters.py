from abc import ABC
from typing import List


class Parameter(ABC):

    def __init__(self, index: int, codes: List[int]):
        self._codes = codes
        self._index = index

    def get(self):
        raise NotImplementedError()

    def set(self, value: int):
        raise NotImplementedError()


class PositionalParameter(Parameter):

    def get(self):
        position = self._codes[self._index]
        result = self._codes[position]
        return result

    def set(self, value: int):
        position = self._codes[self._index]
        self._codes[position] = value


class ImmediateParameter(Parameter):

    def get(self):
        result = self._codes[self._index]
        return result

    def set(self, value: int):
        self._codes[self._index] = value


_parameterClassesByMode = {0: PositionalParameter,
                           1: ImmediateParameter}


def create(index: int, modeString: str, codes: List[int]) -> Parameter:
    mode = int(modeString)
    parameterClass = _parameterClassesByMode[mode]
    parameter = parameterClass(index, codes)
    return parameter
