import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os

class AplicacionPixelArt:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Aplicación de Pixel Art")
        self.imagen_id = None 
        self.raiz.bind("<Configure>", self.actualizar_tamanio)
        self.imagenes_en_lienzo = []

        # Estilos
        self.estilo = {
            "boton": {
                "font": ("Arial", 14),
                "foreground": "#ffffff",
                "activeforeground": "#ffffff",
                "borderwidth": 0,
                "padx": 10,
                "pady": 5
            },
            "boton_color": {
                "background": "",
                "activebackground": ""
            },
            "boton_cyan": {
                "background": "#00FFFF",
                "activebackground": "#00CCCC"
            },
            "boton_amarillo": {
                "background": "#FFFF00",
                "activebackground": "#CCCC00"
            },
            "boton_magenta": {
                "background": "#FF00FF",
                "activebackground": "#CC00CC"
            },
            "boton_negro": {
                "background": "#000000",
                "activebackground": "#333333"
            },
            "lienzo": {
                "background": "#eeeeee"
            },
            "boton_x": {
                "background": "#FF0000",  # Color rojo
                "activebackground": "#CC0000"  # Color rojo oscuro al presionar
            },
            "boton_o": {
                "background": "#00FF00",  # Color verde
                "activebackground": "#00CC00"  # Color verde oscuro al presionar
            },
            "boton_estrella": {
                "background": "#0000FF",  # Color azul
                "activebackground": "#0000CC"  # Color azul oscuro al presionar
            },
            "boton_triangulo": {
                "background": "#FF00FF",  # Color magenta
                "activebackground": "#CC00CC"  # Color magenta oscuro al presionar
            }
        }

        # Contenedor principal
        self.contenedor = tk.Frame(raiz)
        self.contenedor.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.contenedor.columnconfigure(0, weight=1)
        self.contenedor.columnconfigure(1, weight=3)
        self.contenedor.rowconfigure(0, weight=1)

        # Barra lateral izquierda para los botones
        self.barra_lateral = tk.Frame(self.contenedor, bg="#222222")
        self.barra_lateral.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        self.barra_lateral.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], weight=1)

        # Botones para 'X', 'O', estrella y triángulo
        self.boton_x = tk.Button(self.barra_lateral, text="X", command=lambda: self.seleccionar_simbolo('X'), **{**self.estilo["boton"], **self.estilo["boton_x"]})
        self.boton_x.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.boton_o = tk.Button(self.barra_lateral, text="O", command=lambda: self.seleccionar_simbolo('O'), **{**self.estilo["boton"], **self.estilo["boton_o"]})
        self.boton_o.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.boton_estrella = tk.Button(self.barra_lateral, text="Estrella", command=lambda: self.seleccionar_simbolo('*'), **{**self.estilo["boton"], **self.estilo["boton_estrella"]})
        self.boton_estrella.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.boton_triangulo = tk.Button(self.barra_lateral, text="Triángulo", command=lambda: self.seleccionar_simbolo('^'), **{**self.estilo["boton"], **self.estilo["boton_triangulo"]})
        self.boton_triangulo.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Botones de colores
        self.boton_cyan = tk.Button(self.barra_lateral, text="Cyan", command=lambda: self.seleccionar_color('#00FFFF'), **{**self.estilo["boton"], **self.estilo["boton_cyan"]})
        self.boton_cyan.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        self.boton_amarillo = tk.Button(self.barra_lateral, text="Amarillo", command=lambda: self.seleccionar_color('#FFFF00'), **{**self.estilo["boton"], **self.estilo["boton_amarillo"]})
        self.boton_amarillo.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        self.boton_magenta = tk.Button(self.barra_lateral, text="Magenta", command=lambda: self.seleccionar_color('#FF00FF'), **{**self.estilo["boton"], **self.estilo["boton_magenta"]})
        self.boton_magenta.grid(row=6, column=0, padx=5, pady=5, sticky="ew")
        self.boton_negro = tk.Button(self.barra_lateral, text="Negro", command=lambda: self.seleccionar_color('#000000'), **{**self.estilo["boton"], **self.estilo["boton_negro"]})
        self.boton_negro.grid(row=7, column=0, padx=5, pady=5, sticky="ew")

        # Lienzo de Pixel Art
        self.lienzo = tk.Canvas(self.contenedor, bg=self.estilo["lienzo"]["background"], width=500, height=500, highlightthickness=0)
        self.lienzo.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Imagen y estado de juego
        self.imagen = Image.new("RGB", (3, 3), "white")
        self.dibujo = ImageDraw.Draw(self.imagen)
        self.jugador_actual = 'X'

        # Dibujar el tablero tipo "totito"
        self.dibujar_tablero()

        # Ajustar tamaño inicialmente
        self.actualizar_tamanio()

    def actualizar_tamanio(self, event=None):
        self.lienzo.config(width=self.raiz.winfo_width() * 0.75, height=self.raiz.winfo_height() * 0.75)

    def seleccionar_simbolo(self, simbolo):
        print("Seleccionar símbolo:", simbolo)
        self.simbolo_seleccionado = simbolo

        # Solicitar coordenadas al usuario
        self.solicitar_coordenadas()

    def solicitar_coordenadas(self):
        # Crear una ventana secundaria para ingresar coordenadas
        self.ventana_coordenadas = tk.Toplevel(self.raiz)
        self.ventana_coordenadas.title("Ingresar Coordenadas")

        # Etiquetas y campos de entrada para las coordenadas
        tk.Label(self.ventana_coordenadas, text="Fila:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_fila = tk.Entry(self.ventana_coordenadas)
        self.entry_fila.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.ventana_coordenadas, text="Columna:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_columna = tk.Entry(self.ventana_coordenadas)
        self.entry_columna.grid(row=1, column=1, padx=5, pady=5)

        # Botón para aceptar coordenadas
        tk.Button(self.ventana_coordenadas, text="Aceptar", command=self.colocar_figura).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def colocar_figura(self):
        fila = int(self.entry_fila.get())
        columna = int(self.entry_columna.get())
        
        # Calculate the coordinates in the canvas based on the row and column
        x = (columna - 1) * 500 // 3 + 500 // 6 
        y = (fila - 1) * 500 // 3 + 500 // 6
        
        # Draw the figure on the board
        self.dibujar_figura(x, y)
        
        # Close the coordinates window
        self.ventana_coordenadas.destroy()

    def dibujar_figura(self, x, y):
        # Crear una nueva imagen con fondo blanco
        imagen_nueva = Image.new('RGB', (50, 50), "white")
        draw = ImageDraw.Draw(imagen_nueva)

        # Dibujar el símbolo en la imagen
        if self.simbolo_seleccionado == 'X':
            color = self.obtener_color_hexadecimal()
            draw.line((0, 0, 50, 50), fill=color, width=5)
            draw.line((0, 50, 50, 0), fill=color, width=5)
        elif self.simbolo_seleccionado == 'O':
            color = self.obtener_color_hexadecimal()
            draw.ellipse((5, 5, 45, 45), outline=color, width=5)
        elif self.simbolo_seleccionado == '*':
            color = self.obtener_color_hexadecimal()
            draw.polygon([(25, 5), (45, 45), (5, 25), (45, 25), (5, 45)], outline=color, width=5)
        elif self.simbolo_seleccionado == '^':
            color = self.obtener_color_hexadecimal()
            draw.polygon([(5, 45), (25, 5), (45, 45)], outline=color, width=5)

        # Convertir la imagen a un objeto PhotoImage de Tkinter
        imagen_seleccionada = ImageTk.PhotoImage(imagen_nueva)

        # Crear una nueva imagen en el lienzo con la imagen seleccionada
        imagen_id = self.lienzo.create_image(x, y, image=imagen_seleccionada)
        self.imagenes_en_lienzo.append(imagen_id)  # Agregar el identificador de la imagen al registro

    def obtener_color_hexadecimal(self):
        if self.simbolo_seleccionado == 'X':
            return "#FF0000"  # Color rojo
        elif self.simbolo_seleccionado == 'O':
            return "#00FF00"  # Color verde
        elif self.simbolo_seleccionado == '*':
            return "#0000FF"  # Color azul
        elif self.simbolo_seleccionado == '^':
            return "#FF00FF"  # Color magenta

    def seleccionar_color(self, color):
        print("Seleccionar color:", color)
        self.color_seleccionado = color

        # Solicitar coordenadas al usuario
        self.solicitar_coordenadas()

    def dibujar_tablero(self):
        cell_size = 500 // 3  # Calcula el tamaño de cada celda
        for i in range(1, 3):  # Solo necesitas dos líneas para dividir el tablero en tres
            # Dibujar líneas verticales
            self.lienzo.create_line(cell_size * i, 0, cell_size * i, 500, width=2)
            # Dibujar líneas horizontales
            self.lienzo.create_line(0, cell_size * i, 500, cell_size * i, width=2)

raiz = tk.Tk()
app = AplicacionPixelArt(raiz)
raiz.mainloop()
