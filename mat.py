import random
import tkinter as tk


class MiniMate:

    def __init__(self, root):
        self.root = root

        # Ventana sin barra superior, pequeña y en esquina inferior izquierda
        self.root.overrideredirect(True)

        ancho = 200
        alto = 64

        pantalla_alto = self.root.winfo_screenheight()
        margen_x = 12
        margen_y = 48

        pos_x = margen_x
        pos_y = pantalla_alto - alto - margen_y

        self.root.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        # Estilo oscuro tipo terminal/editor
        bg_color = "#1e1e1e"
        fg_color = "#cccccc"
        accent_color = "#2d2d2d"
        border_color = "#3c3c3c"

        self.root.configure(bg=border_color)
        inner = tk.Frame(root, bg=bg_color)
        inner.pack(fill="both", expand=True, padx=1, pady=1)

        self.nivel = 1
        self.racha = 0
        self.respuesta_actual = 0

        # Fila superior: operación + nivel y racha
        top_frame = tk.Frame(inner, bg=bg_color)
        top_frame.pack(fill="x", padx=8, pady=(6, 2))

        self.lbl_operacion = tk.Label(
            top_frame,
            text="",
            font=("Consolas", 10, "bold"),
            fg="#569cd6",
            bg=bg_color,
        )
        self.lbl_operacion.pack(side="left")

        self.lbl_estado = tk.Label(
            top_frame,
            text="L1 | 0",
            font=("Consolas", 8),
            fg="#6a9955",
            bg=bg_color,
        )
        self.lbl_estado.pack(side="right")

        # Fila inferior: input discreto
        self.entry = tk.Entry(
            inner,
            font=("Consolas", 10),
            bg=accent_color,
            fg=fg_color,
            insertbackground=fg_color,
            relief="flat",
            justify="center",
        )
        self.entry.pack(fill="x", padx=8, pady=(2, 6), ipady=2)

        # Atajos de teclado
        self.entry.bind("<Return>", self.verificar)
        self.entry.bind("<Control-z>", lambda e: self.root.destroy())
        self.entry.bind("<Control-Z>", lambda e: self.root.destroy())
        self.entry.bind("<F1>", lambda e: self.cambiar_nivel(1))
        self.entry.bind("<F2>", lambda e: self.cambiar_nivel(2))
        self.entry.bind("<F3>", lambda e: self.cambiar_nivel(3))

        # Arrastre desde fondo o etiquetas
        for widget in (inner, top_frame, self.lbl_operacion, self.lbl_estado):
            widget.bind("<ButtonPress-1>", self.iniciar_arrastre)
            widget.bind("<B1-Motion>", self.mover_ventana)

        self.nueva_pregunta()
        self.entry.focus_set()

    def iniciar_arrastre(self, event):
        self._offset_x = event.x_root - self.root.winfo_x()
        self._offset_y = event.y_root - self.root.winfo_y()

    def mover_ventana(self, event):
        x = event.x_root - self._offset_x
        y = event.y_root - self._offset_y
        self.root.geometry(f"+{x}+{y}")

    def cambiar_nivel(self, nuevo_nivel, msg=None, color="#6a9955"):
        if nuevo_nivel in (1, 2, 3):
            self.nivel = nuevo_nivel
            self.racha = 0
            texto_estado = msg if msg else f"L{self.nivel} | 0"
            self.lbl_estado.config(text=texto_estado, fg=color)
            self.nueva_pregunta()

    def generar_operacion(self):
        if self.nivel == 1:
            op = random.choice(["+", "-", "*"])
            if op == "+":
                a, b = random.randint(5, 35), random.randint(5, 35)
                return f"{a} + {b} =", a + b
            elif op == "-":
                a = random.randint(10, 45)
                b = random.randint(1, a - 1)
                return f"{a} - {b} =", a - b
            else:
                a, b = random.randint(2, 9), random.randint(2, 9)
                return f"{a} * {b} =", a * b

        elif self.nivel == 2:
            op = random.choice(["+", "-", "*"])
            if op == "+":
                a, b = random.randint(35, 180), random.randint(25, 150)
                return f"{a} + {b} =", a + b
            elif op == "-":
                a = random.randint(60, 250)
                b = random.randint(15, a - 10)
                return f"{a} - {b} =", a - b
            else:
                a, b = random.randint(6, 18), random.randint(4, 15)
                return f"{a} * {b} =", a * b

        else:  # Nivel 3: más complejas + divisiones exactas simples
            op = random.choice(["+", "-", "*", "/"])
            if op == "+":
                a, b = random.randint(150, 650), random.randint(120, 550)
                return f"{a} + {b} =", a + b
            elif op == "-":
                a = random.randint(250, 900)
                b = random.randint(80, a - 50)
                return f"{a} - {b} =", a - b
            elif op == "*":
                a, b = random.randint(12, 28), random.randint(6, 19)
                return f"{a} * {b} =", a * b
            else:  # División exacta simple
                divisor = random.randint(2, 12)
                cociente = random.randint(2, 15)
                dividendo = divisor * cociente
                return f"{dividendo} / {divisor} =", cociente

    def nueva_pregunta(self):
        texto_op, resultado = self.generar_operacion()
        self.respuesta_actual = resultado
        self.lbl_operacion.config(text=texto_op)
        self.entry.delete(0, tk.END)

    def verificar(self, event=None):
        texto = self.entry.get().strip()
        if not texto:
            return

        # Comandos rápidos para cambiar de nivel: /1, /2, /3
        if texto in ("/1", "/2", "/3"):
            lvl = int(texto[1])
            self.cambiar_nivel(lvl, msg=f"L{lvl} | 0", color="#569cd6")
            return

        try:
            valor = int(texto)
        except ValueError:
            self.entry.delete(0, tk.END)
            return

        if valor == self.respuesta_actual:
            self.racha += 1
            self.lbl_estado.config(text=f"L{self.nivel} | +{self.racha}", fg="#4ec9b0")
            self.nueva_pregunta()
        else:
            self.racha = 0
            self.lbl_estado.config(text=f"L{self.nivel} | err", fg="#f44747")
            self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniMate(root)
    root.mainloop()