import flet as ft
import numpy as np
import os

# Datos de entrenamiento
X = np.array([
    [1,1,1,1,1,1,0],  # 0
    [0,1,1,0,0,0,0],  # 1
    [1,1,0,1,1,0,1],  # 2
    [1,1,1,1,0,0,1],  # 3
    [0,1,1,0,0,1,1],  # 4
    [1,0,1,1,0,1,1],  # 5
    [1,0,1,1,1,1,1],  # 6
    [1,1,1,0,0,0,0],  # 7
    [1,1,1,1,1,1,1],  # 8
    [1,1,1,1,0,1,1],  # 9
])
X_bias = np.hstack((np.ones((X.shape[0], 1)), X))
D = np.array([
    [1,1,0],  # 0
    [1,0,0],  # 1
    [1,1,1],  # 2
    [1,0,1],  # 3
    [1,1,0],  # 4
    [1,0,1],  # 5
    [0,1,0],  # 6
    [0,0,1],  # 7
    [0,1,0],  # 8
    [0,0,0],  # 9
])

n_inputs = X_bias.shape[1]
n_outputs = D.shape[1]
expected_shape = (n_outputs, n_inputs)

# Función escalón
def step(x): return np.where(x > 0, 1, 0)

# Función para validar pesos
def pesos_validos(path, expected_shape):
    if not os.path.exists(path):
        return False
    try:
        W = np.loadtxt(path)
        return W.shape == expected_shape
    except:
        return False

# Función para entrenar red
def entrenar_red():
    eta = 0.1
    max_epochs = 100
    W = np.random.uniform(-0.5, 0.5, size=expected_shape)
    for epoch in range(max_epochs):
        total_errors = 0
        for i in range(X_bias.shape[0]):
            x = X_bias[i]
            d = D[i]
            y = step(W @ x)
            e = d - y
            total_errors += np.sum(np.abs(e))
            for j in range(n_outputs):
                W[j] += eta * e[j] * x
        if total_errors == 0:
            break
    np.savetxt("pesos_entrenados.txt", W)
    return W

# Codificación de segmentos
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

# Colores para display
ON = "#FF3B3B"
OFF = "#220000"

def crear_segmento(horizontal=True):
    return ft.Container(
        width=60 if horizontal else 10,
        height=10 if horizontal else 60,
        bgcolor=OFF,
        border_radius=4,
        margin=ft.margin.only(top=1, bottom=1),
    )

# -----------------------------
def main(page: ft.Page):
    page.title = "Display 7 segmentos con Perceptrón"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.DARK

    etiquetas = ["≤ 5", "Par", "Primo"]
    resultado_textos = [ft.Text("", size=20) for _ in range(3)]

    segmentos_visuales = {
        "a": crear_segmento(True),
        "b": crear_segmento(False),
        "c": crear_segmento(False),
        "d": crear_segmento(True),
        "e": crear_segmento(False),
        "f": crear_segmento(False),
        "g": crear_segmento(True),
    }

    display = ft.Column([
        ft.Row([ft.Container(width=15), segmentos_visuales["a"], ft.Container(width=15)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([segmentos_visuales["f"], ft.Container(width=50), segmentos_visuales["b"]], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.Container(width=15), segmentos_visuales["g"], ft.Container(width=15)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([segmentos_visuales["e"], ft.Container(width=50), segmentos_visuales["c"]], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.Container(width=15), segmentos_visuales["d"], ft.Container(width=15)], alignment=ft.MainAxisAlignment.CENTER),
    ])

    dropdown = ft.Dropdown(
        label="Selecciona un número (0–9)",
        options=[ft.dropdown.Option(str(i)) for i in range(10)],
        width=250
    )

    def on_number_change(e):
        num = int(e.control.value)
        seg = segmentos[num]
        x = [1] + seg
        if pesos_validos("pesos_entrenados.txt", expected_shape):
            W = np.loadtxt("pesos_entrenados.txt")
            y = step(W @ x)

            # Actualizar segmentos
            mapa = ["a", "b", "c", "d", "e", "f", "g"]
            for i in range(7):
                segmentos_visuales[mapa[i]].bgcolor = ON if seg[i] else OFF

            for i in range(3):
                resultado_textos[i].value = f"¿{etiquetas[i]}? {'✅' if y[i] else '❌'}"
            page.update()
        else:
            for i in range(3):
                resultado_textos[i].value = "¡Entrena la red primero!"
            page.update()

    dropdown.on_change = on_number_change

    def on_train_click(e):
        entrenar_red()
        page.snack_bar = ft.SnackBar(ft.Text("Red entrenada y pesos guardados ✅"))
        page.snack_bar.open = True
        page.update()

    btn_entrenar = ft.ElevatedButton("Entrenar red", on_click=on_train_click)

    page.add(
        ft.Text("Perceptrón con Display de 7 Segmentos", size=24, weight="bold"),
        dropdown,
        btn_entrenar,
        ft.Divider(),
        ft.Text("Display de 7 Segmentos", size=20),
        display,
        ft.Divider(),
        ft.Text("Respuestas de las neuronas:", size=20),
        *resultado_textos
    )

if __name__ == "__main__":
    ft.app(target=main)
