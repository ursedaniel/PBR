#!/usr/bin/env python

from core.rete.Strategy import *

from collections import defaultdict


class AgendaItem(object):
    """
    Class for the representation of an element of the agenda.
    """
    def __init__(self, PNode, token, variables, assigned_patterns):
        # Name of the rule.
        self.__name = PNode.name

        # Salience of the rule.
        self.__salience = PNode.salience

        # Right part (actions) of the rule.
        self.__actions = PNode.actions

        # Complexity of the rule.
        self.__complexity = PNode.complexity

        # Token which activates the rule.
        self.__token = token

        # Variables contained in the rule.
        self.__variables = variables

        # Variables of type Assigned Pattern CEs of the rule.
        self.__assigned_patterns = assigned_patterns

    @property
    def name(self):
        return self.__name

    @property
    def salience(self):
        return self.__salience

    @property
    def actions(self):
        return self.__actions

    @property
    def complexity(self):
        return self.__complexity

    @property
    def token(self):
        return self.__token

    @property
    def variables(self):
        return self.__variables

    @property
    def assigned_patterns(self):
        return self.__assigned_patterns

    def __str__(self):
        line = str(self.__salience) + '\t' + str(self.__name) + ': '

        for identifier in self.__token.wme_indexes:
            line += 'f-' + str(identifier) + ' '

        return line

    def __repr__(self):
        return str(self)


class Agenda(object):
    """
    Class for the representation of an agenda.
    """
    def __init__(self, network, strategy):
        # Reference to the network.
        self.__network = network

        # Dictionary which maps a token to the number of relative activations.
        # The default value is 0.
        self.__token_activations = defaultdict(lambda: 0)

        # Dictionary which maps a list of activations to each salience.
        # It partitions the activations according to their salience.
        self.__salience_activations = {}

        # Current conflict resolution strategy.
        self.__strategy = strategy

        # Available conflict resolution strategies.
        self.__strategies = {
            'depth': DepthStrategy,
            'breadth': BreadthStrategy,
            'random': RandomStrategy,
            'complexity': ComplexityStrategy,
            'simplicity': SimplicityStrategy,
            'lex': NaiveLexStrategy,
            'mea': NaiveMeaStrategy
        }

    @property
    def strategy(self):
        return self.__strategy

    @property
    def strategies(self):
        return self.__strategies

    def change_strategy(self, strategy):
        if isinstance(strategy, Strategy):
            # If the specified strategy is equal to the current one,
            # then it doesn't make any variation.
            # In that case it returns the False value.
            if self.__strategy is strategy:
                return False

            # Otherwise it sorts the agenda according to the specified strategy.
            # In that case it returns the True value.
            else:
                # Sets the specified strategy.
                self.__strategy = strategy

                # Sorts each list of activations by salience according to the specified strategy.
                for salience in self.__salience_activations:
                    self.__salience_activations[salience] = self.__strategy.sort(self.__strategy.iterable(self.__salience_activations[salience]))

                return True

        # If the specified strategy is not valid, then it returns the False value.
        return False

    def add_activation(self, item):
        # If the salience of the specified activation is not contained in the dictionary, then
        # it builds the appropriate container to contain the activations using the specified strategy.
        if item.salience not in self.__salience_activations:
            self.__salience_activations[item.salience] = self.__strategy.build_container()

        # Inserts the specified activation in the container of the considered salience.
        self.__strategy.insert(item, self.__salience_activations[item.salience])

        # Increases the number of activations for the token of the specified activation.
        self.__token_activations[item.token] += 1

    def del_activation(self, token):
        # If the specified token is not contained in the dictionary,
        # then it removes the activations with that token.
        if token in self.__token_activations:
            del self.__token_activations[token]

    def get_next_activation(self):
        # Saves a reference to the list of saliences sorted by decreasing order.
        sorted_saliences = sorted(self.__salience_activations.keys(), reverse=True)

        # For each salience, beginning from the highest one,
        # it identifies and returns the next activations.
        for salience in sorted_saliences:
            # Saves a reference to the activations with the current salience.
            items = self.__salience_activations[salience]

            # Extracts (and discards) each activation until it doesn't find a valid one.
            while items:
                item = self.__strategy.pop(items)

                if self.__token_activations[item.token] > 0:
                    self.__token_activations[item.token] -= 1
                    return item

        # If there aren't any available activations, then it returns the None value.
        return None

    def get_activations(self):
        # Inizializza la lista delle attivazioni valide.
        valid_activations = []

        # Saves a reference to the list of saliences sorted by decreasing order.
        sorted_saliences = sorted(self.__salience_activations.keys(), reverse=True)

        # For each salience, beginning from the highest one,
        # it identifies and adds to the list the next activation.
        for salience in sorted_saliences:
            # Builds an empty container which will contain the valid activations.
            valid_salience_activations = self.__strategy.build_container()

            # For each activation with the current salience,
            # if the token of the activation is still active,
            # then it adds the current activation to the list.
            for item in self.__salience_activations[salience]:
                if self.__token_activations[item.token]:
                    self.__strategy.insert(item, valid_salience_activations)

            # It replaces each container by salience with the updated container by salience,
            # i.e. with the the container by salience containing only the valid activations.
            self.__salience_activations[salience] = valid_salience_activations

            # Sorts the container of the activations in the logic order to be printed.
            sorted_valid_salience_activations = self.__strategy.sorted_iterator(valid_salience_activations)

            # Adds the identified activations to the list.
            valid_activations.extend(sorted_valid_salience_activations)

        # Returns the list of the valid identified activations.
        return valid_activations

    def __str__(self):
        activations = self.get_activations()

        if not activations:
            return 'Empty agenda.'
        else:
            return '\n'.join(map(str, activations)) + '\n' + \
                'for a total of ' + str(len(activations)) + ' activations.'

    def __repr__(self):
        return str(self)
