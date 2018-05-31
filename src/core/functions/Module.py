#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""


# Definition of the decorator which
# unpacks from tuples to lists.
def unpack_args(function):
    def f(self, *args):
        if isinstance(args, tuple):
            args = args[0]
        return function(self, *args)
    return f


class Module(object):
    """
    Class for the representation of a module.
    """
    def __init__(self):
        # Dictionary which maps the names of the loaded functions
        # to the implementstions of the functions which presents these names.
        self.functions = {}

    def get_names(self):
        # Returns the names of all available functions.
        return self.functions.keys()

    def add_method(self, name, function):
        # Sets a mapping between the name of a function and its implementstion.
        self.functions[name] = function

    def get_method(self, name):
        # Returns the function with the specified name.
        return self.functions[name]
