#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""


class ProductionMemory(object):
    """
    Class for the representation of a Production Memory.
    """
    def __init__(self):
        self.__rules = {}

    @property
    def rules(self):
        return self.__rules.values()

    def add_rule(self, rule):
        # If the Production Memory contains a rule with the name equal to
        # the one of the specified rule, then it replaces that rule
        # with the specified one and it returns the boolean value False.
        if rule.name in self.__rules:
            self.__rules[rule.name] = rule
            return False
        # Otherwise, if the Production Memory doesn't contain a rule
        # with the name equal to the one of the specified rule, then
        # it adds that rule to the Production Memory and it returns
        # the boolean value True.
        else:
            self.__rules[rule.name] = rule
            return True

    def remove_rule(self, rule):
        # If the Production Memory contains a rule with the name equal to
        # the one of the specified rule, then it removes that rule from
        # the Production Memory and it returns the boolean value True.
        if rule.name in self.__rules:
            del self.__rules[rule.name]
            return True
        # Otherwise, if the Production Memory doesn't contain any rule
        # with the name equal to the one of the spcified rule, then
        # it doesn't remove any rule from the Production Memory
        # and it returns the boolean value False.
        else:
            return False

    def __str__(self):
        if not self.__rules:
            return 'Empty Production Memory.\n'
        else:
            line = ''

            for rule in self.__rules.values():
                line += str(rule.name) + '\n'

            return line

    def __repr__(self):
        return str(self)
