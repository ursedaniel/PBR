#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""


class Token(object):
    """
    Class for the representation of a token.
    """
    def __init__(self, parent, wme):
        self.__parent = parent
        self.__wme = wme
        self.__wme_indexes = []

        if parent is not None:
            self.__wme_indexes.extend(parent.__wme_indexes)
            self.__head = parent.__head
        else:
            self.__head = self
        self.__wme_indexes.append(wme.identifier)

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def wme(self):
        return self.__wme

    @wme.setter
    def wme(self, value):
        self.__wme = value

    @property
    def wme_indexes(self):
        return self.__wme_indexes

    def __str__(self):
        if self.__parent is not None:
            return '<' + str(self.__parent) + ', ' + str(self.__wme) + '>'
        else:
            return '<' + str(self.__wme) + '>'

    def __repr__(self):
        if self.__parent is not None:
            return '<' + str(self.__parent) + ', ' + str(self.__wme) + '>'
        else:
            return '<' + str(self.__wme) + '>'
