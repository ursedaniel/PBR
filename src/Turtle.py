#!/usr/bin/env python

from shell.CommandLine import CommandLine

"""
    TURTLE
    An expert system shell inspired by CLIPS syntax
    @author Claudio Greco, Daniele Negro, Marco Di Pietro
"""

if __name__ == '__main__':
    try:
        turtle = CommandLine()
        turtle.cmdloop()

    except (KeyboardInterrupt, SystemExit):
        print '\nCtrl-c detected. Exit.'

    print '\nGoodbye!'
