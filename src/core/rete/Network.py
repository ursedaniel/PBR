
#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""
import copy

from core.rete.Nodes import RootNode, PNode

from core.rete.Agenda import Agenda

from core.WorkingMemory import WorkingMemory

from core.ProductionMemory import ProductionMemory

from core.typesystem.TypeSystem import *

class Network(object):
    """
    Class for the representation of a RETE network.
    """
    def __init__(self, evaluator, strategy):
        # Saves a reference to the Evaluator.
        self.__evaluator = evaluator

        # Saves a reference to the Working Memory.
        self.__working_memory = None

        # Saves a reference to the Production Memory.
        self.__production_memory = None

        # Saves a reference to the Agenda.
        self.__agenda = Agenda(self, strategy)

        # Saves a reference to the root of the network.
        self.__root_node = None

        # Dictionary which maps a WME to the tokens which contain them.
        self.__wme_tokens = {}

        # Dictionary which maps a WME to the alpha memory in which it's contained.
        self.__wme_alpha_memories = {}

        # Dictionary which maps a token to the beta memory in which it's contained.
        self.__token_beta_memories = {}

        # Dictionary which maps a alpha memory to the relative patterns.
        self.__alpha_memory_patterns = {}

        # Number of executed activations.
        self.__fired_activations = 0

        # Reset of the network.
        self.reset_network()


    def add_wme_token(self, identifier, token):
        if identifier not in self.__wme_tokens:
            self.__wme_tokens[identifier] = set([token])
        else:
            self.__wme_tokens[identifier].add(token)

    def add_wme_alpha_memory(self, identifier, alpha_memory):
        if identifier not in self.__wme_alpha_memories:
            self.__wme_alpha_memories[identifier] = [alpha_memory]
        else:
            self.__wme_alpha_memories[identifier].append(alpha_memory)

    def set_token_beta_memory(self, identifier, beta_memory):
        self.__token_beta_memories[identifier] = beta_memory

    @property
    def root_node(self):
        return self.__root_node

    @property
    def evaluator(self):
        return self.__evaluator

    @evaluator.setter
    def evaluator(self, value):
        self.__evaluator = value

    @property
    def working_memory(self):
        return self.__working_memory

    @property
    def production_memory(self):
        return self.__production_memory

    @property
    def agenda(self):
        return self.__agenda

    @property
    def wme_tokens(self):
        return self.__wme_tokens

    @wme_tokens.setter
    def wme_tokens(self, values):
        return self.__wme_tokens

    @property
    def token_beta_memories(self):
        return self.__token_beta_memories

    @token_beta_memories.setter
    def token_beta_memories(self, values):
        self.__token_beta_memories = values

    @property
    def wme_alpha_memories(self):
        return self.__wme_alpha_memories

    @wme_alpha_memories.setter
    def wme_alpha_memories(self, values):
        self.__wme_alpha_memories = values

    @property
    def fired_activations(self):
        return self.__fired_activations

    def reset_network(self):
        # Initialies the Working Memory.
        self.__working_memory = WorkingMemory()

        # Initialies the Production Memory.
        self.__production_memory = ProductionMemory()

        # Initialies the root of the network.
        self.__root_node = RootNode(self)

        # Initialies the number of executed activations.
        self.__fired_activations = 0

        # Resets the current conflict resolution strategy.
        current_strategy = self.__agenda.strategy.__class__()

        # Initializes the agenda with the current strategy.
        self.__agenda = Agenda(self, current_strategy)

        # Initializes the dictionaries of the memories of the network.

        self.__wme_tokens = {}
        self.__wme_alpha_memories = {}
        self.__token_beta_memories = {}
        self.__alpha_memory_patterns = {}

    def build_network(self, facts, rules):
        # Resets the network.
        self.reset_network()

        graphs = []

        # Executes the building of the network.

        rules = reversed(list(rules))

        for rule in rules:
            self.add_rule(rule)
            deep_copy_self = copy.deepcopy(self)
            graphs.append(deep_copy_self)

        # Executes the initial matching ot the network.

        for fact in facts:
            self.assert_fact(fact)
            deep_copy_self = copy.deepcopy(self)
            graphs.append(deep_copy_self)

        return graphs

    def recognize_act_iteration(self, next_activation):
        # If the specified activation is valid, then it executes that activation.
        if next_activation is not None:

            total_variables = dict(next_activation.variables, **next_activation.assigned_patterns)

            # Executes each action of the specified activation.
            for action in next_activation.actions:
                # Sets the network as a caller for the current activation.
                action.caller = self

                # Executes the current action.
                self.__evaluator.evaluate(action, variables=total_variables)

            # Increases the number of the executed activations.
            self.__fired_activations += 1

    def recognize_act_cycle(self, iterations=None):
        next_activation = True
        self.__fired_activations = 0

        # Executes the activation until there is an available activation.
        while next_activation is not None:
            # Asks the agenda for the next activation.
            next_activation = self.__agenda.get_next_activation()

            # Executes an iteration of the Recognize-Act-Cycle.
            self.recognize_act_iteration(next_activation)

            # If it has been specified a limit in the number of iterations to be executed,
            # then it decrements the counter and it stops, if necessary, the cycle.
            # The value iterations=None notifies a potentially infinite cycle.
            if iterations is not None:
                iterations -= 1
                if iterations <= 0:
                    break

    def assert_fact(self, fact):
        # Adds the fact to the Working Memory
        # and identifies the corresponding WME.
        wme = self.__working_memory.add_fact(fact)

        # If the WME is not None, i.e. if the fact
        # is not already contained in the Working Memory,
        # then if executes the matching of the WME and
        # it returns the identifier of that WME.
        if wme is not None:
            self.__root_node.match_node(wme)
            return wme.identifier

        # Otherwise it returns the None value.
        else:
            return None

    def retract_fact(self, identifier):
        # If the WME exists in the Working Memory,
        # then it removes that WME and its mapped memories.
        if identifier in self.__working_memory.wmes:
            # If the WME partecipates to one or more tokens,
            # then it removes the tokens from these beta memories.
            if identifier in self.__wme_tokens:
                tokens = self.__wme_tokens[identifier]

                for token in tokens:
                    # Disables the activations for the current token.
                    self.__agenda.del_activation(token)

                    if token in self.__token_beta_memories:
                        beta_memory = self.__token_beta_memories[token]
                        beta_memory.del_token(token)
                        del self.__token_beta_memories[token]

                del self.__wme_tokens[identifier]

            # If the WME is not contained in one or more alpha memories,
            # then it removes the WMEs from these alpha memories.
            if identifier in self.__wme_alpha_memories:
                alpha_memories = self.__wme_alpha_memories[identifier]

                wme = self.__working_memory.wmes[identifier]

                for alpha_memory in alpha_memories:
                    alpha_memory.del_wme(wme)

                del self.__wme_alpha_memories[identifier]

            # Removes the WME from the Working Memory.
            self.__working_memory.remove_fact(identifier)

            # Returns the True value.
            return True

        # Otherwise, if it has not been done a removal,
        # then if returns the False value.
        else:
            return False

    def add_rule(self, rule):
        # Adds the rule to the Production Memory.
        self.__production_memory.add_rule(rule)

        # For each pattern of the left part of the rule, it executes the building of the alpha network
        # and it indexes the alpha memory built according to the considered pattern. In addition, if the pattern
        # is encapsulated in a variable of the type Assigned Pattern CE, then it extracts the considered pattern.
        for pattern in rule.lhs:
            if isinstance(pattern[0], AssignedPatternVariableType):
                pattern = pattern[0].content

            # Builds the alpha network for the considered rule,
            # returning a reference to the identified alpha memory.
            self.__alpha_memory_patterns[str(pattern)] = self.__root_node.build_node(pattern)

        # Builds the PNode which contains the rule.
        pnode = PNode(self, rule)

        # Builds backwards the beta network for the current rule,
        # connecting each pattern to the relative alpha memory.
        pnode.build_node(rule.lhs, self.__alpha_memory_patterns, rule.variable_tests)

    def remove_rule(self, rule):
        # Removal of a rule has not been implemented.
        pass

    def __str__(self):
        return str(self.__root_node)

    def __repr__(self):
        return str(self)
