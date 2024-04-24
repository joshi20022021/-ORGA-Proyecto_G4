import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os

class AplicacionPixelArt:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Aplicación de Pixel Art")
        self.raiz.bind("<Configure>", self.actualizar_tamanio)

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
            },
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

        # Botón para abrir archivo
        self.boton_abrir_archivo = tk.Button(self.barra_lateral, text="Abrir archivo", command=self.abrir_archivo, **{**self.estilo["boton"], **self.estilo["boton_cyan"]})
        self.boton_abrir_archivo.grid(row=8, column=0, padx=5, pady=5, sticky="ew")

        # Lienzo de Pixel Art
        self.lienzo = tk.Canvas(self.contenedor, bg=self.estilo["lienzo"]["background"], width=500, height=500, highlightthickness=0)
        self.lienzo.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.lienzo.bind("<Button-1>", self.comenzar_arrastre)
        self.lienzo.bind("<B1-Motion>", self.actualizar_posicion)
        self.lienzo.bind("<ButtonRelease-1>", self.soltar_imagen)

        # Imagen y estado de juego
        self.imagen = Image.new("RGB", (3, 3), "white")
        self.dibujo = ImageDraw.Draw(self.imagen)
        self.jugador_actual = 'X'

        # Variables para el arrastre de la imagen
        self.simbolo_seleccionado = None
        self.color_seleccionado = '#000000'  # Por defecto, negro
        self.imagen_seleccionada = None
        self.posicion_inicial = None

        # Dibujar el tablero tipo "totito"
        self.dibujar_tablero()

        # Ajustar tamaño inicialmente
        self.actualizar_tamanio()

    def actualizar_tamanio(self, event=None):
        self.lienzo.config(width=self.raiz.winfo_width() * 0.75, height=self.raiz.winfo_height() * 0.75)

    def seleccionar_simbolo(self, simbolo):
        self.simbolo_seleccionado = simbolo
        self.cargar_imagen_simbolo()

    def cargar_imagen_simbolo(self):
        # Aquí deberías cargar imágenes de acuerdo al símbolo seleccionado
        # Se usa un ejemplo simple para representar el proceso
        if self.simbolo_seleccionado == 'X':
            self.imagen_seleccionada = Image.new('RGB', (50, 50), self.color_seleccionado)
        elif self.simbolo_seleccionado == 'O':
            self.imagen_seleccionada = Image.new('RGB', (50, 50), self.color_seleccionado)
        elif self.simbolo_seleccionado == '*':
            self.imagen_seleccionada = Image.new('RGB', (50, 50), self.color_seleccionado)
        elif self.simbolo_seleccionado == '^':
            self.imagen_seleccionada = Image.new('RGB', (50, 50), self.color_seleccionado)
        self.animacion_colocar_figura()

    def animacion_colocar_figura(self):
        if self.imagen_seleccionada:
            self.lienzo.image = ImageTk.PhotoImage(self.imagen_seleccionada)
            self.lienzo.create_image(250, 250, image=self.lienzo.image)  # Posición fija como ejemplo

    def seleccionar_color(self, color):
        self.color_seleccionado = color
        if self.simbolo_seleccionado:
            self.cargar_imagen_simbolo()

    def comenzar_arrastre(self, event):
        self.posicion_inicial = (event.x, event.y)

    def actualizar_posicion(self, event):
        if self.imagen_seleccionada:
            x = event.x - self.posicion_inicial[0] + 250  # 250 es una posición base fija
            y = event.y - self.posicion_inicial[1] + 250
            self.lienzo.delete("all")
            self.lienzo.create_image(x, y, image=self.lienzo.image)

    def soltar_imagen(self, event):
        # Aquí se puede implementar la lógica para fijar la imagen en el lienzo
        pass

    def dibujar_tablero(self):
        cell_size = 500 // 3  # Calcula el tamaño de cada celda
        for i in range(1, 3):  # Solo necesitas dos líneas para dividir el tablero en tres
            # Dibujar líneas verticales
            self.lienzo.create_line(cell_size * i, 0, cell_size * i, 500, width=2)
            # Dibujar líneas horizontales
            self.lienzo.create_line(0, cell_size * i, 500, cell_size * i, width=2)

    def abrir_archivo(self):
        ruta_archivo = filedialog.askopenfilename(initialdir=os.getcwd(), title="Seleccionar archivo de imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if ruta_archivo:
            imagen = Image.open(ruta_archivo)
            self.imagen_seleccionada = ImageTk.PhotoImage(imagen)
            self.animacion_colocar_figura()

raiz = tk.Tk()
app = AplicacionPixelArt(raiz)
raiz.mainloop()
