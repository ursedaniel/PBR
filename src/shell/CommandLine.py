#!/usr/bin/env python

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""
import re
import cmd

import platform

import os

import time

import copy

from core.exceptions.Exceptions import ParseException, EvaluateException

from core.parser.Parser import Parser

from core.Builder import Builder

from core.Evaluator import Evaluator

from core.rete.Network import Network

from core.rete.Strategy import DepthStrategy

from core.functions.Functions import Functions

from core.functions.Predicates import Predicates

from core.typesystem.TypeSystem import BaseType

from core.rete.Plotter import Plotter

wstream = None

colored_loaded = False

# If the operating system doesn't support the POSIX standard
# then it uses the pyreadline module; otherwise, it uses
# the readline module and it sets the autocompletion.
try:
    if os.name is not 'posix':
        import pyreadline as readline
    else:
        import readline
        if 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")

except Exception:
    print '\nWarning! Pyreadline or readline should be installed.\n   Unix-like: "pip install readline"\n \
            Windows: "pip install pyreadline"\nThe system will start without keys support.\n'

# Se sono disponibili le librerie aggiuntive
# allora utilizza i colori; in caso contrario
# utilizza la linea di comando classica
try:
    import sys
    from colorama import init
    from termcolor import colored
    from colorama import AnsiToWin32
    init(wrap=False)
    wstream = AnsiToWin32(sys.stderr).stream
    colored_loaded = True

except ImportError:
    print 'To use colors install termcolor and colorama:\n   "pip install colorama termcolor"'
    colored_loaded = False


def colortext(text, color, attribs=False):
    """
    Imposta i colori per la shell se le dipendenze sono soddisfatte.
    """
    global colored_loaded
    if colored_loaded:
        if attribs:
            return colored(text, color, None, ['bold'])
        else:
            return colored(text, color)
    else:
        return text


class CommandLine(cmd.Cmd):
    """
    A class for the command line.
    It is not possible to give multiline commands.

    This class is useful to parse two elements:
    1. the command
    2. the argument (or the arguments)

    For instance (assert (black dog) (black cat)) is equal to:
    1. Command: assert
    2. Argument: (black dog) (black cat)

    If the command is recognized the system proceed its computation sending
    the whole string (command argument) to the parser and then evaluate it.
    """

    def __init__(self):
        cmd.Cmd.__init__(self)

        # Declaration of the variables.
        self.__strategy = DepthStrategy()
        self.clear()

        self.count = 0

        # Declaration of the variables of the shell.
        global wstream, colored_loaded
        self.__milestone = 'PBR PROJECT'
        self.__version = '1.0'
        self.__main_title = 'Algoritm Rete ' + self.__version + ' (' + self.__milestone + ')'
        self.__wstream = wstream
        self.__colored_loaded = colored_loaded
        self.__error_prefix = str(colortext(r'[ERROR] ', 'red', True))
        self.__start_time = 0
        self.__elapsed_time = 0
        self.__stats = True
        self.__default_exception_message = 'Unknown exception!'
        self.use_rawinput = True
        self.ruler = '='
        self.default_file_name = 'new.clp'
        self.prompt = str(colortext('ALGORITMUL RETE - PROIECT > ', 'green'))
        self.intro = """\

______________________________________
""" + self.__main_title + """

Running on Python """ + str(platform.python_version()) + ' ' + str(platform.architecture()[0]) + """
     ''     ''    ''
    Pasul 1:
    Foloseste load #calea catre fisier#.

    Pasul 2:
    Foloseste comanda reset.
    
    Pasul 3:
    Foloseste comanda run 1.
    
    Pasul Final:
    Foloseste comanda exit pentru a primi rezultatele.
    
    Alte Comenzi:
    Trebuie folosite dupa Pasul 2:
        rules - pentru a returna regulile.
        facts - pentru a returna faptele.
       """

    def clear(self, ):
        self.__parser = Parser()
        self.__builder = Builder()
        self.__facts = []
        self.__rules = {}
        self.__globals = {}
        self.__evaluator = self.__builder.evaluator
        self.__network = Network(self.__evaluator, self.__strategy)
        self.__agenda = self.__network.agenda
        self.__working_memory = None
        self.__production_memory = None
        self.__predicates_list = sorted(Predicates().get_names())
        self.__functions_list = sorted(Functions().get_names())

        self.networks = list()

    def start_timer(self):
        """
        Save computation start time.
        """
        self.__start_time = time.time()

    def stop_timer(self):
        """
        Save computation elapsed time.
        """
        self.__elapsed_time = time.time() - self.__start_time

    def get_stats(self):
        """
        Return text containing statistics about last computation.
        """
        s = ''
        s += 'Elapsed time: ' + str(self.__elapsed_time) + ' seconds.\n'
        s += 'Fired rules: ' + str(self.__network.fired_activations) + '.\n'

        if self.__elapsed_time < 1e-10:
            self.__elapsed_time += 1e-10

        s += str(self.__network.fired_activations/self.__elapsed_time) + ' rules per second.\n'
        return s

    # --- Beginning of the commands.

    # Assert
    def do_assert(self, line):
        """
        It creates one or more facts and adds them to the working memory.
        If a fact has been already asserted then it returns false.

        Usage:  (assert <fact>+)

        Examples:   (assert (light red) (light green))
                    (assert (mark is-tall 1.80))
                    (assert (height (+ 1 0.80)))

        See the documentation for more.
        """
        if line:
            try:
                assertions = '(assert ' + line + ')'
                ast = self.__parser.parseAssert(assertions)

                print ''
                facts = self.__builder.build_assert(ast)
                print ''

                if not self.__working_memory:
                    self.do_reset('')

                self.__facts.extend(facts)

                for fact in facts:
                    fact_assertion = self.__network.assert_fact(fact)

                    if fact_assertion is None:
                        print 'The fact already exists!\n'

            except ParseException as e:
                print ''
                self.print_error(str(e))
                print ''
            except EvaluateException as e:
                print ''
                self.print_error(str(e))
                print ''

    # Retract
    def do_retract(self, line):
        """
        It removes one or more facts from the working memory.
        This procedure is called retraction.
        When a retraction is executed it could generate changes on the agenda.

        Usage:  (retract (<fact-index>|<fact-address>)+)

        Examples:   (retract 1)
                    (retract 4 3)
                    (retract ?f)
                    (retract ?g ?h)
                    (retract 6 ?t ?x 5 7)

        See the documentation for more.
        """
        if line:
            try:
                retractions = '(retract ' + line + ')'
                ast = self.__parser.parseRetract(retractions)

                print ''
                for identifier in ast[1:]:
                    if self.__network.retract_fact(identifier.content):
                        print 'The fact with identifier ' + str(identifier) + ' has been removed.'
                    else:
                        print 'The fact ' + str(identifier) + ' doesn\'t exist!'
                print ''

            except ParseException as e:
                print ''
                self.print_error(str(e))
                print ''
            except EvaluateException as e:
                print ''
                self.print_error(str(e))
                print ''

        else:
            print '\nOne or more fact identifiers must be specified!\n'

    # Deffacts
    def do_deffacts(self, line):
        """
        A good way to define multiple facts.
        It is necessary to use when facts must be loaded from file.
        An assert, instead, is for RHS of a rule and for shell interaction.

        Usage:  (deffacts <name> [comment] <fact>*)

        Examples: (deffacts test "comment test" (hello hi) (goodbye bye))
                  (deffacts trying (one) (two) (three))
                  (deffacts something)

        See the documentation for more.
        """
        if line:
            try:
                deffacts = '(deffacts ' + line + ')'
                ast = self.__parser.parseProgram(deffacts)

                print ''
                (facts, _) = self.__builder.build(ast)
                print ''

                self.__facts.extend(facts)

                if not self.__working_memory:
                    self.do_reset('')

                for fact in facts:
                    self.__network.assert_fact(fact)

            except ParseException as e:
                print ''
                self.print_error(str(e))
                print ''
            except EvaluateException as e:
                print ''
                self.print_error(str(e))
                print ''
            except Exception as e:
                print ''
                self.print_error(self.__default_exception_message)
                print ''

    # Defrule
    def do_defrule(self, line):
        """
        It defines a production rule: LHS --> RHS
        LHS stands for left hand side, composed by parttern queries.
        RHS stands for right hand side, composed by actions.
        If a LHS is satisfied, then the actions in RHS will be executed.

        Usage:  (defrule <name> [comment] LHS => RHS)

        Examples: (defrule t1 "tst1" (pattern ?a) => (assert (hello)))
                  (defrule t2 "tst2" (pattern ?b ?a) => (assert (hi)))

        See the documentation for more.
        """
        if line:
            try:

                defrule = '(defrule ' + line + ')'
                ast = self.__parser.parseProgram(defrule)

                print ''
                (_, rules) = self.__builder.build(ast)
                print ''

                if not self.__production_memory:
                    self.do_reset('')

                for rule in rules:
                    if rule.name in self.__rules:
                        print '[WARNING] Redefining an existing rule \"' + str(rule.name) + '\"!'

                    self.__rules[rule.name] = rule

                rules = reversed(list(rules))

                for rule in rules:
                    self.__network.add_rule(rule)

            except ParseException as e:
                print ''
                self.print_error(str(e))
                print ''
            except EvaluateException as e:
                print ''
                self.print_error(str(e))
                print ''
            except Exception as e:
                print ''
                self.print_error(self.__default_exception_message)
                print ''

    # Deglobal
    def do_defglobal(self, line):
        """
        A container to define global variables.
        A global variable must be initialized.
        Global variables are shared between facts and rules.

        Usage:  (defglobal <global-assignment>*)

        Examples: (defglobal ?*x* = 10)
                  (defglobal ?*x* = 10  ?*c*="hello")

        See the documentation for more.
        """
        if line:
            try:
                defglobal = '(defglobal ' + line + ')'
                ast = self.__parser.parseProgram(defglobal)
                print ''
                self.__builder.build(ast)
                print ''
            except ParseException as e:
                print ''
                self.print_error(str(e))
                print ''
            except EvaluateException as e:
                print ''
                self.print_error(str(e))
                print ''
            except Exception as e:
                print ''
                self.print_error(self.__default_exception_message)
                print ''
        else:
            print '\nYou should specify a global variable!\n'

    # Clear
    def do_clear(self, line):
        """
        It removes all facts and rules.
        If a file has been loaded, after a clear, it must be loaded again.
        It's just like quit and start again the system.

        Usage:  (clear)
        """
        line = ''
        self.clear()

    # Reset
    def do_reset(self, line):
        """
        The reset command works on facts:
            1) It removes existing facts from the working memory.
            2) It asserts facts from existing deffacts statements.
            3) It builds the network of rules.

        Usage:  (reset)
        """
        line = ''

        try:
            print '\nBuilding network... '

            self.__builder.reset()

            self.__evaluator.environment.global_variables = copy.copy(self.__globals)

            self.__network.build_network(copy.deepcopy(self.__facts), copy.deepcopy(self.__rules.values()))

            self.networks.append(self.__network)

            self.__agenda = self.__network.agenda

            self.__working_memory = self.__network.working_memory

            self.__production_memory = self.__network.production_memory

            if not self.__rules:
                print '\nEmpty network created.\n'

            print 'OK.\n'
        except EvaluateException as e:
            print ''
            self.print_error(str(e))
            print ''
        except Exception as e:
            print ''
            self.print_error(str(e))
            print ''

    # Globals
    def do_globals(self, line):
        """
        The globals command shows the list of declared global variables.

        Usage:  (globals)
        """
        line = ''
        if self.__evaluator.environment.global_variables:
            print ''
            for v in self.__evaluator.environment.global_variables:
                print str(v.name) + ' = ' + str(self.__evaluator.environment.global_variables[v])
            print ''
        else:
            print '\nNo globals defined!\n'

    # Facts
    def do_facts(self, line):
        """
        The facts command shows the list of all facts.
        Each fact is shown with its own index.

        Usage:  (facts)
        """
        line = ''
        if self.__working_memory:
            print ''
            print self.__working_memory
            print ''

            with open('facts.txt', 'w') as file:
                file.write(str(self.__working_memory))
        else:
            print '\nWorking memory not initialized yet!\n'

            with open('facts.txt', 'w') as file:
                file.write('Working memory not initialized yet!')

    # Rules
    def do_rules(self, line):
        """
        The rules command shows the names of all rules.

        Usage:  (rules)
        """
        line = ''
        if self.__production_memory:
            print ''
            print self.__production_memory
            print ''
            with open('rules.txt', 'w') as file:
                file.write(str(self.__production_memory))
        else:
            print '\nProduction memory not initialized yet!\n'
            with open('rules.txt', 'w') as file:
                file.write('Production memory not initialized yet!')

    # Agenda
    def do_agenda(self, line):
        """
        The agenda is a collection of activations which match pattern entities.
        If all the patterns of a rule match facts, its activation is added.
        Thus for one rule there could be more than one activation.
        At the end of a matching cycle, the agenda is reordered.
        The next activation will be always on top.
        This last step is called conflict resolution.
        See "strategy" for available strategies.

        Usage:  (agenda)
        """
        line = ''
        if self.__agenda:
            print ''
            print self.__agenda
            print ''
            with open('rules.txt', 'w') as file:
                file.write(str(self.__agenda))
        else:
            print '\nNetwork not initialized yet!\n'
            with open('rules.txt', 'w') as file:
                file.write('Network not initialized yet!')

    # Run
    def do_run(self, times):
        """
        To make the program run, just enter the run command.
        Using deffacts, you must do a reset before a run.

        To trace a program you should specify a maximum number of cycles.
        Otherwise, it will run until no rule is activated.

        Usage:  (run)
                (run <number of steps>)
        """
        graphs = list()
        if times:
            try:
                times = abs(int(times))
            except ValueError:
                print ''
                self.print_error('Times must be an integer. Example: (run 10).')
                print ''
            except Exception:
                print ''
                self.print_error(self.__default_exception_message)
                print ''
        else:
            times = None

        if self.__network is not None:
            try:
                if self.__network.agenda.get_activations():
                    print '\nStarting recognize-act-cycle...'
                    self.start_timer()
                    self.__network.recognize_act_cycle(times)
                    graphs = self.__network.build_network(copy.deepcopy(self.__facts), copy.deepcopy(self.__rules.values()))
                    self.stop_timer()
                    if self.__stats:
                        print self.get_stats()
                        with open('stats.txt', 'w') as file:
                            file.write(str(self.get_stats()))
                else:
                    print '\nNo rule to fire!\n'
            except EvaluateException as e:
                print ''
                self.print_error(str(e))
                print ''
        else:
            print '\nYou should execute reset before run!\n'

        self.count = 0
        for graph in graphs:
            self.count += 1
            print '\nSe genereaza fisierul roteNode' + str(self.count) + '.json'
            graphString = str(graph).replace('(', '')
            graphString = graphString.replace(')', '')
            graphString = graphString.replace('None', '')
            graphString = graphString.replace(', ,', ',')
            graphString = graphString.replace(' {}, ', '')
            graphString = graphString.replace('Empty Alpha Memory', '{Empty Alpha Memory: {} }')
            graphString = graphString.replace('}, }', '} }')
            graphString = graphString.replace('}, }', '} }')
            graphString = re.sub(r'([0-9]+: [a-zA-Z ]+)+', r'{ "\1;": ', graphString)
            graphString = re.sub(r'(\[[0-9]+\]),', r'{ "\1": {} }, ', graphString)
            graphString = re.sub(r': (\[[0-9]+\])', r': { "\1": {} } } ', graphString)
            graphString = re.sub(r'([a-zA-Z ]+):', r'"\1":', graphString)
            graphString = graphString.replace('?"', '"?')
            graphString.replace('\n', '')
            graphList = graphString.split(';')
            for index in graphList[1::]:
               temp = index.replace(': \n{ ', '')
               graphList[0] = graphList[0] + temp
            graphString = graphList[0].replace('""','; ')
            self.do_draw(graph, 'png')
            with open('roteNode' + str(self.count) + '.json', 'w') as file:
                file.write(graphString)

            with open('test' + str(self.count) + '.txt', 'w') as file:
                file.write(str(graph.root_node))

    # Strategy
    def do_strategy(self, strategy):
        """
        It allows to change the strategy for conflict resolution.
        If no parameter is specified, it shows the current strategy.

        Available strategies:
        Depth, Breadth, Random, Simplicity, Complexity, LEX and MEA.

        The default strategy is Depth.

        Usage:  (strategy <strategy>)
        """

        if not self.__network:
            print '\nYou should execute reset before changing the strategy!\n'
            return

        if strategy:
            strategy = str.lower(strategy)
            if strategy in self.__network.agenda.strategies:
                self.__strategy = self.__network.agenda.strategies[strategy]()
                self.__network.agenda.change_strategy(self.__strategy)
            else:
                print '\nThe specified strategy doesn\'t exist!\n'
        else:
            print ''
            print str(self.__network.agenda.strategy)
            print ''

    # --- Fine comandi

    # --- Altre funzioni di supporto

    # Visualizza la lista delle funzioni supportate dal sistema
    def help_functions(self):
        print '\n\tA list of supported functions.\n\tThey are used inside an assert, a deffacts or a defrule.\n'

        sys.stdout.write('\t')
        print '\n\t'.join(self.__functions_list)
        print ''

    # Visualizza la lista dei predicati supportati dal sistema
    def help_predicates(self):
        print '\n\tA list of supported predicates.\n\tThey are used inside an assert, a deffacts or a defrule.\n'

        sys.stdout.write('\t')
        print '\n\t'.join(self.__predicates_list)
        print ''

    # Visualizza le statistiche sul run eseguito
    def do_stats(self, line):
        """
        It shows some statistics about rules, time and more.

        Usage:  (stats on)
                (stats off)
        """
        line = line.lower()
        if line == 'on':
            # @TODO enable stats
            self.__stats = True
            print 'Stats enabled.'
        elif line == 'off':
            # @TODO disable stats
            self.__stats = False
            print 'Stats disabled.'
        else:
            self.print_error('Bad argument! Valid arguments are: on, off.')

    # Pulizia preliminare dell'input nel caso in cui il comando venga inserito usando le parentesi.
    # In questo modo e' possibile scrivere (deffacts ...) oppure deffacts ...
    def precmd(self, line):
        """Useful to clear the input line."""
        line = line.lstrip().rstrip()
        if (len(line) > 0) and line[0] == '(' and line[-1] == ')':
            return line[1:-1]
        else:
            return line

    # Override di emptyline, evita di ripetere l'ultimo comando nel caso in cui si prema invio senza
    # digitare alcun carattere
    def emptyline(self):
        """
        Override of default empyline.
        If enter is pressed on empty prompt, it will not repeat the last command.
        """
        pass

    # Gestione errore
    def default(self, line):
        """Default behavior when no functions or predicates with given name are available."""
        # cattura il nome della funzione ed i parametri
        function = line.split(' ')
        fname = function.pop(0)
        params = function

        msg = 'Missing function declaration for ' + colortext(fname, 'magenta', True) + ' '
        if len(params) > 0:
            msg += '(args: ' + colortext(' '.join(params), 'cyan') + ')'
        self.print_error(msg)

    def print_error(self, msg):
        """
        It prints the error colored or not.
        It depends on available modules.
        """
        global wstream
        if wstream is not None:
            print >>wstream, self.__error_prefix + msg
        else:
            print self.__error_prefix + msg

    # Help dell'help
    def help_help(self):
        """
        Simply write the keyword help followed by a command name.
        Please, write the command without brackets.

        Usage: (help <command>)
        """
        print """
        Simply write the keyword help followed by a command name.
        Please, write the command without brackets.

        Usage: (help <command>)
        """

    # --- Gestione file

    # Legge il file specificato
    def do_load(self, line):
        """
        It loads a turtle file into the system.
        Remember to do a reset to instantiate deffacts statements.

        Usage: (load <filename>)
        """

        if not line:
            print ''
            self.print_error('Filename should be specified!')
            print ''
            return

        print '\nLoading file... '

        try:
            ast = self.__parser.parseFile(line)

            (facts, rules) = self.__builder.build(ast)

            self.__globals.update(self.__evaluator.environment.global_variables)

            self.__facts.extend(facts)

            for rule in rules:
                if rule.name in self.__rules:
                    print '[WARNING] Redefining an existing rule \"' + str(rule.name) + '\"!'

                self.__rules[rule.name] = rule

            print 'OK.\n'

        except ParseException as e:
            print ''
            self.print_error(str(e))
            print ''
        except EvaluateException as e:
            print ''
            self.print_error(str(e))
            print ''
        except IOError as e:
            print ''
            self.print_error('Unable to access the file \"' + line + '\"!')
            print ''
        except Exception as e:
            print ''
            self.print_error(self.__default_exception_message)
            print ''

    def do_draw(self, graph, line='svg'):
        """
        It draws the current RETE-like network graph.
        The plot will be saved as RETE.<format>
        Available formats: png, svg.
        The default format is svg.

        Usage: (draw <format>)

        Examples:   (draw png)
                    (draw svg)

        See the documentation for more.
        """
        plotter = Plotter()
        filename = 'RETE' + str(self.count)

        if graph:
            plotter.build(graph.root_node)

            if line:
                try:
                        if line == 'png':
                            plotter.draw_png_to_file(filename + '.png')
                            print '\nFile', filename + '.png', 'created.\n'
                        elif line == 'svg':
                            plotter.draw_svg_to_file(filename + '.svg')
                            print '\nFile', filename + '.svg', 'created.\n'
                        else:
                            print '\nInvalid format! Valid formats are: png, svg!\n'

                except IOError:
                    print '\nYou have to specify a correct filename!\n'
            else:
                plotter.draw_svg_to_file(filename + '.svg')
                print '\nFile', filename + '.svg', 'created.\n'
        else:
            print '\nNetwork not built yet!\n'
    # --- Gestione della terminazione

    # Quit
    def do_quit(self, line):
        """
        Quit command.

        Usage:  (quit)
        """
        return True

    # Exit
    def do_exit(self, line):
        """
        Exit command.

        Usage:  (exit)
        """
        return True

    # EOF
    def do_EOF(self, line):
        """
        It exits writing EOF or pressing Ctrl+d.
        Only in this case there will be a question to confirm.

        Usage:  (EOF)
                Press CTRL+D keys
        """
        if raw_input('Really exit?(y/n): ') == 'y':
            return True
