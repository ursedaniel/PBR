#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

from core.typesystem.TypeSystem import *

from core.rete.Agenda import AgendaItem

from core.rete.Token import Token

from collections import OrderedDict


class Node(object):
    """
    Class for the representation of a generic node of the network.
    """
    def __init__(self, network):
        # Reference to the network.
        self.__network = network

        # Reference to the Evaluator.
        self.__evaluator = self.__network.evaluator

        # Reference to the Environment.
        self.__environment = self.__evaluator.environment

    @property
    def network(self):
        return self.__network

    @property
    def evaluator(self):
        return self.__evaluator

    @property
    def environment(self):
        return self.__environment


class RootNode(Node):
    """
    Class for the representation of the root node of the network.
    """
    def __init__(self, network):
        Node.__init__(self, network)

        # Dictionary of the children of the node.
        self.__children = {}

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value):
        self.__children = value

    def add_child(self, child):
        if child.label not in self.__children:
            self.__children[child.label] = child
            return True
        else:
            return False

    def del_child(self, child):
        if child.label in self.__children:
            del self.__children[child.label]
            return True
        else:
            return False

    def build_node(self, pattern):
        if len(pattern) > 0:
            # Saves the first elemento f the pattern, which corresponds to the name of the fact.
            # (A pattern is of the form [name of the fact, [attributes of the fact]]).
            head = pattern[0]

            # If the considered element is one of the children of the node, then it builds
            # the network beginning from the identified children, specifying as parameters
            # the list of the attributes of the fact and the instance of the class which will contain
            # the references to the identified variables. In the end, it returns backwards
            # the reference to the alpha memory which will be built at the end of the algorithm.
            if head in self.__children:
                return self.__children[head].build_node(pattern[1], {})

            else:
                # Otherwise it builds a new alpha node specifying as parameters the name
                # of the identified fact and the depth level of the node, which will be used
                # mainly for the identification of a mapping between the position of the elements
                # of the pattern and the position of the attributes of the facts.
                # (It assumes that the depth level begins from 0 for the children of the root node).
                # Then it adds the built node and calls the building beginning from the considered
                # node. In the end, it returns backwards a reference to the alpha memory
                # which will be built at the end of the algorithm.
                node = AlphaNode(self.network, self, head, 0)
                self.add_child(node)
                return node.build_node(pattern[1], {})

    def match_node(self, wme):
        # Saves the fact contained in the WME.
        fact = wme.fact

        # Saves the name of the fact.
        name = fact.name

        # If the name is contained among the children of the node,
        # it calls the matching beginning from the considered node.
        if name in self.__children:
            self.__children[name].match_node(wme)

    def __str__(self):
        return str(self.__children)

    def __repr__(self):
        return str(self)


class AlphaNode(Node):
    """
    Class for the representation of an alpha node of the network.
    """
    def __init__(self, network, parent, label, depth):
        Node.__init__(self, network)

        # Parent of the node.
        self.__parent = parent

        # Content of the node.
        self.__label = label

        # Dictionary of the children of the node.
        self.__children = {}

        # Possible alpha memory mapped to the node.
        self.__alpha_memory_node = None

        # Depth level of the node. The level builds a mapping
        # between the position of the elements of the pattern
        # and the position of the attributes of the facts.
        self.__depth = depth

        # Sets of the references to the variables contained among the children of the node.
        # The set is used to avoid the iterations on the nodes which rapresent
        # constants during the matching of the possible variables.
        self.__var_nodes = set()

        # If the considered node is a variable, then it saves
        # a reference to the last variable, if it's present,
        # with analogous name, to control possible duplicates.
        self.__to_check = None

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        self.__label = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value):
        self.__children = value

    @property
    def alpha_memory_node(self):
        return self.__alpha_memory_node

    @alpha_memory_node.setter
    def alpha_memory_node(self, value):
        self.__alpha_memory_node = value

    @property
    def to_check(self):
        return self.__to_check

    @to_check.setter
    def to_check(self, value):
        self.__to_check = value

    def add_child(self, child):
        if child.label not in self.__children:
            self.__children[child.label] = child
            return True
        else:
            return False

    def del_child(self, child):
        if child.label in self.__children:
            del self.__children[child.label]
            return True
        else:
            return False

    def build_node(self, pattern, var_refs):
        # If the considered node represents a variable, then it saves a reference
        # to the position that the variable will take on. Moreover, if has already
        # been found a variable with the same name of the considered node, then
        # it saves a reference to the position which could be checked for duplicates
        # during the matching phase, to remove a priori not equal attributes which
        # don't correspond to the same variable.
        if isinstance(self.__label, VariableType):
            # Adds the variable in the set of the nodes of the parent.
            self.__parent.__var_nodes.add(self.__label)

            # If the variable has already been found during the building, then it saves
            # a reference to the position of that variable in the pattern, to possibly
            # check a duplicate during the matching phase.
            if self.__label in var_refs:
                var_positions = var_refs[self.__label]
                self.to_check = var_positions[len(var_positions) - 1]

            # Memorizza la variabile nel dizionario.
            if self.__label not in var_refs:
                var_refs[self.__label] = [self.__depth - 1]
            else:
                var_refs[self.__label].append(self.__depth - 1)

        # Checks if it has been reached the last element of the pattern. The depth level
        # of the node corresponds to the position of the element of the pattern to check.
        if self.__depth < len(pattern):
            # Memorizza l'attributo corrente del pattern
            head = pattern[self.__depth]

            # If the considered attribute is one of the children of the node, then it builds a network
            # beginning from the identified child. In the end, it returns backwards a reference
            # to the alpha memory which will be built at the end of the algorithm.
            if head in self.__children:
                return self.__children[head].build_node(pattern, var_refs)

            # Otherwise, it builds a new alpha node specifying the name of the node
            # and the depth level of the node as parameters. Then it adds the built node
            # and it calls the building beginning from the considered node. In the end,
            # it returns backwards the reference to the alpha memory which will be
            # built at the end of the algorithm.
            else:
                node = AlphaNode(self.network, self, head, self.__depth + 1)
                self.add_child(node)
                return node.build_node(pattern, var_refs)

        # Otherwise it means which has been reached the last element of the pattern.
        # For that reason, it has been built an alpha memory node in which it has been saved
        # the instance of the class containing the references of possible variables found
        # during the building of the network. In the end, it returns backwards a reference
        # to the alpha memory which will be built at the end of the algorithm.
        else:
            if self.__alpha_memory_node is None:
                self.__alpha_memory_node = AlphaMemoryNode(self.network, self)

            self.__alpha_memory_node.variables = var_refs

            return self.__alpha_memory_node.build_node()

    def match_node(self, wme):
        # If the variable for the check of possible duplicate variables
        # has been set, then it compares the value of the current node
        # with the value of the reference to the variable to check.
        if self.__to_check is not None:
            # Memorizza il valore del nodo corrente
            head = wme.fact.values[self.__depth - 1]

            # If the value taken by the current node and the value taken by
            # the variable to check are different, then it means that
            # there is a fact with multiple variables with the
            # same name but with different values. For this
            # reason, it rejects the considered fact.
            if wme.fact.values[self.__to_check] != head:
                return

        # It checks if it has been reached the last element of the pattern. The depth level
        # of the node corresponds to the position of the element of the pattern to check.
        if self.__depth < len(wme.fact.values):
            # Saves the considered attribute.
            head = wme.fact.values[self.__depth]

            # If the attribute corresponds to one of the children of the node,
            # then it calls the matching beginning from the identified child.
            if head in self.__children:
                self.__children[head].match_node(wme)

            # It calls the matching on possible children
            # which correspond to one of the variables.
            for child in self.__var_nodes:
                self.__children[child].match_node(wme)

        # Otherwise, if the end of the alpha network has been reached,
        # then it adds the WME to the relative alpha memory and it
        # activates this node to go ahead with the beta network.
        else:
            if self.__alpha_memory_node is not None:
                self.__alpha_memory_node.add_wme(wme)
                self.__alpha_memory_node.activate_beta(wme)

    def __str__(self):
        if self.__alpha_memory_node is None:
            return str((self.__children, self.__to_check))
        else:
            return str((self.__children, self.__alpha_memory_node, self.__to_check))

    def __repr__(self):
        return str(self)


class AlphaMemoryNode(Node):
    """
    Class for the representation of an alpha memory of the network.
    """
    def __init__(self, network, parent):
        Node.__init__(self, network)

        # Parent of the node.
        self.__parent = parent

        # List of the children of the node.
        self.__children = []

        # List of the WME contained in the node.
        self.__wmes = OrderedDict()

        # Reference to the identified variables.
        self.__variables = None

        # Mapping between the WME and the identified variables.
        self.__wme_variables = {}

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value):
        self.__children = value

    @property
    def wmes(self):
        return self.__wmes

    @wmes.setter
    def wmes(self, values):
        self.__alpha_elements = values

    @property
    def variables(self):
        return self.__variables

    @variables.setter
    def variables(self, values):
        self.__variables = values

    @property
    def wme_variables(self):
        return self.__wme_variables

    def add_wme(self, wme):
        self.__wmes[wme.identifier] = wme

    def del_wme(self, wme):
        del self.__wmes[wme.identifier]
        del self.__wme_variables[wme.identifier]

    def add_child(self, child):
        self.__children.append(child)

    def del_child(self, child):
        self.__children.remove(child)

    def build_node(self):
        return self

    def activate_beta(self, wme):
        self.network.add_wme_alpha_memory(wme.identifier, self)

        if wme.identifier not in self.__wme_variables:
            self.__wme_variables[wme.identifier] = {}

        # Saves all the variables of the alpha memory mapping all the instances for every WME.
        for v in self.__variables:
            self.__wme_variables[wme.identifier][v] = wme.fact.get_attribute(self.__variables[v][0])

        for child in self.__children:
            if type(child) is not PNode:
                child.right_activation(wme)

            else:
                # There is a direct link to the pnode.
                # It means that the relative rule presents only a condition.
                child.match_node(Token(None, wme), self.__wme_variables[wme.identifier], {})

    def __str__(self):
        line = ' '

        if self.__wmes:
            for wme in self.__wmes.values():
                line += str(wme) + '\n'

            if self.__wmes:
                line += str(self.__variables)
        else:
            line += 'Empty Alpha Memory'

        return line

    def __repr__(self):
        return str(self)


class TestsNode(Node):
    """
    Class for the representation of a node to build and contain the tests.
    """
    def __init__(self, network):
        Node.__init__(self, network)

        # Set of the tests to execute.
        self.__tests = set()

    @property
    def tests(self):
        return self.__tests

    @tests.setter
    def tests(self, values):
        self.__tests = values

    def build_tests(self, is_last, alpha_variables, tests):
        var_globals = [GlobalVariableType(x) for x in self.environment.global_variables.keys()]

        # For every variable in the set composed by the union
        # of the variables of the specified alpha memory
        # and the global variables, then it saves
        # the tests which involve these variables
        # to the specified tests set.
        for v in set(alpha_variables.keys() + var_globals):
            if v in tests:
                self.__tests.update(tests[v])
                del tests[v]

        # It removes the set of the identified local test
        # from the set of the tests specified as parameter.
        for t in self.__tests:
            for v in t.test_variables:
                if v in tests:
                    tests[v].remove(t)

        # If the flag which specifies if the considered node
        # is the last one which contains the test is set to True,
        # then, if there are still tests in the set, then it
        # raises an exception, because it means that the
        # test contains variables not declared in the alpha memory.
        if is_last:
            # Rimuove tutti gli insiemi di test vuoti rimanenti.
            # It removes all the remaining empty sets of tests.
            for k in tests.keys():
                if not tests[k]:
                    del tests[k]

            if tests:
                raise EvaluateException('There are tests with invalid variables!')


class JoinNode(TestsNode):
    """
    Class for the representation of a Join Node.
    """
    def __init__(self, network, beta_memory=None, alpha_memory=None):
        TestsNode.__init__(self, network)

        # Reference to the node which represents the left input.
        # This node should be a beta memory.
        self.__parent = beta_memory

        # Reference to the node which represents the right input.
        # This node should be an alpha memory.
        self.__alpha_memory = alpha_memory

        # List of the children of the node to which the tokens are propagated.
        self.__children = []

        # Variable of the possible Assigned Pattern CE.
        self.__assigned_pattern_variable = None

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def alpha_memory(self):
        return self.__alpha_memory

    @alpha_memory.setter
    def alpha_memory(self, value):
        self.__alpha_memory = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value):
        self.__children = value

    @property
    def assigned_pattern_variable(self):
        return self.__assigned_pattern_variable

    @assigned_pattern_variable.setter
    def assigned_pattern_variable(self, value):
        self.__assigned_pattern_variable = value

    def add_child(self, child):
        self.__children.append(child)

    def del_child(self, child):
        self.__children.remove(child)

    def build_node(self, lhs, position, alpha_memory_patterns, tests):
        # If the considered pattern is of type Assigned Pattern CE,
        # then it's decomposed saving the variable which will reference
        # an instance of the pattern in the node. In that way every
        # WME which will pass through the current join will be
        # mapped to the saved variable.
        if isinstance(lhs[position][0], AssignedPatternVariableType):
            self.__assigned_pattern_variable = lhs[position][0].name
            lhs[position] = lhs[position][0].content

        # Saves a reference to the alpha memory relative to the current pattern
        # to join it to the alpha network.
        self.__alpha_memory = alpha_memory_patterns[str(lhs[position])]

        # It builds the tests for the current node.
        self.build_tests(False, self.__alpha_memory.variables, tests)

        # Adds the current node as a child of the alpha memory.
        self.__alpha_memory.add_child(self)

        # Builds a beta memory node.
        beta_memory = BetaMemoryNode(self.network)

        # Sets the beta memory node which has been just created as a parent of the current join node.
        self.__parent = beta_memory

        # Adds the current node as a child of the beta memory.
        beta_memory.add_child(self)

        # Propagates the building of the beta network to the upper level.
        beta_memory.build_node(lhs, position - 1, alpha_memory_patterns, tests)

    def left_activation(self, token, pattern_assignments):
        # Pseudo-algorithm:
        # 1. Finds the variables (labels) in common between the beta and the alpha memories.
        # 2. If there are WMEs in the alpha memory, then for every WME it compares the instances of
        #    the variables in common to the instances in the input token.
        # 3. If the matching reached a satisfactory conclusion, then:
        #    3a. Builds a new token: token + current WME.
        #    3b. Joins the dictionaries in a new dictionary.
        #    3c. Executes the tests; if all the tests had a positive outcome, then:
        #        3c.1 Propagates the token and the new dictionary to the children (beta memories).
        # 4. Goes back to step 2.

        # TOKENS VS WMES.

        if self.__alpha_memory.wmes:
            # Variables coming from the beta memories relative to the token.
            # beta_variables is in the form variable_label_current_token : instance.
            beta_variables = self.__parent.token_variables[token]

            # For every WME it checks the matching and eventually it composes
            # token and dictionary and propagates to the sons.
            for wme in self.__alpha_memory.wmes.values():
                passed = True

                # Dictionary which will contain the instanced variables
                # of the alpha memory according to the considered WME.
                # alpha_variables is variable_label_current_wme : instance.
                alpha_variables = self.__alpha_memory.wme_variables[wme.identifier]

                # It compares the alpha variables in common with the betas.
                # It fails if:
                #   1. The instanced are equal but don't concern to the same token
                #      (It filters the instances of the variables in the beta memory
                #      selecting only the ones which contain the token).
                #   2. The instances are different.

                alpha = alpha_variables
                beta = beta_variables

                if len(alpha) > len(beta):
                    alpha, beta = beta, alpha

                for v in alpha:
                # If v is present in the beta dictionary, too.
                    if v in beta:
                        # If the value of v in alpha is the same in beta, then it proceeds.
                        # Otherwise, stop the search because the matching failed.
                        if alpha[v] != beta[v]:
                            passed = False
                            break

                # If the token has passed the matching.
                if passed:

                    # Union of the dictionaries of the variables.
                    # The double asterisk is needed to use dict constructor.
                    # In this case, the form is dict(mapping, **kwargs)
                    # which can be rewritten as dict(mapping, key1=value1, key2=value2, ...).
                    # If the two dictionaries have keys in common, then the conflict
                    # is solved in favor of the alpha variables.

                    new_variables = dict(beta_variables, **alpha_variables)

                    test_passed = True

                    # Executes every test of the current join node.
                    for test in self.tests:
                        if not self.evaluator.evaluate(test, True, new_variables):
                            test_passed = False
                            break

                    # If all the tests stopped with a positive outcome, then it builds
                    # the new token and it propagates it to the children of the current join node.
                    if test_passed:
                        if self.__assigned_pattern_variable is not None:
                            pattern_assignments[self.__assigned_pattern_variable] = wme.identifier

                        new_token = Token(token, wme)

                        # Propagates the new token and the relative variables to every child of the current node.
                        for child in self.__children:
                            child.match_node(new_token, new_variables, pattern_assignments)

    def right_activation(self, wme):
        # Pseudo-algorithm:
        # 1. Identifies the variables (labels) in common between the beta memory and the alpha memory.
        # 2. If there are tokens in the beta memory, then for every token it compares the instances
        #    of the variables in common to the instances of the input WME.
        # 3. If the matching ended well then:
        #    3a. Builds a new token: token + WME.
        #    3b. Joins the dictionaries in a new dictionary.
        #    3c. Executes the tests; if all ended with a positive outcome, then:
        #        3c.1 Propagates the token and the new dictionary to the children (beta memories).
        # 4. Goes back to step 2.

        # Se e' presente una beta memory padre non vuota.
        if self.__parent.tokens:

            # WME VS TOKENS.

            tokens = self.__parent.tokens

            # Dictionary which will contain the instanced variables
            # of the alpha memory according to the considered WME.
            # alpha_variables is variable_label_current_wme : instance.
            alpha_variables = self.alpha_memory.wme_variables[wme.identifier]

            # For every token t, it retrieve the dictionary of the relative instanced variables and
            # it checks the variables with the same label. If the unification of the variables goes well,
            # then it joins the dictionary of the variables of the token with the dictionary of the variables
            # of the WME and it builds a new dictionary; it builds a new token given by (t + WME) and
            # it propagates it with the new dictionary.
            for t in tokens:
                # Variables coming from the beta memories relative to the token.
                # beta_variables is in the form variable_label_current_token : instance.
                beta_variables = self.__parent.token_variables[t]

                passed = True

                alpha = alpha_variables
                beta = beta_variables

                if len(alpha) > len(beta):
                    alpha, beta = beta, alpha

                for v in alpha:
                # If v is contained in the beta dictionary, too.
                    if v in beta:
                        # If the value of v in alpha is the same in beta, then proceeds.
                        # Otherwise, stops the search because the matching failed.
                        if alpha[v] != beta[v]:
                            passed = False
                            break

                if passed:

                    # Union of the dictionaries of the variables.
                    # The double asterisk is needed to use dict constructor.
                    # In this case, the form is dict(mapping, **kwargs)
                    # which can be rewritten as dict(mapping, key1=value1, key2=value2, ...).
                    # If the two dictionaries have keys in common, then the conflict
                    # is solved in favor of the alpha variables.

                    new_variables = dict(beta_variables, **alpha_variables)

                    test_passed = True

                    # Executes every test in the current join node.
                    for test in self.tests:
                        if not self.evaluator.evaluate(test, True, new_variables):
                            test_passed = False
                            break

                    # If all the tests stopped with a positive outcome, then it builds
                    # a new token and it propagates it to the children of the current join node.
                    if test_passed:
                        if self.__assigned_pattern_variable is not None:
                            self.__parent.assigned_pattern_ces[t][self.__assigned_pattern_variable] = wme.identifier

                        new_token = Token(t, wme)

                        for child in self.__children:
                            child.match_node(new_token, new_variables, self.__parent.assigned_pattern_ces[t])

    def __str__(self):
        line = 'JOIN\n'

        if self.tests:
            line += 'Number of tests: ' + str(len(self.tests))
        else:
            line += 'No tests'

        if self.__assigned_pattern_variable:
            line += '\nPattern assignment: ' + str(self.__assigned_pattern_variable)

        return line

    def __repr__(self):
        return str(self)


class DummyJoinNode(JoinNode):
    """
    Class for the representation of a Dummy Join Node.
    """
    def __init__(self, network, alpha_memory=None):
        JoinNode.__init__(self, network, None, alpha_memory)

    def build_node(self, lhs, position, alpha_memory_patterns, tests):
        # If the considered pattern is of type Assigned Pattern CE,
        # then it decomposes it saving in the node the variable
        # which will reference an instance of the pattern.
        # In that way every WME which will pass through
        # the current join node will be mapped to the
        # referenced variable.
        if isinstance(lhs[position][0], AssignedPatternVariableType):
            self.assigned_pattern_variable = lhs[position][0].name
            lhs[position] = lhs[position][0].content

        # Saves a reference to the alpha memory relative 
        # to the current pattern to connect to the Alpha Network.
        self.alpha_memory = alpha_memory_patterns[str(lhs[position])]

        # Builds the tests of the current node.
        self.build_tests(True, self.alpha_memory.variables, tests)

        # Adds the current node as a child of the alpha memory.
        self.alpha_memory.add_child(self)

    def right_activation(self, wme):
        # Initializes the dictionary of the Assigned Pattern CEs.
        pattern_assignments = {}

        # Maps the WME which will pass through the current dummy join node
        # to the possible variable of type Assigned Pattern CE.
        if self.assigned_pattern_variable is not None:
            pattern_assignments[self.assigned_pattern_variable] = wme.identifier

        alpha_variables = self.alpha_memory.wme_variables[wme.identifier]

        # Executes every test of the current join node.
        for test in self.tests:
            if not self.evaluator.evaluate(test, True, alpha_variables):
                return

        # If all the tests stopped with a positive outcome, then
        # it  builds the new token and it propagates it to the beta memories.
        token = Token(None, wme)

        for child in self.children:
            child.match_node(token, alpha_variables, pattern_assignments)

    def __str__(self):
        line = 'D. JOIN\n'

        if self.tests:
            line += 'Number of tests: ' + str(len(self.tests))
        else:
            line += 'No tests'

        if self.assigned_pattern_variable:
            line += '\nPattern assignment: ' + str(self.assigned_pattern_variable)

        return line

    def __repr__(self):
        return str(self)


class BetaMemoryNode(Node):
    """
    Class for the representation of a Beta Memory Node.
    """
    def __init__(self, network, parent=None):
        Node.__init__(self, network)

        # Reference to the parent Join or Dummy Join node.
        self.__parent = parent

        # List of the children of the node.
        self.__children = []

        # Dictionary of locally saved tokens.
        self.__tokens = OrderedDict()

        # Dictionary which contains the references to the variables
        # beginning from a token, populated in matching phase, too.
        self.__token_variables = {}

        # Reference to the dictionary which contains the Assigned Pattern CEs.
        self.__assigned_pattern_ces = {}

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value):
        self.__children = value

    @property
    def tokens(self):
        return self.__tokens

    @tokens.setter
    def tokens(self, values):
        self.__tokens = values

    @property
    def variables(self):
        return self.__variables

    @property
    def token_variables(self):
        return self.__token_variables

    @property
    def assigned_pattern_ces(self):
        return self.__assigned_pattern_ces

    def add_token(self, token):
        self.__tokens[token] = token

    def del_token(self, token):
        del self.__tokens[token]
        del self.__token_variables[token]
        del self.__assigned_pattern_ces[token]

    def add_child(self, child):
        self.__children.append(child)

    def del_child(self, child):
        self.__children.remove(child)

    def build_node(self, lhs, position, alpha_memory_patterns, tests):
        # If the last position of the pattern of the left part of the rule
        # has not been reached yet, then it builds a join node
        # which becomes the parent of the current beta memory node.
        if position > 0:
            # Builds a join node.
            join_node = JoinNode(self.network)

            # Sets the join node as parent of the current node.
            self.parent = join_node

            # Sets the current node as a child of the join node.
            join_node.add_child(self)

            # Delegates the join node to the building of the remaining network.
            join_node.build_node(lhs, position, alpha_memory_patterns, tests)

        # Otherwise it builds a dummy join node which
        # becomes the father of the current beta memory node.
        else:
            # Builds a dummy join node.
            dummy_join_node = DummyJoinNode(self.network)

            # Sets the dummy join node as a parent of the current node.
            self.parent = dummy_join_node

            # Sets the current node as a child of the dummy join node.
            dummy_join_node.add_child(self)

            # Delegates the dummy join node to the building of the remaining network.
            dummy_join_node.build_node(lhs, position, alpha_memory_patterns, tests)

    def match_node(self, token, variables, pattern_assignments):
        # Maps the current token to the considered beta memory node.
        self.network.set_token_beta_memory(token, self)

        self.__assigned_pattern_ces[token] = pattern_assignments

        # Saves the input token in the beta memory node.
        self.add_token(token)

        for identifier in token.wme_indexes:
            self.network.add_wme_token(identifier, token)

        # Builds a dictionary of variables relative to the token
        # which will be in the form token: variable_label: instance.
        self.__token_variables[token] = variables

        # Propagates the token to the children of the current beta memory node.
        # (the children can be join or dummy join nodes).
        for child in self.children:
            child.left_activation(token, pattern_assignments)

    def __str__(self):
        line = ' '
        t = None
        if self.__tokens:
            for token in self.__tokens:
                line += str(token) + '\n'
                t = token

            if self.__token_variables[t]:
                line += str(self.__token_variables[t].keys())
        else:
            line += 'Empty Beta Memory'

        return line

    def __repr__(self):
        return str(self)


class PNode(TestsNode):
    """
    Class for the representation of a PNode (Production Node).
    """
    def __init__(self, network, rule):
        TestsNode.__init__(self, network)

        # Parent of the node: it can be a join node or an alpha memory node.
        self.__parent = None

        # Right part of a rule.
        self.__actions = rule.rhs

        # Name of the rule represented by the PNode.
        self.__name = rule.name

        # Salience of the rule.
        self.__salience = rule.salience

        # Complexity of the rule.
        self.__complexity = rule.complexity

        # Variable of the possible Assigned Pattern CE.
        self.__assigned_pattern_variable = None

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def name(self):
        return self.__name

    @property
    def complexity(self):
        return self.__complexity

    @property
    def salience(self):
        return self.__salience

    @property
    def actions(self):
        return self.__actions

    @property
    def assigned_pattern_variable(self):
        return self.__assigned_pattern_variable

    def build_node(self, lhs, alpha_memory_patterns, tests):
        # If the left part of the rule contains more then a pattern,
        # then it builds a join node to which it delegates the building of the network.
        if len(lhs) > 1:
            # Builds a join node.
            join_node = JoinNode(self.network)

            # Sets the join node as a parent of the current node.
            self.parent = join_node

            # Sets the current node as a child of the join node.
            join_node.add_child(self)

            # Delegates the building of the network to the join node.
            join_node.build_node(lhs, len(lhs) - 1, alpha_memory_patterns, tests)

        # Altrimenti collega il nodo pnode corrente all'alpha memory corrispondente
        # all'unico pattern presente nella parte sinistra della regola.
        else:
            # Manages the case in which a pattern is associated to an Assigned Pattern CE.
            if isinstance(lhs[0][0], AssignedPatternVariableType):
                self.__assigned_pattern_variable = lhs[0][0].name
                lhs[0] = lhs[0][0].content

            # Identifies the alpha memory to be mapped to the node.
            alpha_memory = alpha_memory_patterns[str(lhs[0])]

            # Adds the current node as a child of the alpha memory.
            alpha_memory.add_child(self)

            # Builds the tests for the current node.
            self.build_tests(True, alpha_memory.variables, tests)

            # Adds the current node to the alpha memory with the same key of the lhs[0] pattern.
            self.__parent = alpha_memory_patterns[str(lhs[0])]

    def match_node(self, token, variables, pattern_assignments):
        # Executes every test of the current PNode node.
        for test in self.tests:
            if not self.evaluator.evaluate(test, True, variables):
                return

        # Maps the current token to the considered WME.
        for identifier in token.wme_indexes:
            self.network.add_wme_token(identifier, token)

        # Maps the WME which passes through the current PNode node
        # to the possible variable of type Assigned Pattern CE.
        if self.__assigned_pattern_variable is not None:
            pattern_assignments[self.__assigned_pattern_variable] = token.wme.identifier

        # Adds the activaion relative to the current PNode to the agenda.
        self.network.agenda.add_activation(AgendaItem(self, token, variables, pattern_assignments))

    def __str__(self):
        line = str(self.__name) + '\n'

        if self.tests:
            line += str(len(self.tests))
        else:
            line += 'No tests'

        if self.__assigned_pattern_variable:
            line += '\nPattern assignment: ' + str(self.__assigned_pattern_variable)

        return line

    def __repr__(self):
        return str(self)
