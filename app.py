import tkinter as tk
from tkinter import filedialog, messagebox
import ply.lex as lex
import re

class AnalizadorLexico:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    tokens = (
        'COMMENT',
        'NEW_PRINT',
        'SET_PRINT',
        'COORDINATES',
        'COLOR'
    )

    # Tokens
    t_COMMENT = r'\#.*'
    t_NEW_PRINT = r'new_print'
    t_SET_PRINT = r'set_print_[XO△☆]'
    t_COORDINATES = r'\(\s*\d+\s*,\s*\d+\s*\)'
    t_COLOR = r'(cyan|negro|amarillo|magenta)'

    # Ignored characters
    t_ignore = ' \t'

    # Error handling
    def t_error(self, t):
        print(f"Ilegal caracter '{t.value[0]}'")
        t.lexer.skip(1)

    def verificar_estructura(self, contenido):
        self.lexer.input(contenido)
        for tok in self.lexer:
            if tok.type == 'COMMENT':
                continue
            if tok.type == 'NEW_PRINT':
                continue
            if tok.type != 'SET_PRINT':
                return False, f"Estructura incorrecta en la línea {tok.lineno}"
            partes = re.findall(r'\w+', tok.value)  # Dividir la línea en partes
            if len(partes) != 4:  # Verificar que haya cuatro partes (figura, coordenadas, color)
                return False, f"Error en la línea {tok.lineno}: Estructura incorrecta"
            coordenadas = partes[2:4]
            for coord in coordenadas:
                if not re.match(r'\(\s*\d+\s*,\s*\d+\s*\)', coord):
                    return False, f"Error en la línea {tok.lineno}: Coordenadas inválidas"
        return True, "Estructura del archivo válida"

class TotitoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Totito App")
        self.root.configure(background="#f0f0f0")
        
        # Matriz para representar el tablero 3x3
        self.tablero = [[' ' for _ in range(3)] for _ in range(3)]
        
        # Estilo para los botones de las figuras
        self.figura_btn_style = {"bg": "#d9d9d9", "activebackground": "#bfbfbf", "pady": 5}

        # Botones para elegir las figuras
        self.botones_figuras = []
        self.figuras = {"X": "✕", "O": "◯", "Estrella": "☆", "Triangulo": "△"}
        for figura, caracter in self.figuras.items():
            btn = tk.Button(root, text=caracter, command=lambda f=figura: self.elegir_figura(f), **self.figura_btn_style)
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.botones_figuras.append(btn)
        
        # Canvas para dibujar el tablero
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack()
        self.dibujar_tablero()

        # Botón para cargar desde archivo
        btn_cargar = tk.Button(root, text="Cargar desde archivo", command=self.cargar_desde_archivo, padx=10, pady=5, bg="#007bff", fg="white", activebackground="#0056b3")
        btn_cargar.pack(pady=10)

    def dibujar_tablero(self):
        # Dibuja las líneas del tablero
        for i in range(1, 3):
            self.canvas.create_line(100 * i, 0, 100 * i, 300)
            self.canvas.create_line(0, 100 * i, 300, 100 * i)

    def elegir_figura(self, figura):
        if figura in ["X", "O"]:
            self.ventana_coordenadas(figura)
        elif figura == "Estrella":
            self.ventana_coordenadas(figura)
        elif figura == "Triangulo":
            self.ventana_coordenadas(figura)

    def ventana_coordenadas(self, figura):
        ventana = tk.Toplevel(self.root)
        ventana.title("Ingrese fila y columna")
        ventana.configure(background="#f0f0f0")
        
        tk.Label(ventana, text="Fila (1-3):", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(ventana, text="Columna (1-3):", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(ventana, text="Color:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)

        entry_fila = tk.Entry(ventana)
        entry_fila.grid(row=0, column=1, padx=5, pady=5)
        entry_columna = tk.Entry(ventana)
        entry_columna.grid(row=1, column=1, padx=5, pady=5)

        colores = ["cyan", "magenta", "yellow", "black"]
        color_variable = tk.StringVar(ventana)
        color_variable.set(colores[0])
        dropdown_color = tk.OptionMenu(ventana, color_variable, *colores)
        dropdown_color.grid(row=2, column=1, padx=5, pady=5)

        btn_confirmar = tk.Button(ventana, text="Confirmar", command=lambda: self.dibujar_figura(figura, entry_fila.get(), entry_columna.get(), color_variable.get()), bg="#007bff", fg="white", activebackground="#0056b3")
        btn_confirmar.grid(row=3, columnspan=2, padx=5, pady=5)

    def dibujar_figura(self, figura, fila, columna, color):
        try:
            fila = int(fila)
            columna = int(columna)
            if fila < 1 or fila > 3 or columna < 1 or columna > 3:
                messagebox.showerror("Error", "Coordenadas fuera de rango (1-3).")
                return
            # Calcular coordenadas en píxeles
            x = columna * 100 - 50
            y = fila * 100 - 50
            if figura == "X":
                self.canvas.create_line(x-40, y-40, x+40, y+40, fill=color, width=2)
                self.canvas.create_line(x-40, y+40, x+40, y-40, fill=color, width=2)
            elif figura == "O":
                self.canvas.create_oval(x-40, y-40, x+40, y+40, outline=color, width=2)
            elif figura == "Estrella":
                puntos = [x, y-50, x-20, y-20, x-50, y, x-20, y+20, x, y+50, x+20, y+20, x+50, y, x+20, y-20]
                self.canvas.create_polygon(puntos, fill=color, outline=color)
            elif figura == "Triangulo":
                puntos = [x, y-50, x-50, y+50, x+50, y+50]
                self.canvas.create_polygon(puntos, fill=color, outline=color)
            # Actualizar la matriz del tablero
            self.tablero[fila-1][columna-1] = figura
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos para fila y columna.")


    def colocar_figura(self, figura, fila, columna, color):
        # Coloca la figura en el tablero en las coordenadas especificadas
        x = columna * 100 - 50
        y = fila * 100 - 50
        if figura == "X":
            self.canvas.create_line(x-40, y-40, x+40, y+40, fill=color, width=2)
            self.canvas.create_line(x-40, y+40, x+40, y-40, fill=color, width=2)
        elif figura == "O":
            self.canvas.create_oval(x-40, y-40, x+40, y+40, outline=color, width=2)
        elif figura == "Estrella":
            puntos = [x, y-50, x-20, y-20, x-50, y, x-20, y+20, x, y+50, x+20, y+20, x+50, y, x+20, y-20]
            self.canvas.create_polygon(puntos, fill=color, outline=color)
        elif figura == "Triangulo":
            puntos = [x, y-50, x-50, y+50, x+50, y+50]
            self.canvas.create_polygon(puntos, fill=color, outline=color)

        # Actualiza la matriz del tablero
        self.tablero[fila-1][columna-1] = figura

    def cargar_desde_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos .olc", "*.olc")])
        if archivo:
            try:
                with open(archivo, 'r') as file:
                    contenido = file.read()
                    analizador_lexico = AnalizadorLexico()  # Instanciar el analizador léxico
                    if analizador_lexico.verificar_estructura(contenido):
                        # Procesar el contenido del archivo si la estructura es válida
                        lineas = contenido.split("\n")
                        for linea in lineas:
                            if linea.strip().startswith("set_print"):
                                partes = re.findall(r'\w+', linea)  # Dividir la línea en partes
                                figura = partes[0].split("_")[-1].lower()  # Obtener la figura de la línea
                                coordenadas = re.findall(r'\d+', linea)  # Extraer las coordenadas de la línea
                                if len(coordenadas) != 2:  # Verifica que haya dos elementos en coordenadas
                                    messagebox.showerror("Error", "Las coordenadas son inválidas.")
                                    continue
                                color = partes[-1]  # Obtener el color de la línea
                                fila, columna = map(int, coordenadas)
                                self.dibujar_figura(figura, fila, columna, color)
                    else:
                        messagebox.showerror("Error", "La estructura del archivo no es válida.")
            except FileNotFoundError:
                messagebox.showerror("Error", "El archivo no se encontró.")



if __name__ == "__main__":
    root = tk.Tk()
    app = TotitoApp(root)
    root.mainloop()
