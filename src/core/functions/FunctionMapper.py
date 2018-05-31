#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

import os

from inspect import imp, getmembers

from core.exceptions.Exceptions import EvaluateException


class FunctionMapper(object):
    """
    Class for the representation of a mapper of functions.
    In particular, it loads the modules containing
    the functions available to the user.
    """
    def __init__(self):
        self.__map = {}

    def get_method(self, name):
        try:
            # Returns the function which presents the specified name.
            return self.__map[name]
        except KeyError:
            # Raises an exception in the case in which the function is not present.
            raise EvaluateException('Unable to find the function ' + name + '!')

    def load_class(self, name):
        # Saves the list of the names of the functions contained in the specified module.
        keys = name().get_names()

        for key in keys:
            # If the considered function of the module is not already present in the system,
            # then it saves a reference to that function in the dictionary.
            if not key in self.__map:
                self.__map[key] = name().get_method(key)

    def load_file(self, filename):
        # Saves the name and the extension of the file. It assumes that the class
        # to be loaded has the same name of the module (.py or .pyc file).
        mod_name, file_ext = os.path.splitext(os.path.split(filename)[-1])

        py_mod = None

        # If the file has .py extension, then it loads that module.
        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, filename)

        # If the file has .pyc extension, then it loads that module.
        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filename)

        else:
            raise EvaluateException('Unable to find the file ' + filename + '!')

        # Builds the list of the classes contained in the module.
        classes = [u for (v, u) in getmembers(py_mod, isclass) if v.startswith(mod_name)]

        # Loads the classes contained in the module.
        for c in classes:
            self.load_class(c)

    def load_directory(self, directory):
        # Specifies the directory which contains the modules to be loaded.
        os.chdir(directory)

        # Loads the .py and .pyc files found in the specified directory.
        for f in os.listdir('.'):
            if f.endswith('.py'):
                self.load_file(f)

            elif f.endswith('.pyc'):
                self.load_file(f)
