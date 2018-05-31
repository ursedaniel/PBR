#!/usr/bin/env python

import sys

from Module import unpack_args, Module

from core.typesystem.TypeSystem import *

from core.entities.OrderedFact import OrderedFact

from core.exceptions.Exceptions import EvaluateException


class SpecialFunctions(Module):
    """
    Class for the representation of the available special functions.
    """
    def __init__(self):
        Module.__init__(self)
        self.add_method('printout', self.printout)
        self.add_method('assert', self.assertion)
        self.add_method('retract', self.retract)
        self.add_method('bind', self.bind)
        self.add_method('test', self.test)
        self.add_method('strategy', self.strategy)

    @unpack_args
    def printout(self, *args):
        for arg in args[1:]:
            sys.stdout.write(str(arg) + ' ')

        sys.stdout.write('\n')

    @unpack_args
    def assertion(self, *args):
        network = args[0]

        for fact in args[1:]:
            ordered_fact = OrderedFact(fact[0], fact[1])

            network.assert_fact(ordered_fact)

    @unpack_args
    def test(self, *args):
        if False in [isinstance(x, BooleanType) for x in args[1:]]:
            raise EvaluateException('The \"test\" predicate takes only boolean parameters!')

        return args[1]

    @unpack_args
    def retract(self, *args):
        network = args[0]

        for arg in args[1:]:
            network.retract_fact(arg.content)

    @unpack_args
    def bind(self, *args):
        network = args[0]

        environment = network.evaluator.environment

        if isinstance(args[1], SinglefieldVariableType):
            environment.set_local_variable(SinglefieldVariableType(args[1].name, args[2]))

        elif isinstance(args[1], GlobalVariableType):
            environment.set_global_variable(GlobalVariableType(args[1].name, args[2]))

    @unpack_args
    def strategy(self, *args):
        network = args[0]

        if args[1] in network.agenda.strategies:
            network.agenda.change_strategy(network.agenda.strategies[args[1]]())
            return True
        else:
            return False
