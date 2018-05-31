#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""


class Environment(object):
    """
    Class for the representation of the sets of instanced variables.
    """
    def __init__(self):
        # Dictionary of the global variables.
        self.__global_variables = {}

        # Dictionary of the singlefield and multifield variables.
        self.__local_variables = {}

        # Dictionary of the variables used in tests.
        self.__test_variables = {}

    @property
    def global_variables(self):
        return self.__global_variables

    @global_variables.setter
    def global_variables(self, values):
        self.__global_variables = values

    @property
    def local_variables(self):
        return self.__local_variables

    @local_variables.setter
    def local_variables(self, values):
        self.__local_variables = values

    @property
    def test_variables(self):
        return self.__test_variables

    @test_variables.setter
    def test_variables(self, values):
        self.__test_variables = values

    def clear_global_variables(self):
        self.__globals = {}

    def clear_local_variables(self):
        self.__local_variables = {}

    def clear_test_variables(self):
        self.__test_variables = {}

    def set_global_variable(self, variable):
        # Sets the global variable in the dictionary.
        self.__global_variables[variable] = variable.content

    def set_local_variable(self, variable):
        # Sets the local variable in the dictionary.
        self.__local_variables[variable] = variable.content

    def set_test_variable(self, variable):
        # Sets the variable used in the tests in the dictionary.
        self.__test_variables[variable] = variable.content

    def get_global_variable(self, variable):
        try:
            return self.__global_variables[variable]
        except KeyError:
            return None

    def get_local_variable(self, variable):
        try:
            return self.__local_variables[variable]
        except KeyError:
            return None

    def get_test_variable(self, variable):
        try:
            return self.__test_variables[variable]
        except KeyError:
            return None

    def __str__(self):
        return str(self.__global_variables) + '\n' + str(self.__local_variables)

    def __repr__(self):
        return str(self.__global_variables) + '\n' + str(self.__local_variables)
