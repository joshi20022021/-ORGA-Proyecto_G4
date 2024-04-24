from parser import parser

import logging

data = """
# esto es un comentario

new_print PrimeraImpresion;


# set_print_x(fila, columna, color);
# set_print_o(fila, columna, color);
# set_print_triangulo(fila, columna, color);
# set_print_estrella(fila, columna, color);

# coordenadas para el jugador x
set_print_x(1, 1, cyan);
set_print_x(2, 1, negro);
set_print_x(2, 2, cyan);
set_print_x(3, 2, amarillo);
set_print_x(3, 3, magenta);


# coordanadas para el jugador o
set_print_o(3, 1, magenta);
set_print_o(1, 2, cyan);
set_print_o(1, 3, amarillo);
set_print_o(2, 3, negro);

end_print;

"""


data = parser.parse(data)
print(data)
