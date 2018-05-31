#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""


class Fact(object):
    """
    Abstract class for the representation of a fact.
    """
    def __init__(self, name):
        # Name of the fact.
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def values(self):
        raise NotImplementedError('Fact has not been implemented yet!')

    @values.setter
    def values(self, values):
        raise NotImplementedError('Fact has not been implemented yet!')
