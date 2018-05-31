#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

import operator as op

from Module import unpack_args, Module

from core.typesystem.TypeSystem import *

from core.exceptions.Exceptions import EvaluateException


class Predicates(Module):
    """
    Class for the representation of the available predicates.
    """
    def __init__(self):
        Module.__init__(self)
        self.add_method('eq', self.equal)
        self.add_method('neq', self.not_equal)
        self.add_method('<', self.less_than)
        self.add_method('<=', self.less_equal)
        self.add_method('>', self.greater_than)
        self.add_method('>=', self.greater_equal)
        self.add_method('and', self.logical_and)
        self.add_method('or', self.logical_or)
        self.add_method('not', self.logical_not)

    def __boolean_converter(self, value):
        return BooleanType('TRUE') if value is True else BooleanType('FALSE')

    @unpack_args
    def equal(self, *args):
        return self.__boolean_converter(all([args[0] == x for x in args[1:]]))

    @unpack_args
    def not_equal(self, *args):
        return self.__boolean_converter(all([args[0] != x for x in args[1:]]))

    @unpack_args
    def less_than(self, *args):
        return self.__boolean_converter(all([x < y for (x, y) in zip(args, args[1:])]))

    @unpack_args
    def less_equal(self, *args):
        return self.__boolean_converter(all([x <= y for (x, y) in zip(args, args[1:])]))

    @unpack_args
    def greater_than(self, *args):
        return self.__boolean_converter(all([x > y for (x, y) in zip(args, args[1:])]))

    @unpack_args
    def greater_equal(self, *args):
        return self.__boolean_converter(all([x >= y for (x, y) in zip(args, args[1:])]))

    @unpack_args
    def logical_and(self, *args):
        if False in [isinstance(x, BooleanType) for x in args]:
            raise EvaluateException('The \"and\" predicate takes only boolean parameters!')

        return self.__boolean_converter(not False in [x.content for x in args])

    @unpack_args
    def logical_or(self, *args):
        if False in [isinstance(x, BooleanType) for x in args]:
            raise EvaluateException('The \"or\" predicate takes only boolean parameters!')

        return self.__boolean_converter(True in [x.content for x in args])

    @unpack_args
    def logical_not(self, *args):
        if False in [isinstance(x, BooleanType) for x in args]:
            raise EvaluateException('The \"not\" predicate takes only boolean parameters!')

        if len(args) != 1:
            raise EvaluateException('The \"not\" predicate takes only one parameter!')

        return self.__boolean_converter(not args[0].content)
