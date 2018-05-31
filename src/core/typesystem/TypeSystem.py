#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

from core.exceptions.Exceptions import EvaluateException


class BaseType(object):
    """
    Class for the representation of a generic type.
    """
    pass


class BooleanType(BaseType):
    """
    Class for the representation of a boolean type.
    """
    def __init__(self, content):
        self.__content = False
        values = {'TRUE': True, 'FALSE': False}
        if content in values:
            self.__content = values[content]

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    def __eq__(self, other):
        return self.__content == other.__content

    def logical_not(self):
        return not self.__content

    def logical_and(self, other):
        return self.__content and other.__content

    def logical_or(self, other):
        return self.__content or other.__content

    def __str__(self):
        return 'TRUE' if self.__content is True else 'FALSE'

    def __repr__(self, ):
        return 'TRUE' if self.__content is True else 'FALSE'

    def __hash__(self):
        return hash(str(self.__content))


class NumberType(BaseType):
    """
    Class for the representation of a generic number.
    """
    def __init__(self, content):
        self.__content = content

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    def type_promotion(self, a, b):
        if a.__class__ == b.__class__:
            return a.__class__
        else:
            return FloatType

    def __add__(self, other):
        t = self.type_promotion(self, other)
        return t(self.content + other.content)

    def __sub__(self, other):
        t = self.type_promotion(self, other)
        return t(self.content - other.content)

    def __mul__(self, other):
        t = self.type_promotion(self, other)
        return t(self.content * other.content)

    def __div__(self, other):
        return FloatType(float(self.content) / other.content)

    def __mod__(self, other):
        t = self.type_promotion(self, other)
        return t(self.content % other.content)

    def __pow__(self, other):
        t = self.type_promotion(self, other)
        return t(self.content ** other.content)

    def __neg__(self):
        return self.content.__class__(- self.content)

    def logical_and(self, other):
        t = self.type_promotion(self, other)
        return t(self.content and other.content)

    def logical_or(self, other):
        t = self.type_promotion(self, other)
        return t(self.content or other.content)

    def __abs__(self):
        return self.__class__(abs(self.content))

    def __lt__(self, other):
        if isinstance(other, NumberType):
            return self.content < other.content
        else:
            return False

    def __le__(self, other):
        if isinstance(other, NumberType):
            return self.content <= other.content
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, NumberType):
            return self.content > other.content
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, NumberType):
            return self.content >= other.content
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, NumberType):
            return self.content == other.content
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, NumberType):
            return self.content != other.content
        else:
            return True

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return str(self.content)

    def __hash__(self):
        return hash(str(self.__content))


class IntegerType(NumberType):
    """
    Class for the representation of an integer number.
    """
    def __init__(self, content):
        NumberType.__init__(self, int(content))


class FloatType(NumberType):
    """
    Class for the representation of a floating point number.
    """
    def __init__(self, content):
        NumberType.__init__(self, float(content))


class LexemeType(BaseType):
    """
    Class for the representation of generic text.
    """
    def __init__(self, content):
        self.__content = content

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    def __eq__(self, other):
        return self.content == other.content

    def __ne__(self, other):
        return self.content != other.content

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return str(self.content)

    def __hash__(self):
        return hash(str(self.__content))


class SymbolType(LexemeType):
    """
    Class for the representation of a symbol.
    """
    def __init__(self, content):
        LexemeType.__init__(self, str(content))

    def __add__(self, other):
        return SymbolType(self.content + other.content)


class StringType(LexemeType):
    """
    Class for the representation of a string.
    """
    def __init__(self, content):
        LexemeType.__init__(self, str(content))

    def __add__(self, other):
        return StringType(self.content[:-1] + other.content[1:])

    def sub_string(self, start, end):
        return StringType('\"' + (self.content).replace('\"', '')[start:end] + '\"')

    def str_index(self, text):
        return IntegerType(self.content.replace('\"', '').find(text.replace('\"', '')))

    def str_length(self):
        return len(self.content) - 2

    def __lt__(self, other):
        if isinstance(other, StringType):
            return self.content < other.content
        else:
            return False

    def __le__(self, other):
        if isinstance(other, StringType):
            return self.content <= other.content
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, StringType):
            return self.content > other.content
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, StringType):
            return self.content >= other.content
        else:
            return False


class FunctionType(BaseType):
    """
    Class for the representation of a generic function.
    """
    def __init__(self, name, parameters):
        self.__name = name
        self.__function = None
        self.__parameters = parameters

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__parameters = value

    @property
    def function(self):
        return self.__function

    @function.setter
    def function(self, value):
        self.__function = value


class FunctionCallType(FunctionType):
    """
    Class for the representation of a function.
    """
    def __init__(self, name, parameters):
        FunctionType.__init__(self, name, parameters)

    def evaluate(self, evaluator):
        return self.function([x.content if isinstance(x, VariableType) else x for x in evaluator.evaluate(self.parameters, evaluator.test_mode)])

    def __str__(self):
        return 'FunctionCall: (' + self.name + ' ' + ' '.join([str(x) for x in self.parameters]) + ')'

    def __repr__(self):
        return 'FunctionCall: (' + self.name + ' ' + ' '.join([str(x) for x in self.parameters]) + ')'


class SpecialFunctionCallType(FunctionType):
    """
    Class for the representation of a special function.
    It defines the functions callable in the right part
    of a rule as special functions.
    """
    def __init__(self, name, parameters):
        FunctionType.__init__(self, name, parameters)
        self.__caller = None

    @property
    def caller(self):
        return self.__caller

    @caller.setter
    def caller(self, value):
        self.__caller = value

    def validate(self):
        # Verifies that the function can be evalued. In particular, it verifies if
        # the method which evaluates the function is present, if any of the parameter
        # is a pattern or a function and if the variables are all instanced.
        if self.function is None:
            return False

        for parameter in self.parameters:
            if isinstance(parameter, FunctionCallType):
                return False

        return True

    def evaluate(self, evaluator):
        return self.function([self.caller] + evaluator.evaluate(self.parameters, evaluator.test_mode))

    def __str__(self):
        return 'SpecialFunctionCall: (' + self.name + ' ' + ' '.join(['(' + str(x) + ')' for x in self.parameters]) + ')'

    def __repr__(self):
        return 'SpecialFunctionCall: (' + self.name + ' ' + ' '.join(['(' + str(x) + ')' for x in self.parameters]) + ')'

class SpecialTestCallType(SpecialFunctionCallType):
    """
    Class for the representation of a test, in order to
    verify predicates on one or more variables.
    """
    def __init__(self, name, parameters):
        SpecialFunctionCallType.__init__(self, name, parameters)
        self.__test_variables = set()

    @property
    def test_variables(self):
        return self.__test_variables

    def evaluate(self, evaluator):
        return self.function([self.caller] + evaluator.evaluate(self.parameters, evaluator.test_mode)).content

    def build(self):
        self.__build(self.parameters)

    def __build(self, parameters):
        for p in parameters:
            if isinstance(p, VariableType):
                self.__test_variables.add(p)
            elif isinstance(p, FunctionCallType):
                self.__build(p.parameters)

    def __str__(self):
        return 'SpecialTestCall: (' + self.name + ' ' + ' '.join(['(' + str(x) + ')' for x in self.parameters]) + ' test variables: ' + str(self.__test_variables) + ')'

    def __repr__(self):
        return 'SpecialTestCall: (' + self.name + ' ' + ' '.join(['(' + str(x) + ')' for x in self.parameters]) + ')'

class VariableType(BaseType):
    """
    Class for the representation of a generic variable.
    """
    def __init__(self, name, content=None):
        self.__name = name
        self.__content = content

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    def is_instanced(self):
        return self.__content is not None

    def __str__(self):
        if self.__content is None:
            return str(self.__name)
        else:
            return '<' + str(self.__name) + ' = ' + str(self.__content) + '>'

    def __repr__(self):
        if self.__content is None:
            return str(self.__name)
        else:
            return '<' + str(self.__name) + ' = ' + str(self.__content) + '>'

    def __eq__(self, other):
        return self.__name == other.__name

    def __neq__(self, other):
        return self.__name != other.__name

    def __hash__(self):
        return hash(str(self.__name))


class GlobalVariableType(VariableType):
    """
    Class for the representation of a global variable.
    """
    def __init__(self, name, value=None):
        VariableType.__init__(self, name, value)


class SinglefieldVariableType(VariableType):
    """
    Class for the representation of a single variable.
    """
    def __init__(self, name, value=None):
        VariableType.__init__(self, name, value)


class AssignedPatternVariableType(VariableType):
    """
    Class for the representation of the assignment
    of a pattern to a variable.
    """

    def __init__(self, name, value=None):
        VariableType.__init__(self, name, value)


class ConditionalElementType(BaseType):
    """
    Class for the representation of a generic conditional element.
    It defines logical operators and, or and not between facts
    as conditional elements.
    """
    def __init__(self, name, patterns):
        self.__name = name
        self.__patterns = patterns

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def patterns(self):
        return self.__patterns

    @patterns.setter
    def patterns(self, values):
        self.__patterns = values

    def __str__(self):
        return 'ConditionalElement: (' + self.__name + ' ' + ' '.join([str(x) for x in self.__patterns]) + ')'

    def __repr__(self):
        return 'ConditionalElement: (' + self.__name + ' ' + ' '.join([str(x) for x in self.__patterns]) + ')'
