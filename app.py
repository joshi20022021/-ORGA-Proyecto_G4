import tkinter as tk
from tkinter import filedialog, messagebox
from analyzer.analyzer import analyze_file
import re
import os
from ComSerial import serial


class TotitoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Totito App")
        self.root.configure(background="#f0f0f0")

        # Matriz para representar el tablero 3x3
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]

        # Estilos para los botones de las figuras
        figura_btn_style = {
            "bg": "#d9d9d9",
            "activebackground": "#bfbfbf",
            "fg": "black",  # Color del texto
            "font": ("Arial", 14),  # Fuente y tamaño del texto
            "pady": 5,  # Padding vertical
            "padx": 10,  # Padding horizontal
        }

        # Canvas para dibujar el tablero
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack()
        self.dibujar_tablero()

        # Botones para elegir las figuras
        self.botones_figuras = []
        self.figuras = {"X": "✕", "O": "◯", "Estrella": "☆", "Triangulo": "△"}
        for figura, caracter in self.figuras.items():
            btn = tk.Button(
                root,
                text=caracter,
                command=lambda f=figura: self.elegir_figura(f),
                **figura_btn_style,
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.botones_figuras.append(btn)

        # Botón para cargar desde archivo
        btn_cargar = tk.Button(
            root,
            text="Cargar desde archivo",
            command=self.cargar_desde_archivo,
            padx=10,
            pady=5,
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
        )
        btn_cargar.pack(pady=10)

        # Crear el área de texto
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(pady=10)
        self.text_area = tk.Text(self.text_frame, width=30, height=10)
        self.text_area.pack()

        # Botón para enviar el texto y actualizar el tablero
        btn_enviar = tk.Button(
            root,
            text="Enviar texto",
            padx=10,
            pady=5,
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
        )
        btn_enviar.pack(pady=10)

        # Crear la barra de menú
        self.crear_menu()

    def nuevo_archivo(self):
        # Eliminar todas las figuras del tablero
        items = self.canvas.find_all()
        for item in items:
            tags = self.canvas.gettags(item)
            if "figura" in tags:
                self.canvas.delete(item)
        # Reiniciar la matriz del tablero
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        # Limpiar el área de texto
        self.text_area.delete(1.0, tk.END)

    def guardar_como(self):
        # Aquí puedes implementar la funcionalidad para guardar como archivo
        pass

    def guardar(self):
        # Aquí puedes implementar la funcionalidad para guardar archivo
        pass

    def imprimir(self):
        # Aquí puedes implementar la funcionalidad para imprimir
        pass

    def salir(self):
        self.root.quit()

    def acerca_de(self):
        # Aquí puedes mostrar información sobre la aplicación
        pass

    def crear_menu(self):
        # Crear la barra de menú
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Menú Archivo
        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(
            label="Abrir archivo", command=self.cargar_desde_archivo
        )
        archivo_menu.add_command(label="Nuevo archivo", command=self.nuevo_archivo)
        archivo_menu.add_command(label="Guardar como", command=self.guardar_como)
        archivo_menu.add_command(label="Guardar", command=self.guardar)
        archivo_menu.add_command(label="Imprimir", command=self.imprimir)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.salir)

        # Menú Ayuda
        ayuda_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de...", command=self.acerca_de)

    def dibujar_tablero(self):
        # Dibuja las líneas del tablero
        for i in range(1, 3):
            self.canvas.create_line(100 * i, 0, 100 * i, 300)  # Líneas verticales
            self.canvas.create_line(0, 100 * i, 300, 100 * i)  # Líneas horizontales

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

        # Estilos de texto
        label_style = {"bg": "#f0f0f0", "fg": "black", "font": ("Arial", 12)}

        tk.Label(ventana, text="Fila (1-3):", **label_style).grid(
            row=0, column=0, padx=5, pady=5
        )
        tk.Label(ventana, text="Columna (1-3):", **label_style).grid(
            row=1, column=0, padx=5, pady=5
        )
        tk.Label(ventana, text="Color:", **label_style).grid(
            row=2, column=0, padx=5, pady=5
        )

        entry_style = {"bg": "white", "fg": "black", "font": ("Arial", 12)}
        entry_fila = tk.Entry(ventana, **entry_style)
        entry_fila.grid(row=0, column=1, padx=5, pady=5)
        entry_columna = tk.Entry(ventana, **entry_style)
        entry_columna.grid(row=1, column=1, padx=5, pady=5)

        dropdown_style = {"bg": "#f0f0f0", "fg": "black", "font": ("Arial", 12)}
        colores = ["cyan", "magenta", "amarillo", "negro"]
        color_variable = tk.StringVar(ventana)
        color_variable.set(colores[0])
        dropdown_color = tk.OptionMenu(ventana, color_variable, *colores)
        dropdown_color.config(**dropdown_style)
        dropdown_color.grid(row=2, column=1, padx=5, pady=5)

        button_style = {
            "bg": "#007bff",
            "fg": "white",
            "font": ("Arial", 12),
            "activebackground": "#0056b3",
        }
        btn_confirmar = tk.Button(
            ventana,
            text="Confirmar",
            command=lambda: self.dibujar_figura(
                figura, entry_fila.get(), entry_columna.get(), color_variable.get()
            ),
            **button_style,
        )
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
            figura = figura.upper()  # Convertir la figura a mayúsculas

            # Mapear "negro" a "black"
            if color == "negro":
                color = "black"
            # Mapear "amarillo" a "yellow"
            elif color == "amarillo":
                color = "yellow"

            if figura == "X":
                line1 = self.canvas.create_line(
                    x - 40, y - 40, x + 40, y + 40, fill=color, width=2
                )
                line2 = self.canvas.create_line(
                    x - 40, y + 40, x + 40, y - 40, fill=color, width=2
                )
                # Agregar etiqueta "figura" a las líneas
                self.canvas.addtag_withtag("figura", line1)
                self.canvas.addtag_withtag("figura", line2)
            elif figura == "O":
                oval = self.canvas.create_oval(
                    x - 40, y - 40, x + 40, y + 40, outline=color, width=2
                )
                # Agregar etiqueta "figura" al óvalo
                self.canvas.addtag_withtag("figura", oval)
            elif figura == "ESTRELLA":
                puntos = [
                    x,
                    y - 50,
                    x - 20,
                    y - 20,
                    x - 50,
                    y,
                    x - 20,
                    y + 20,
                    x,
                    y + 50,
                    x + 20,
                    y + 20,
                    x + 50,
                    y,
                    x + 20,
                    y - 20,
                ]
                polygon = self.canvas.create_polygon(puntos, fill=color, outline=color)
                # Agregar etiqueta "figura" al polígono
                self.canvas.addtag_withtag("figura", polygon)
            elif figura == "TRIANGULO":
                puntos = [x, y - 50, x - 50, y + 50, x + 50, y + 50]
                polygon = self.canvas.create_polygon(puntos, fill=color, outline=color)
                # Agregar etiqueta "figura" al polígono
                self.canvas.addtag_withtag("figura", polygon)

            # Actualizar la matriz del tablero
            self.tablero[fila - 1][columna - 1] = figura
        except ValueError:
            messagebox.showerror(
                "Error", "Ingrese valores numéricos para fila y columna."
            )

    def colocar_figura(self, figura, fila, columna, color):
        # Coloca la figura en el tablero en las coordenadas especificadas
        x = columna * 100 - 50
        y = fila * 100 - 50
        if figura == "X":
            self.canvas.create_line(x - 40, y - 40, x + 40, y + 40, fill=color, width=2)
            self.canvas.create_line(x - 40, y + 40, x + 40, y - 40, fill=color, width=2)
        elif figura == "O":
            self.canvas.create_oval(
                x - 40, y - 40, x + 40, y + 40, outline=color, width=2
            )
        elif figura == "Estrella":
            puntos = [
                x,
                y - 50,
                x - 20,
                y - 20,
                x - 50,
                y,
                x - 20,
                y + 20,
                x,
                y + 50,
                x + 20,
                y + 20,
                x + 50,
                y,
                x + 20,
                y - 20,
            ]
            self.canvas.create_polygon(puntos, fill=color, outline=color)
        elif figura == "Triangulo":
            puntos = [x, y - 50, x - 50, y + 50, x + 50, y + 50]
            self.canvas.create_polygon(puntos, fill=color, outline=color)

        # Actualiza la matriz del tablero
        self.tablero[fila - 1][columna - 1] = figura
        

    def cargar_desde_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos .olc", "*.olc")])
        if archivo:
            try:
                with open(archivo, "r") as file:
                    contenido = file.read()
                    self.text_area.delete(
                        1.0, tk.END
                    )  # Limpiar el contenido actual del TextArea
                    self.text_area.insert(tk.END, contenido)

                prints = analyze_file(archivo) 
                serial(prints)
                messagebox.showerror("Error", prints)
                
                for print in prints:
                    for instruction in print.instructions:
                        self.dibujar_figura(
                            instruction.shape,
                            instruction.row,
                            instruction.column,
                            instruction.color,
                        )

            except FileNotFoundError:
                messagebox.showerror("Error", "El archivo no se encontró.")

    def cargar_desde_texto(self):
        # Obtener el contenido del TextArea
        contenido = self.text_area.get("1.0", tk.END)

        # Crear un archivo .olc y escribir el contenido
        try:
            with open("archivo_temporal.olc", "w") as file:
                file.write(contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el archivo temporal: {e}")
            return

        # Abrir el archivo automáticamente
        try:
            os.startfile("archivo_temporal.olc")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo temporal: {e}")

        # Cargar el contenido del archivo en el tablero
        self.cargar_desde_archivo()


if __name__ == "__main__":
    root = tk.Tk()
    app = TotitoApp(root)

    root.mainloop()
