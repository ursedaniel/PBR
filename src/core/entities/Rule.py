#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

from core.typesystem.TypeSystem import FunctionCallType


class Rule(object):
    """
    Class for the representation of a rule.
    """
    def __init__(self, name, salience=0):
        # Name of the rule.
        self.__name = name

        # Salience of the rule.
        self.__salience = salience

        # Left part of the rule.
        self.__lhs = []

        # Right part of the rule.
        self.__rhs = []

        # Set of the tests contained in the rule.
        self.__tests = set()

        # Dictionary which maps the variables contained
        # in the tests to the tests themselves.
        self.__variable_tests = {}

        # Complexity of the rule.
        self.__complexity = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def salience(self):
        return self.__salience

    @salience.setter
    def salience(self, salience):
        self.__salience = salience

    @property
    def lhs(self):
        return self.__lhs

    @lhs.setter
    def lhs(self, lhs):
        self.__lhs = lhs

    @property
    def rhs(self):
        return self.__rhs

    @rhs.setter
    def rhs(self, rhs):
        self.__rhs = rhs

    @property
    def tests(self):
        return self.__tests

    @tests.setter
    def tests(self, values):
        self.__tests = values

    @property
    def variable_tests(self):
        return self.__variable_tests

    @variable_tests.setter
    def variable_tests(self, values):
        self.__variable_tests = values

    @property
    def complexity(self):
        return self.__complexity

    def evaluate_complexity(self):
        # The complexity of the rule is given by:
        # +1 for every pattern.
        # +1 for every unique variable found in the test.
        # +1 for every unique function or predicate found in the test.
        self.__complexity = len(self.__lhs) + len(self.__variable_tests)

        for test in self.__tests:
            self.__evaluate_complexity(test.parameters)

    def __evaluate_complexity(self, parameters):
            if parameters[0].name in ['and', 'or', 'not']:
                self.__evaluate_complexity(parameters[0].parameters)
            else:
                self.__complexity += 1
                for parameter in parameters:
                    if isinstance(parameter, FunctionCallType):
                        self.__complexity += 1

    def __str__(self):
        return str(self.__name) + ' {salience = ' + str(self.__salience) + '} ' + str(self.__lhs) + ' => ' + str(self.__rhs) + str(self.__tests)

    def __repr__(self):
        return str(self.__name) + ' {salience = ' + str(self.__salience) + '} ' + str(self.__lhs) + ' => ' + str(self.__rhs) + str(self.__tests)
