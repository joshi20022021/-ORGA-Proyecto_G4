#!/usr/bin/env python3

import ply.lex as lex
import ply.yacc as yacc


tokens = {"NUMBER", "COLOR", "FUNCTION", "COMMENT"}

t_NUMBER = r"\d+"
t_COLOR = r"cyan|magenta|amarillo|negro"
t_TEXT = r"[a-zA-Z_][a-zA-Z0-9_]*"

kw_PRINT_X = r"set_print_x"
kw_PRINT_O = r"set_print_o"
kw_PRINT_TRIANGLE = r"set_print_triangulo"
kw_PRINT_STAR = r"set_print_estrella"

kw_NEW_JOB = r"new_print"
kw_END_JOB = r"end_print"
