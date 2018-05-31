#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""


class BaseException(Exception):
    """
    Class for the representation of a generic exception.
    """
    pass


class EvaluateException(BaseException):
    """
    Class for the representation of an exception
    raised during the evaluation of an expression.
    """
    def __init__(self, message):
        # Message of the evaluation error.
        self.__message = message

    @property
    def message(self):
        return self.__message

    def __str__(self):
        return '[EVALUATION ERROR]: ' + self.__message

    def __repr__(self):
        return self.__message


class ParseException(BaseException):
    """
    Class for the representation of an exception
    raised during the parsing of a program.
    """
    def __init__(self, message, line_number, line):
        # Message of the parsing error.
        self.__message = message

        # Line number of the error.
        self.__line_number = line_number

        # Line of the error.
        self.__line = line

    @property
    def message(self):
        return self.__message

    @property
    def line_number(self):
        return self.__line_number

    @property
    def line(self):
        return self.__line

    def __str__(self):
        return '[SYNTAX ERROR AT LINE ' + str(self.__line_number) + '] ' + self.__message + '\n' + 'Line: \"' + self.__line + '\"'
