#!/usr/bin/env python3

import ply.yacc as yacc
from lexer import *

from printjob import PrintJob, Instruction

"""
    @author: sebas-v-c
"""


def p_star(p):
    """
    start   : prints
    """
    p[0] = p[1]


def p_prints(p):
    """
    prints  : prints print
            | print
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_print(p):
    """
    print   : NEW_PRINT ID ';' statements END_PRINT ';'
    """
    new_print = PrintJob(p[2])
    new_print.instructions = p[4]
    p[0] = new_print


def p_statements_sequence(p):
    """
    statements  : statements statement ';'
                | statement ';'
    """
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement_definition(p):
    """
    statement   :
                |   PRINT_X '(' NUMBER ',' NUMBER ',' COLOR ')'
                |   PRINT_O '(' NUMBER ',' NUMBER ',' COLOR ')'
                |   PRINT_TRI '(' NUMBER ',' NUMBER ',' COLOR ')'
                |   PRINT_STAR '(' NUMBER ',' NUMBER ',' COLOR ')'
    """
    if p[1] == "set_print_x":
        p[0] = Instruction("x", p[3], p[5], p[7])
    elif p[1] == "set_print_o":
        p[0] = Instruction("o", p[3], p[5], p[7])
    elif p[1] == "set_print_triangulo":
        p[0] = Instruction("triangulo", p[3], p[5], p[7])
    elif p[1] == "set_print_estrella":
        p[0] = Instruction("estrella", p[3], p[5], p[7])


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()
