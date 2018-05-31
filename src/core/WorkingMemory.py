#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

from core.exceptions.Exceptions import EvaluateException

from core.typesystem.TypeSystem import BaseType, VariableType

from core.entities.Fact import Fact

from collections import defaultdict


class WME(object):
    """
    Class for the representation of a Working Memory Element.
    """
    def __init__(self, identifier, fact):
        self.__identifier = identifier
        self.__fact = fact

    @property
    def identifier(self):
        return self.__identifier

    @identifier.setter
    def identifier(self, value):
        self.__identifier = value

    @property
    def fact(self):
        return self.__fact

    @fact.setter
    def fact(self, value):
        self.__fact = value

    def __str__(self):
        return str(self.__identifier) + ': ' + str(self.__fact)

    def __repr__(self):
        return str(self.__identifier) + ': ' + str(self.__fact)


class WorkingMemory(object):
    """
    Class for the representation of a Working Memory.
    """
    def __init__(self):
        self.__wmes = {}
        self.__facts = defaultdict(lambda: False)
        self.__counter = long(1)

    @property
    def wmes(self):
        return self.__wmes

    def add_fact(self, fact):
        # If the Working Memory doesn't contain a fact with
        # the name equal to the one of the specified fact,
        # then it adds that fact to the Working Memory
        # and it returns the generated WME.
        fact.values = [x.content if isinstance(x, VariableType) else x for x in fact.values]
        if False in [isinstance(x, BaseType) for x in fact.values]:
            raise EvaluateException('The fact "' + str(fact.name) + '" contains a null variable!')

        if not self.__facts[fact]:
            wme = WME(self.__counter, fact)
            self.__facts[fact] = True
            self.__wmes[self.__counter] = wme
            self.__counter += 1
            return wme
        # Otherwise, if the Working Memory already contains
        # a fact with the name equal to the one of the
        # specified fact, then it doesn't add any fact
        # to the Working Memory.
        else:
            return None

    def remove_fact(self, identifier):
        # If the Working Memory doesn't contain a fact
        # with the name qual to the one of the specified fact,
        # then it removes that fact from the Working Memory
        # and it returns the boolean value True.
        if identifier in self.__wmes:
            fact = self.__wmes[identifier].fact
            del self.__facts[fact]
            del self.__wmes[identifier]

            return True
        # Otherwise, if the Working Memory doesn't contain
        # a fact with the name equal to the one of the specified fact,
        # then it doesn't remove any fact from the Working Memory
        # and it returns the boolean value False.
        else:
            return False

    def __str__(self):
        if not self.__wmes:
            return 'Empty Working Memory.'
        else:
            line = ''

            for identifier in sorted(self.__wmes):
                fact = self.__wmes[identifier].fact
                line += 'f-' + str(identifier) + ' ' + str(fact) + '\n'

            line += 'for a total of '
            length = len(self.__wmes)

            if length > 1:
                line += str(length) + ' facts.'
            else:
                line += str(length) + ' fact.'

            return line

    def __repr__(self):
        return str(self)
