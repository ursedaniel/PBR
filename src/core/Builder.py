#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

from core.parser.Parser import Parser

from core.typesystem.TypeSystem import *

from core.Evaluator import Evaluator

from core.functions.FunctionMapper import FunctionMapper

from core.functions.SpecialFunctions import SpecialFunctions

from core.functions.Functions import Functions

from core.functions.Predicates import Predicates

from core.Environment import Environment

from core.WorkingMemory import WorkingMemory

from core.ProductionMemory import ProductionMemory

from core.entities.OrderedFact import OrderedFact

from core.entities.Rule import Rule


class Builder(object):
    """
    Class for the building of the working memory and
    the production memory after the parsing and
    the preliminary evaluation of a sequence
    of facts and rules.
    """
    def __init__(self):
        # Saves an instance of the Environment class.
        self.__environment = Environment()

        # Saves an instance of the FunctionMapper class.
        self.__function_mapper = FunctionMapper()

        # Loads the module containing the special functions available to the user.
        self.__function_mapper.load_class(SpecialFunctions)

        # Loads the module containing the functions available to the user.
        self.__function_mapper.load_class(Functions)

        # Loads the module containing the predicates available to the user.
        self.__function_mapper.load_class(Predicates)

        # Saves an instance of the Evaluator class, which requires as parameters
        # the references to the instances of the Environment containing the global variables
        # and of the FunctionMapper containing the mappings between the names of the functions
        # and the predicates available to the users and the corresponding implementations.
        self.__evaluator = Evaluator(self.__environment, self.__function_mapper)

    @property
    def evaluator(self):
        return self.__evaluator

    @evaluator.setter
    def evaluator(self, value):
        self.__evaluator = value

    def build(self, AST):
        # Saves a list to contain the facts.
        facts = []

        # Memorizza a list to contain the rules.
        rules = []

        for (item_type, item_content) in AST:
            # If the construct corresponds to the definition of a global variable, then
            # it is evaluated and the result is added in the set of global variables.
            if item_type == 'DEFGLOBAL_CONSTRUCT':
                for assignment in item_content:
                    print 'Defining defglobal:', assignment.name
                    assignment.content = self.__evaluator.evaluate(assignment.content)
                    self.__environment.set_global_variable(assignment)

            # If the construct corresponds to the definition of a list of facts, then
            # the attributes of each fact are evaluated and the fact is added to the list of facts.
            elif item_type == 'DEFFACTS_CONSTRUCT':
                print 'Defining deffacts:', item_content[0]
                for fact in item_content[1:]:
                    for i in xrange(len(fact[1])):
                        # Evaluates each attribute of the considered fact.
                        fact[1][i] = self.__evaluator.evaluate(fact[1][i])

                    # Saves an instance of the considered fact
                    # specifying its name and its attributes.
                    f = OrderedFact(fact[0], fact[1])

                    # Adds the current fact to the list of facts.
                    facts.append(f)

            # If the construct corresponds to the definition of a rule, then
            # its left and right parts are preliminarly evaluated and the rule
            # is added to the list of rules. Possible non global variables
            # will be evaluated after the matching phase between facts and rules.
            elif item_type == 'DEFRULE_CONSTRUCT':
                name = item_content[0][0]
                print 'Defining defrule:', name

                # Saves an instance of the considered rule.
                r = Rule(name)

                # If the rule contains a value of the salience,
                # then it is saved in the instance of the rule.
                if len(item_content[0]) > 1:
                    if item_content[0][1][0] is 'salience':
                        r.salience = item_content[0][1][1].content

                # Saves the left part in the instance of the rule.
                lhs = item_content[1]

                # Evaluates each element of the left part of the rule.
                for i in xrange(len(lhs)):

                    # Checks if the element of the left part of the rule represents a test.
                    if isinstance(lhs[i][0], SpecialTestCallType):

                        # Builds the set of the variables contained in the test.
                        lhs[i][0].build()

                        # Builds, in the rule containing the test, a dictionary in the form:
                        # variable_involved_in_the_test : list_of_references_to_tests_which_contains_it.
                        for v in lhs[i][0].test_variables:
                            if not v in r.variable_tests:
                                r.variable_tests[v] = set([lhs[i][0]])
                            else:
                                r.variable_tests[v].add(lhs[i][0])

                        # Adds the test to instance of the rule.
                        r.tests.add(lhs[i][0])

                    else:
                        # If the current element of the left part
                        # of the rule is not a test, then it is evaluated.
                        lhs[i] = self.__evaluator.evaluate(lhs[i])

                        # Adds the current element to the left part of the instance of the rule.
                        r.lhs.append(lhs[i])

                # Evaluates the complexity of the rule.
                r.evaluate_complexity()

                # Saves the right part in the instance of the rule.
                r.rhs = item_content[2]

                # Adds the rule to the list of rules.
                rules.append(r)

        # Returns the lists of identified facts and rules.
        return (facts, rules)

    def build_assert(self, ast):
        facts = []

        for fact in ast[1:]:
            print 'Defining fact:', fact[0]

            for i in xrange(len(fact[1])):
                # Evaluates each attribute of the considered fact.
                fact[1][i] = self.__evaluator.evaluate(fact[1][i])

            # Saves an instance of the considered fact
            # specifying its name and its attributes.
            f = OrderedFact(fact[0], fact[1])

            # Adds the considered fact to the Working Memory.
            facts.append(f)

        return facts

    def reset(self):
        self.__environment.clear_local_variables()
        self.__environment.clear_test_variables()
        self.__evaluator = Evaluator(self.__environment, self.__function_mapper)
