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

import random

import time


class Functions(Module):
    """
    Class for the representation of the available functions.
    """
    def __init__(self):
        Module.__init__(self)
        self.add_method('+', self.addition)
        self.add_method('-', self.subtraction)
        self.add_method('*', self.multiplication)
        self.add_method('/', self.division)
        self.add_method('%', self.module)
        self.add_method('**', self.power)
        self.add_method('abs', self.abs)
        self.add_method('min', self.minimum)
        self.add_method('max', self.maximum)
        self.add_method('strcat', self.strcat)
        self.add_method('substr', self.substr)
        self.add_method('strlen', self.strlen)
        self.add_method('strindex', self.strindex)
        self.add_method('symcat', self.symcat)
        self.add_method('randint', self.randint)

        random.seed(time.time())

    @unpack_args
    def addition(self, *args):
        if not len(args) > 1:
            raise EvaluateException('+ requires at least 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, NumberType) for x in args]:
            raise EvaluateException('+ requires all parameters to be numbers!')

        return reduce(op.add, args, IntegerType(0))

    @unpack_args
    def subtraction(self, *args):
        if not len(args) > 1:
            raise EvaluateException('- requires at least 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, NumberType) for x in args]:
            raise EvaluateException('- requires all parameters to be numbers!')

        return reduce(op.sub, args[1:], args[0])

    @unpack_args
    def multiplication(self, *args):
        if not len(args) > 1:
            raise EvaluateException('* requires at least 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, NumberType) for x in args]:
            raise EvaluateException('* requires all parameters to be numbers!')

        return reduce(op.mul, args, IntegerType(1))

    @unpack_args
    def division(self, *args):
        if not len(args) > 1:
            raise EvaluateException('\ requires at least 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, NumberType) for x in args]:
            raise EvaluateException('\ requires all parameters to be numbers!')
        
        elif 0 in [x.content for x in args[1:]]:
            raise EvaluateException('division by zero!')

        return reduce(op.div, args[1:], args[0])

    @unpack_args
    def module(self, *args):
        if not len(args) > 1:
            raise EvaluateException('% requires at least 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, NumberType) for x in args]:
            raise EvaluateException('% requires all parameters to be numbers!')
        
        elif 0 in [x.content for x in args[1:]]:
            raise EvaluateException('module by zero!')

        return reduce(op.mod, args[1:], args[0])

    @unpack_args
    def power(self, *args):
        if not len(args) > 1:
            raise EvaluateException('** requires at least 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, NumberType) for x in args]:
            raise EvaluateException('** requires all parameters to be numbers!')

        return reduce(op.pow, args[1:], args[0])

    @unpack_args
    def abs(self, *args):
        if not len(args) is 1:
            raise EvaluateException('Abs requires 1 parameter!')

        elif not isinstance(args[0], NumberType):
            raise EvaluateException('Abs requires all parameters to be numbers!')

        return op.abs(args[0])

    @unpack_args
    def minimum(self, *args):
        if not len(args) > 1:
            raise EvaluateException('Min requires at least 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, NumberType) for x in args]:
            raise EvaluateException('Min requires all parameters to be numbers!')

        return min(args)

    @unpack_args
    def maximum(self, *args):
        if not len(args) > 1:
            raise EvaluateException('Max requires at least 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, NumberType) for x in args]:
            raise EvaluateException('Max requires all parameters to be numbers!')

        return max(args)

    @unpack_args
    def strcat(self, *args):
        if not len(args) > 0:
            raise EvaluateException('Strcat requires at least 1 parameter!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, StringType) for x in args]:
            raise EvaluateException('Strcat requires all parameters to be strings!')

        return reduce(StringType.__add__, args[1:], args[0])

    @unpack_args
    def substr(self, *args):
        if not len(args) is 3:
            raise EvaluateException('Substr requires 3 parameters!' + ' (' + str(len(args)) + ' given).')

        elif not isinstance(args[0], StringType) or not isinstance(args[1], IntegerType) or not isinstance(args[2], IntegerType):
            raise EvaluateException('Substr requires 1 string and 2 integers!')

        return args[0].sub_string(args[1].content, args[2].content)

    @unpack_args
    def strlen(self, *args):
        if not len(args) is 1:
            raise EvaluateException('Strlen requires 1 parameter!' + ' (' + str(len(args)) + ' given).')

        elif not isinstance(args[0], StringType):
            raise EvaluateException('Strlen requires 1 string!')

        return IntegerType(StringType.str_length(args[0]))

    @unpack_args
    def strindex(self, *args):
        if not len(args) is 2:
            raise EvaluateException('Strindex requires 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif not isinstance(args[0], StringType) or not isinstance(args[1], StringType):
            raise EvaluateException('Strindex requires 2 strings!')

        return args[0].str_index(args[1].content)

    @unpack_args
    def symcat(self, *args):
        if not len(args) > 0:
            raise EvaluateException('Symcat requires at least 1 parameter!' + ' (' + str(len(args)) + ' given).')

        elif False in [isinstance(x, SymbolType) for x in args]:
            raise EvaluateException('Symcat requires 2 symbols!')

        return reduce(SymbolType.__add__, args[1:], args[0])

    @unpack_args
    def randint(self, *args):
        if not len(args) is 2:
            raise EvaluateException('Randint requires 2 parameters!' + ' (' + str(len(args)) + ' given).')

        elif not isinstance(args[0], IntegerType) or not isinstance(args[1], IntegerType):
            raise EvaluateException('Randint requires 2 integers!')

        step = 1

        if args[0] > args[1]:
            step = -1

        return IntegerType(random.randrange(args[0].content, args[1].content, step))
