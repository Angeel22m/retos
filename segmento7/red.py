import flet as ft
import numpy as np

# -----------------------------
# Cargar pesos entrenados
W = np.loadtxt("pesos_entrenados.txt")

# Codificación en 7 segmentos
segmentos = [
    [1,1,1,1,1,1,0],  # 0
    [0,1,1,0,0,0,0],  # 1
    [1,1,0,1,1,0,1],  # 2
    [1,1,1,1,0,0,1],  # 3
    [0,1,1,0,0,1,1],  # 4
    [1,0,1,1,0,1,1],  # 5
    [1,0,1,1,1,1,1],  # 6
    [1,1,1,0,0,0,0],  # 7
    [1,1,1,1,1,1,1],  # 8
    [1,1,1,1,0,1,1]   # 9
]

# Función escalón
def step(x): return np.where(x > 0, 1, 0)

# -----------------------------
# Colores para segmentos
ON = "#FF3B3B"
OFF = "#220000"

# Crear segmento con estilo y animación
def crear_segmento(horizontal=True):
    return ft.Container(
        width=60 if horizontal else 10,
        height=10 if horizontal else 60,
        bgcolor=OFF,
        border_radius=5,
        animate=ft.animation.Animation(300, "easeOut"),
        shadow=ft.BoxShadow(blur_radius=4, color="#440000", spread_radius=1)
    )

# Flet app principal
def main(page: ft.Page):
    page.title = "Display 7 segmentos con Perceptrón"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30
    page.theme_mode = ft.ThemeMode.DARK  # Tema oscuro

    etiquetas = ["≤ 5", "Par", "Primo"]
    resultado_textos = [ft.Text("", size=20) for _ in range(3)]

    # Crear segmentos visuales
    segmentos_visuales = {
        "a": crear_segmento(horizontal=True),
        "b": crear_segmento(horizontal=False),
        "c": crear_segmento(horizontal=False),
        "d": crear_segmento(horizontal=True),
        "e": crear_segmento(horizontal=False),
        "f": crear_segmento(horizontal=False),
        "g": crear_segmento(horizontal=True),
    }

    # Layout del display 7 segmentos
    display = ft.Column([
        ft.Row([ft.Container(width=10), segmentos_visuales["a"]]),
        ft.Row([
            segmentos_visuales["f"],
            ft.Container(width=60),
            segmentos_visuales["b"]
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([ft.Container(width=10), segmentos_visuales["g"]]),
        ft.Row([
            segmentos_visuales["e"],
            ft.Container(width=60),
            segmentos_visuales["c"]
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([ft.Container(width=10), segmentos_visuales["d"]])
    ])

    # Dropdown para elegir número
    dropdown = ft.Dropdown(
        label="Selecciona un número (0–9)",
        options=[ft.dropdown.Option(str(i)) for i in range(10)],
        width=250
    )

    def on_number_change(e):
        num = int(e.control.value)
        seg = segmentos[num]
        x = [1] + seg  # Bias + segmentos
        y = step(W @ x)

        # Actualizar colores segmentos
        mapa = ["a", "b", "c", "d", "e", "f", "g"]
        for i in range(7):
            nombre = mapa[i]
            segmentos_visuales[nombre].bgcolor = ON if seg[i] else OFF

        # Actualizar respuestas neuronas
        for i in range(3):
            resultado_textos[i].value = f"¿{etiquetas[i]}? {'✅' if y[i] else '❌'}"

        page.update()

    dropdown.on_change = on_number_change

    # Añadir controles a la página
    page.add(
        ft.Text("Perceptrón con Display de 7 Segmentos", size=24, weight="bold"),
        dropdown,
        ft.Divider(),
        ft.Text("Display de 7 Segmentos", size=20),
        display,
        ft.Divider(),
        ft.Text("Respuestas de las neuronas:", size=20),
        *resultado_textos
    )

if __name__ == "__main__":
    ft.app(target=main)
