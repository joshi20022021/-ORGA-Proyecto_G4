#!/usr/bin/env python3

import ply.yacc as yacc
from lexer import tokens

"""
    @author: sebas-v-c
"""


def p_star(p):
    """
    start   : prints
    """
    pass


def p_prints(p):
    """
    prints  : prints NEW_PRINT ID ';' statements END_PRINT ';'
            | NEW_PRINT ID ';' statements END_PRINT ';'
    """
    if len(p) == 7:
        p[0] = [{p[2]: p[4]}]
    else:
        p[0] = p[1] + [{p[3]: p[5]}]


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
        p[0] = {"shape": "x", "row": p[3], "column": p[5], "color": p[7]}
    elif p[1] == "set_print_o":
        p[0] = {"shape": "o", "row": p[3], "column": p[5], "color": p[7]}
    elif p[1] == "set_print_triangulo":
        p[0] = {"shape": "triangulo", "row": p[3], "column": p[5], "color": p[7]}
    elif p[1] == "set_print_estrella":
        p[0] = {"shape": "estrella", "row": p[3], "column": p[5], "color": p[7]}


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()
