from intcode.machine import MachineBase
from abc import ABC


class Parameter(ABC):

    def __init__(self, index: int, machine: MachineBase):
        self._machine = machine
        self._index = index

    def get(self):
        raise NotImplementedError()

    def set(self, value: int):
        raise NotImplementedError()

    def _get(self, index: int):
        self._resize(index)
        return self._machine.program[index]

    def _set(self, index: int, value: int):
        self._resize(index)
        self._machine.program[index] = value

    def _resize(self, index):
        while index >= len(self._machine.program):
            self._machine.program.append(0)


class PositionalParameter(Parameter):

    def get(self):
        position = self._get(self._getIndex())
        result = self._get(position)
        return result

    def set(self, value: int):
        position = self._get(self._getIndex())
        self._set(position, value)

    def _getIndex(self):
        raise NotImplementedError('must implement _getIndex()')


class AbsolutePositionalParameter(PositionalParameter):

    def _getIndex(self):
        return self._index


class RelativePositionalParameter(PositionalParameter):

    def _getIndex(self):
        return self._index + self._machine.relativeBase


class ImmediateParameter(Parameter):

    def get(self):
        result = self._get(self._index)
        return result

    def set(self, value: int):
        self._set(self._index, value)


_parameterClassesByMode = {0: AbsolutePositionalParameter,
                           1: ImmediateParameter,
                           2: RelativePositionalParameter}


def create(index: int, mode: int, machine: MachineBase) -> Parameter:
    parameterClass = _parameterClassesByMode[mode]
    parameter = parameterClass(index, machine)
    return parameter
