#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

import pyparsing as pp

from core.typesystem.TypeSystem import *

from core.exceptions.Exceptions import ParseException 


# --- Definition of the basic elements of the language.

# Defines open and closed brackets.
OB, CB = pp.Literal('(').suppress(), pp.Literal(')').suppress()

# Defines a string.
STRING = pp.dblQuotedString

# Defines the parse action for a string.
STRING.setParseAction(lambda s, l, t: StringType(t[0]))

# Defines a string to be used by the printout.
PRINTOUT_STRING = pp.QuotedString(quoteChar='"', multiline=True, escChar='\\')

# Defines the parse action for a string to be used by the printout.
PRINTOUT_STRING.setParseAction(lambda s, l, t: StringType(t[0]))

# Defines a comment removing the double quotes after the parsing.
COMMENT = pp.QuotedString('"', '\\', None, True, True, None).suppress()

# Defines a symbol.
SYMBOL = pp.Word(pp.alphas, pp.alphanums + '-_')

# Defines the parse action for a symbol.
SYMBOL.setParseAction(lambda s, l, t: SymbolType(t[0]))

# Defines an integer number.
SIGN = pp.oneOf('+ -')
INTEGER = pp.Combine(pp.Optional(SIGN) + pp.Word(pp.nums))

# Defines the parse action for an integer number.
INTEGER.setParseAction(lambda s, l, t: IntegerType(t[0]))

# Defines a floating point number.
UNSIGNED_INT = pp.Word(pp.nums)
INTEGER_PART = pp.Optional(SIGN) + pp.Word(pp.nums)
EXPONENT = pp.Combine(pp.oneOf('e E') + INTEGER)
FLOAT_1 = pp.Combine(INTEGER_PART + '.' + UNSIGNED_INT + pp.Optional(EXPONENT))
FLOAT_2 = pp.Combine(INTEGER_PART + EXPONENT)
FLOAT_3 = pp.Combine(INTEGER_PART + '.' + pp.Optional(EXPONENT))
FLOAT_4 = pp.Combine(pp.Optional(SIGN) + '.' + UNSIGNED_INT + pp.Optional(EXPONENT))
FLOAT = FLOAT_1 | FLOAT_2 | FLOAT_3 | FLOAT_4

# Defines the parse action for an unsigned integer number.
UNSIGNED_INT.setParseAction(lambda s, l, t: IntegerType(t[0]))

# Defines the parse action for a floating point number.
FLOAT.setParseAction(lambda s, l, t: FloatType(t[0]))

# Defines a boolean value.
BOOLEAN = pp.Literal('TRUE') | pp.Literal('FALSE')

# Defines the parse action for a boolean number.
BOOLEAN.setParseAction(lambda s, l, t: BooleanType(t[0]))

# --- Definition of the constructs for the declaration of the facts.

# Defines the name of the declaration of the facts.
DEFFACTS_NAME = SYMBOL

# Defines the name of a variable.
VARIABLE_SYMBOL = pp.Word(pp.alphas, pp.alphanums)

# Defines the name of a global variable.
GLOBAL_VARIABLE = pp.Combine(pp.Literal('?*') + SYMBOL + pp.Literal('*'))

# Defines the parse action for the name of a global variable.
GLOBAL_VARIABLE.setParseAction(lambda s, l, t: GlobalVariableType(t[0]))

# Defines the keywords reserved to the special function calls.
SPECIAL_FUNCTION_NAMES = (pp.Keyword('assert') | pp.Keyword('retract') | pp.Keyword('bind'))

# Defines the name of a function excluding the keyboards reserved to the special function calls.
FUNCTION_NAME = ~SPECIAL_FUNCTION_NAMES + pp.Word(pp.printables.translate(None, '()' + pp.nums), pp.printables.translate(None, '()'))

# Defines a constant.
CONSTANT = BOOLEAN | SYMBOL | STRING | FLOAT | INTEGER

# Initializes the calling of a function.
FUNCTION_CALL = pp.Forward()

# Defines the name of a single variable.
SINGLEFIELD_VARIABLE = pp.Combine(pp.Literal('?') + VARIABLE_SYMBOL)

# Defines the name of a variable.
VARIABLE = SINGLEFIELD_VARIABLE | GLOBAL_VARIABLE

# Defines an expression.
EXPRESSION = CONSTANT | VARIABLE | FUNCTION_CALL

# Defines the calling of a function.
FUNCTION_CALL << OB + FUNCTION_NAME + pp.ZeroOrMore(EXPRESSION) + CB

# Defines a field of an ordered pattern.
FACT_FIELD = GLOBAL_VARIABLE | CONSTANT | FUNCTION_CALL

# Defines an ordered pattern.
ORDERED_FACT_PATTERN = OB + pp.Group(SYMBOL + pp.Group(pp.ZeroOrMore(FACT_FIELD))) + CB

# Defines a pattern.
FACT_PATTERN = ORDERED_FACT_PATTERN

# Defines a list of patterns.
FACT_PATTERNS = pp.ZeroOrMore(FACT_PATTERN)

# Defines the construct for the declaration of a list of facts.
DEFFACTS_CONSTRUCT = OB + pp.Keyword('deffacts').suppress() + DEFFACTS_NAME + pp.Optional(COMMENT) + FACT_PATTERNS + CB

# Defines the parse action for the fields of a pattern of a fact.
FACT_FIELD.setParseAction(lambda s, l, t: t[0])

# Defines the parse action for the patterns of a fact.
FACT_PATTERNS.setParseAction(lambda s, l, t: t.asList())

# Defines the parse action for the calling of a function.
FUNCTION_CALL.setParseAction(lambda s, l, t: FunctionCallType(t[0], t[1:]))

# Defines the parse action which will be executed after the reading of a fact.
# It creates a couple of the form ('DEFFACTS_CONSTRUCT', list of the elements of the fact).
DEFFACTS_CONSTRUCT.setParseAction(lambda s, l, t: ('DEFFACTS_CONSTRUCT', [x for x in t]))

# --- Definition of the constructs for the declaration of the rules.

# Defines the name of a rule.
RULE_NAME = SYMBOL.copy()

# Defines an integer expression.
INTEGER_EXPRESSION = EXPRESSION

# Defines the declaration of the salience of a rule.
RULE_PROPERTY = OB + pp.Keyword('salience') + INTEGER_EXPRESSION + CB

# Defines the declaration of a rule.
DECLARATION = OB + pp.Group(pp.Keyword('declare').suppress() + pp.OneOrMore(RULE_PROPERTY)) + CB

# Initializes a condition in the left part of a rule.
CONDITIONAL_ELEMENT = pp.Forward()

# Defines a term for a constraint in the right part of a rule.
RHS_TERM = CONSTANT | VARIABLE | FUNCTION_CALL

# Defines a term for a constraint in the left part of a rule.
LHS_TERM = CONSTANT | GLOBAL_VARIABLE | SINGLEFIELD_VARIABLE

# Defines a constraint in the right part of a rule.
RHS_CONSTRAINT = RHS_TERM

# Defines a constraint in the left part of a rule.
LHS_CONSTRAINT = LHS_TERM

# Defines an ordered pattern in the left part of a rule.
ORDERED_PATTERN_CE = OB + SYMBOL + pp.Group(pp.ZeroOrMore(LHS_CONSTRAINT)) + CB

# Defines a pattern in the left part of a rule.
PATTERN_CE = ORDERED_PATTERN_CE

# Defines the parse action for the pattern.
PATTERN_CE.setParseAction(lambda s, l, t: t.asList())

# Defines a pattern with an assignment in the left part of a rule.
ASSIGNED_PATTERN_CE = SINGLEFIELD_VARIABLE + pp.Literal('<-').suppress() + PATTERN_CE

# Defines the parse action for an assignment of an instance of a fact to a variable.
ASSIGNED_PATTERN_CE.setParseAction(lambda s, l, t: AssignedPatternVariableType(t[0], t[1:]))

# Defines a checking condition to test a function in the left part of a rule.
TEST_CE = OB + pp.Keyword('test') + FUNCTION_CALL + CB

# Defines the parse action for the checking condition to test a function in the left part of a rule.
TEST_CE.setParseAction(lambda s, l, t: SpecialTestCallType(t[0], [t[1]]))

# Defines an 'and' conditional element between facts in the left part of a rule.
AND_CE = OB + pp.Keyword('and') + pp.OneOrMore(pp.Group(CONDITIONAL_ELEMENT)) + CB

# Defines the parse action for the 'and' conditional element between facts.
AND_CE.setParseAction(lambda s, l, t: ConditionalElementType(t[0], t[1:]))

# Defines an 'or' conditional element between facts in the left part of a rule.
OR_CE = OB + pp.Keyword('or') + pp.OneOrMore(pp.Group(CONDITIONAL_ELEMENT).setParseAction(lambda s, l, t: t.asList())) + CB

# Defines the parse action for the 'or' conditional element between facts.
OR_CE.setParseAction(lambda s, l, t: ConditionalElementType(t[0], t[1:]))

# Defines a 'not' conditional element of a fact in the left part of a rule.
NOT_CE = OB + pp.Keyword('not') + (pp.Group(CONDITIONAL_ELEMENT)) + CB

# Defines the parse action for the 'not' conditional element of a fact in the left part of a rule.
NOT_CE.setParseAction(lambda s, l, t: ConditionalElementType(t[0], t[1]))

# Defines a condition in the left part of a rule.
CONDITIONAL_ELEMENT << (BOOLEAN | TEST_CE | AND_CE | OR_CE | NOT_CE | PATTERN_CE | ASSIGNED_PATTERN_CE)

# Defines a list of conditions.
CONDITIONAL_ELEMENTS = pp.Group(pp.Group(PATTERN_CE | ASSIGNED_PATTERN_CE) + pp.ZeroOrMore(pp.Group(CONDITIONAL_ELEMENT)))

# Defines an ordered fact with possible variables of the assert.
ORDERED_RHS_PATTERN = OB + SYMBOL + pp.Group(pp.ZeroOrMore(RHS_CONSTRAINT)) + CB

# Defines a fact of the assert.
RHS_PATTERN = ORDERED_RHS_PATTERN

# Defines the parse action for a fact of the assert.
RHS_PATTERN.setParseAction(lambda s, l, t: t.asList())

# Defines the parse action for the list of facts of the assert.
RHS_PATTERNS = pp.OneOrMore(pp.Group(RHS_PATTERN)).setParseAction(lambda s, l, t: t.asList())

# Defines the call of a special function in the right part of a rule.
RHS_FUNCTION_CALL = OB + pp.Literal('assert') + RHS_PATTERNS + CB | \
    OB + pp.Literal('retract') + pp.OneOrMore(SINGLEFIELD_VARIABLE | UNSIGNED_INT) + CB | \
    OB + pp.Literal('bind') + VARIABLE + EXPRESSION + CB | \
    OB + pp.Literal('printout') + pp.OneOrMore(PRINTOUT_STRING | EXPRESSION) + CB | \
    OB + pp.Literal('strategy') + pp.oneOf('depth breadth random complexity simplicity lex mea') + CB

# Defines an action in the right part of a rule.
ACTION = RHS_FUNCTION_CALL

# Defines a list of actions in the right part of a rule.
ACTIONS = pp.Group(pp.ZeroOrMore(ACTION))

# Defines the construct for the declaration of a rule.
DEFRULE_CONSTRUCT = OB + pp.Keyword('defrule').suppress() + pp.Group(RULE_NAME + pp.Optional(COMMENT) + \
    pp.Optional(DECLARATION)).setParseAction(lambda s, l, t: t.asList()) + \
    CONDITIONAL_ELEMENTS + pp.Literal('=>').suppress() + ACTIONS + CB

# Defines the parse action for the name of a rule.
RULE_NAME.setParseAction(lambda s, l, t: SymbolType(t[0]))

# Defines the parse action for a declaration in the left part of a rule.
DECLARATION.setParseAction(lambda s, l, t: t.asList())

# Defines the parse action for a single variable.
SINGLEFIELD_VARIABLE.setParseAction(lambda s, l, t: SinglefieldVariableType(t[0]))

# Defines the parse action for a condition in the left part of a rule.
CONDITIONAL_ELEMENTS.setParseAction(lambda s, l, t: t.asList())

# Defines the parse action for an action in the right part of a rule.
ACTIONS.setParseAction(lambda s, l, t: t.asList())

# Defines the parse action for a special function.
RHS_FUNCTION_CALL.setParseAction(lambda s, l, t: SpecialFunctionCallType(t[0], t[1:]))

# Defines the parse action which will be executed after the reading of a rule.
# It builds a couple of the form ('DEFRULE_CONSTRUCT', list of the elements of the rule).
DEFRULE_CONSTRUCT.setParseAction(lambda s, l, t: ('DEFRULE_CONSTRUCT', [x for x in t]))

# --- Definition of the constructs for the declaration of the global variables.

# Defines the assignment of a global variable.
GLOBAL_ASSIGNMENT = GLOBAL_VARIABLE + pp.Literal('=') + EXPRESSION

# Defines the assignmento of multiple global variables.
DEFGLOBAL_CONSTRUCT = OB + pp.Keyword('defglobal').suppress() + pp.ZeroOrMore(GLOBAL_ASSIGNMENT) + CB

# Defines the parse action for the assignment of a global variable.
GLOBAL_ASSIGNMENT.setParseAction(lambda s, l, t: GlobalVariableType(t[0].name, t[2]))

# Defines the parse action which will be executed after the assignment of a global variable.
# It builds a couple of the form ('DEFGLOBAL_CONSTRUCT', list of the instanced variables).
DEFGLOBAL_CONSTRUCT.setParseAction(lambda s, l, t: ('DEFGLOBAL_CONSTRUCT', [x for x in t]))

# --- Definition of the constructs of a program.

# Defines a construct of the language.
CONSTRUCT = DEFFACTS_CONSTRUCT | DEFRULE_CONSTRUCT | DEFGLOBAL_CONSTRUCT

# Defines a single line comment before or after the construct.
LINE_COMMENT = pp.Combine(pp.OneOrMore(';')) + pp.restOfLine

# Defines a multiple line comment.
MULTILINE_COMMENT = pp.cStyleComment

# Defines the root of the grammar which represents the program.
PROGRAM = pp.ZeroOrMore(CONSTRUCT | LINE_COMMENT.suppress() | MULTILINE_COMMENT.suppress())

# --- Definition of the constructs of an assert.

ASSERT = OB + pp.Literal('assert') + RHS_PATTERNS + CB

# --- Definition of the constucts of a retract.

RETRACT = OB + pp.Literal('retract') + pp.OneOrMore(UNSIGNED_INT) + CB


class Parser(object):
    """
    Class for the parsing of a program of the system.
    """
    def __init__(self, debug=False):
        self.setDebug(debug)

    def setDebug(self, debug):
        DEFRULE_CONSTRUCT.setName('defrule')
        DEFRULE_CONSTRUCT.setDebug(debug)

        DEFFACTS_CONSTRUCT.setName('deffacts')
        DEFFACTS_CONSTRUCT.setDebug(debug)

        DEFGLOBAL_CONSTRUCT.setName('defglobal')
        DEFGLOBAL_CONSTRUCT.setDebug(debug)

        LINE_COMMENT.setName('comment')
        LINE_COMMENT.setDebug(debug)

    def parseAssert(self, text):
        try:
            parsed = ASSERT.parseString(text, parseAll=True).asList()
        except pp.ParseException as e:
            raise ParseException('Check for the appropriate syntax!', e.lineno, e.line)

        # Returns the AST built by the parser.
        return parsed

    def parseRetract(self, text):
        try:
            parsed = RETRACT.parseString(text, parseAll=True).asList()
        except pp.ParseException as e:
            raise ParseException('Check for the appropriate syntax!', e.lineno, e.line)

        # Returns the AST built by the parser.
        return parsed

    def parseProgram(self, text):
        try:
            parsed = PROGRAM.parseString(text, parseAll=True).asList()
        except pp.ParseException as e:
            raise ParseException('Check for the appropriate syntax!', e.lineno, e.line)

        # Returns the AST built by the parser.
        return parsed

    def parseFile(self, filename):
        # Loads the specified file to be read.
        resource = open(filename, 'r')

        # Reads the content of the opened file.
        text = resource.read()

        # Closes the opened file.
        resource.close()

        # Returns the AST built by the parser.
        return self.parseProgram(text)
