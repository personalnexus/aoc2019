from test import AllLinesTestBase as TestBase
from typing import List, DefaultDict
from collections import defaultdict
from math import ceil


class Chemical(object):

    def __init__(self, unit, name):
        self.unit = unit
        self.name = name

    @staticmethod
    def parse(s: str):
        unitAndName = (s.strip().split(' '))
        return Chemical(int(unitAndName[0]), unitAndName[1])

    def __mul__(self, i):
        return Chemical(i * self.unit, self.name)

    def __repr__(self):
        return f'{self.unit} {self.name}'


class Reaction(object):

    def __init__(self, s: str):
        inputsAndOutput = s.split('=>')
        self.inputs = [Chemical.parse(s) for s in inputsAndOutput[0].split(',')]
        self.output = Chemical.parse(inputsAndOutput[1])


class Reactor(object):

    def __init__(self, reactions):
        self.reactionsByOutputName = dict((r.output.name, r) for r in reactions)
        self.balanceByChemicalName: DefaultDict[str, int] = defaultdict(int)
        self.oreConsumption = 0

    def getChemical(self, c: Chemical):
        need = c.unit - self.balanceByChemicalName[c.name]
        if need <= 0:
            self.balanceByChemicalName[c.name] = -need
        else:
            reaction = self.reactionsByOutputName[c.name]
            multiplier = ceil(need / reaction.output.unit)
            for inputChemical in reaction.inputs:
                multipliedChemical = inputChemical * multiplier
                if inputChemical.name == 'ORE':
                    self.oreConsumption += multipliedChemical.unit
                else:
                    self.getChemical(multipliedChemical)
            self.balanceByChemicalName[c.name] += (multiplier * reaction.output.unit) - c.unit

    def __repr__(self):
        return f'Ore: {self.oreConsumption}, Balances: {self.balanceByChemicalName}'


class Day14(TestBase):

    def process(self, lines: List[str]):
        reactor = Reactor(Reaction(line) for line in lines)
        reactor.getChemical(Chemical(1, 'FUEL'))
        print(reactor)
        return reactor.oreConsumption

    def test(self):
        self.assertEqual(31, self.process(['10 ORE => 10 A',
                                           '1 ORE => 1 B',
                                           '7 A, 1 B => 1 C',
                                           '7 A, 1 C => 1 D',
                                           '7 A, 1 D => 1 E',
                                           '7 A, 1 E => 1 FUEL'
                                           ]))
        self.assertEqual(165, self.process(['9 ORE => 2 A',
                                            '8 ORE => 3 B',
                                            '7 ORE => 5 C',
                                            '3 A, 4 B => 1 AB',
                                            '5 B, 7 C => 1 BC',
                                            '4 C, 1 A => 1 CA',
                                            '2 AB, 3 BC, 4 CA => 1 FUEL'
                                            ]))
        self.assertEqual(180697, self.process(['2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG',
                                               '17 NVRVD, 3 JNWZP => 8 VPVL',
                                               '53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL',
                                               '22 VJHF, 37 MNCFX => 5 FWMGM',
                                               '139 ORE => 4 NVRVD',
                                               '144 ORE => 7 JNWZP',
                                               '5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC',
                                               '5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV',
                                               '145 ORE => 6 MNCFX',
                                               '1 NVRVD => 8 CXFTF',
                                               '1 VJHF, 6 MNCFX => 4 RFSQX',
                                               '176 ORE => 6 VJHF'
                                               ]))
        self.assertEqual(2210736, self.process(['171 ORE => 8 CNZTR',
                                                '7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL',
                                                '114 ORE => 4 BHXH',
                                                '14 VRPVC => 6 BMBT',
                                                '6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL',
                                                '6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT',
                                                '15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW',
                                                '13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW',
                                                '5 BMBT => 4 WPTQ',
                                                '189 ORE => 9 KTJDG',
                                                '1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP',
                                                '12 VRPVC, 27 CNZTR => 2 XDBXC',
                                                '15 KTJDG, 12 BHXH => 5 XCVML',
                                                '3 BHXH, 2 VRPVC => 7 MZWV',
                                                '121 ORE => 7 VRPVC',
                                                '7 XCVML => 6 RJRHP',
                                                '5 BHXH, 4 VRPVC => 5 LTCX'
                                                ]))
