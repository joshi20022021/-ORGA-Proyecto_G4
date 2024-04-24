#!/usr/bin/env python3

import ply.lex as lex

"""
    @author: sebas-v-c
"""


literals = ["(", ")", ",", ";"]
reserved = {
    "new_print": "NEW_PRINT",
    "end_print": "END_PRINT",
    "set_print_x": "PRINT_X",
    "set_print_o": "PRINT_O",
    "set_print_triangulo": "PRINT_TRI",
    "set_print_estrella": "PRINT_STAR",
}

tokens = list(reserved.values()) + [
    "COLOR",
    "ID",
    "NUMBER",
    "COMMENT",
]

t_ignore_COMMENT = r"\#.*"
t_ignore = " \t"


def t_COLOR(t):
    r"cyan|magenta|amarillo|negro"
    t.value = str(t.value).lower()
    return t


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# define a rule so we can track column
def find_column(input, token):
    line_start = input.rfind("\n", 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
