#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

from core.exceptions.Exceptions import EvaluateException

from core.typesystem.TypeSystem import *

from core.typesystem.TypeSystem import *

from collections import defaultdict


class Evaluator(object):
    """
    Class for the evaluation of an AST (Abstract Syntax Tree).
    """
    def __init__(self, environment, function_mapper):
        # Saves a reference to the specified environment.
        self.__environment = environment

        # Saves a reference to the specified function mapper.
        self.__function_mapper = function_mapper

        # Flag which specifies the evaluation mode.
        self.__test_mode = False

        # Dictionary which maps types to methods which evaluate them.
        self.__type_evaluators = defaultdict(lambda: self.default)

        # Builds the dictionary which maps types to methods which evaluate them.
        self.__init_type_evaluators()

    def __init_type_evaluators(self):
        self.__add_type_evaluator(IntegerType, self.visitIntegerType)
        self.__add_type_evaluator(FloatType, self.visitFloatType)
        self.__add_type_evaluator(LexemeType, self.visitLexemeType)
        self.__add_type_evaluator(SymbolType, self.visitSymbolType)
        self.__add_type_evaluator(StringType, self.visitStringType)
        self.__add_type_evaluator(list, self.visitList)
        self.__add_type_evaluator(GlobalVariableType, self.visitGlobalVariableType)
        self.__add_type_evaluator(SinglefieldVariableType, self.visitSinglefieldVariableType)
        self.__add_type_evaluator(FunctionCallType, self.visitFunctionCallType)
        self.__add_type_evaluator(SpecialFunctionCallType, self.visitSpecialFunctionCallType)
        self.__add_type_evaluator(SpecialTestCallType, self.visitSpecialTestCallType)
        self.__add_type_evaluator(ConditionalElementType, self.visitConditionalElementType)

    def __add_type_evaluator(self, class_type, evaluator):
        self.__type_evaluators[class_type] = evaluator

    @property
    def environment(self):
        return self.__environment

    @environment.setter
    def environment(self, value):
        self.__environment = value

    @property
    def test_mode(self):
        return self.__test_mode

    def evaluate(self, node, test_mode=False, variables={}):
        self.__test_mode = test_mode

        if variables:
            if test_mode:
                self.__environment.test_variables = variables
            else:
                self.__environment.local_variables = variables

        return self.__type_evaluators[type(node)](node)

    def default(self, node):
        return node

    def visitIntegerType(self, node):
        return node

    def visitFloatType(self, node):
        return node

    def visitLexemeType(self, node):
        return node

    def visitSymbolType(self, node):
        return node

    def visitStringType(self, node):
        return node

    def visitList(self, node):
        return [self.evaluate(x, self.__test_mode) for x in node]

    def visitGlobalVariableType(self, node):
        value = self.__environment.get_global_variable(node)

        if value is None:
            raise EvaluateException('The global variable ' + node.name + ' has not been instanced!')
        else:
            node.content = value
            return node

    def visitSinglefieldVariableType(self, node):
        if self.__test_mode is True:
            value = self.__environment.get_test_variable(node)
        else:
            value = self.__environment.get_local_variable(node)

        if value is not None:
            node.content = self.evaluate(value, self.__test_mode)

        return node

    def visitFunctionCallType(self, node):
        node.function = self.__function_mapper.get_method(node.name)

        return node.evaluate(self)

    def visitSpecialFunctionCallType(self, node):
        node.function = self.__function_mapper.get_method(node.name)

        return node.evaluate(self)

    def visitSpecialTestCallType(self, node):
        node.function = self.__function_mapper.get_method(node.name)

        return node.evaluate(self)

    def visitConditionalElementType(self, node):
        node.patterns = [self.evaluate(x, self.__test_mode) for x in node.patterns]
        return node
