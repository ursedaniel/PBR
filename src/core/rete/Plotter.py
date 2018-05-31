#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""


from core.rete.Nodes import *
from core.parser.Parser import Parser
from core.rete.Network import Network
from core.Builder import Builder
from core.rete.Network import Network
from core.rete.Strategy import *

from utilities.Timer import Timer

try:
    import networkx as nx
except Exception:
    print '\nWarning! Networkx should be installed.\n'

try:
    import pydot
except Exception:
    print '\nWarning! Pydot should be installed.\n'

import copy
import time

class Plotter(object):
    """
    Class for the plotting of the RETE network.
    """
    def __init__(self):
        self.__network = nx.DiGraph(name='RETE network visualization')

    def build(self, node):
        cls = node.__class__
        method = getattr(self, 'build' + cls.__name__, self.default)
        return method(node)

    def buildRootNode(self, node):
        self.__network.add_node(id(node), label='root', node_type='RootNode', style='filled', fontname='arial', fillcolor='lightgrey')

        for child in node.children:
            self.build(node.children[child])

    def buildAlphaNode(self, node):
        self.__network.add_node(id(node), label=str(node.label) + '\n', node_type='AlphaNode', style='filled', fontname='arial', fillcolor='#32b2ff')
        self.__network.add_edge(id(node.parent), id(node))

        for child in node.children:
            self.build(node.children[child])

        if node.alpha_memory_node is not None:
            self.build(node.alpha_memory_node)

    def buildAlphaMemoryNode(self, node):
        self.__network.add_node(id(node), label=str(node), node_type='AlphaMemoryNode', style='filled, rounded', fontname='arial', fillcolor='#f8ff04', shape='box')
        self.__network.add_edge(id(node.parent), id(node))

        for child in node.children:
            self.build(child)

    def buildJoinNode(self, node):
        self.__network.add_node(id(node), label=str(node), node_type='JoinNode', style='filled', fontname='arial', fillcolor='#00cc33')
        self.__network.add_edge(id(node.parent), id(node))
        self.__network.add_edge(id(node.alpha_memory), id(node))

        for child in node.children:
            self.build(child)

    def buildDummyJoinNode(self, node):
        self.__network.add_node(id(node), label=str(node), node_type='JoinNode', style='filled', fontname='arial', fillcolor='#339900')
        self.__network.add_edge(id(node.alpha_memory), id(node))

        for child in node.children:
            self.build(child)

    def buildBetaMemoryNode(self, node):
        self.__network.add_node(id(node), label=str(node), node_type='BetaMemoryNode', style='filled, rounded', fontname='arial', fillcolor='#e355a7', shape='box')
        self.__network.add_edge(id(node.parent), id(node))

        for child in node.children:
            self.build(child)

    def buildPNode(self, node):
        self.__network.add_node(id(node), label=str(node), node_type='PNode', style='filled', fontcolor='white', fontname='arial', fillcolor='#cc0033')
        self.__network.add_edge(id(node.parent), id(node))

    def default(self, node):
        pass

    # Requires Networkx and Graphviz to be installed.
    def draw_png_to_file(self, filename):
        # Scrive il file png con il nome specificato
        nx.to_pydot(self.__network).write_png(filename)

    # Requires Networkx and Graphviz to be installed.
    def draw_svg_to_file(self, filename):
        # Scrive il file svg con il nome specificato
        nx.to_pydot(self.__network).write_svg(filename)

if __name__ == '__main__':
    parser = Parser()

    ast = parser.parseFile('../../programs/MissionariNP.clp')

    builder = Builder()

    (facts, rules) = builder.build(ast)

    evaluator = builder.evaluator

    network = Network(evaluator, DepthStrategy())

    network.build_network(copy.deepcopy(facts), copy.deepcopy(rules))

    pm = network.production_memory

    wm = network.working_memory

    agenda = network.agenda

    print 'Working memory:'
    print wm

    print 'Initial agenda:\n', agenda

    start = time.clock()

    network.recognize_act_cycle()

    end = time.clock()

    print 'TIME', (end - start)

    print '\nFinal agenda:\n', agenda

    print '\nExecuted activations:', network.fired_activations

    print '\nWorking memory:'
    print wm

    plotter = Plotter()

    plotter.build(network.root_node)

    plotter.draw_svg_to_file('Rete.svg')
