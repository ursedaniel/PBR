#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

from core.entities.Fact import Fact


class OrderedFact(Fact):
    """
    Class for the representation of an ordered fact.
    """
    def __init__(self, name, values=[]):
        Fact.__init__(self, name)

        # Attributes of the fact.
        self.__values = values

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self, values):
        self.__values = values

    def add_attribute(self, attribute):
        self.__values.append(attribute)

    def get_attribute(self, index):
        return self.__values[index]

    def set_attribute(self, index, item):
        self.__values[index] = item

    def __eq__(self, other):
        return self.name == other.name and self.__values == other.__values

    def __str__(self):
        if self.__values:
            return '(' + str(self.name) + ' ' + ' '.join([str(x) for x in self.__values]) + ')'
        else:
            return '(' + str(self.name) + ')'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.name, tuple(self.__values)))
