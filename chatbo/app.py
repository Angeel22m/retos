import flet as ft
from datetime import datetime
import time
import json
import os
import unicodedata
import difflib

# Ruta del archivo de historial
HISTORIAL_PATH = "chat.json"
import re

BASE_CONOCIMIENTO = {
    "que es el imc": "El IMC (Índice de Masa Corporal) es una fórmula que relaciona tu peso con tu estatura. Sirve para saber si estás en un rango de peso saludable.",
    
    "como calcular mi imc": "Para calcular tu IMC usa la fórmula: peso (kg) dividido por tu altura (m) al cuadrado. O dime tu peso y altura y yo lo calculo.",
    
    "como bajar de peso": "Para bajar de peso, enfócate en una alimentación balanceada, evita ultraprocesados, haz ejercicio regularmente y duerme bien.",
    
    "como perder grasa": "Para perder grasa corporal: mantén un déficit calórico, entrena con pesas y duerme mínimo 7-8 horas. La constancia es clave.",
    
    "como ganar masa muscular": "Ganar músculo requiere un buen plan de entrenamiento con pesas, comer suficiente proteína (1.6-2.2g/kg) y descansar adecuadamente.",
    
    "cuantas calorias debo consumir": "Depende de tu edad, sexo, peso, estatura y actividad física. En promedio, entre 1800 y 2500 kcal. Puedo ayudarte a estimarlas.",
    
    "que ejercicios recomiendas": "Ejercicios recomendados: caminar, correr, nadar, entrenar fuerza, andar en bici y yoga. Escoge lo que disfrutes y puedas mantener.",
    
    "cuanta agua debo tomar": "La recomendación general es entre 1.5 y 2.5 litros al día. Si haces ejercicio o hace calor, puede ser más.",
    
    "como tener habitos saludables": "Empieza con pequeños cambios: duerme bien, come más frutas y verduras, muévete a diario y evita el estrés crónico.",
    
    "que alimentos son buenos para la salud": "Frutas, verduras, granos integrales, legumbres, frutos secos y pescados grasos como el salmón son excelentes para la salud.",

    "cuanto debo dormir": "Lo ideal para adultos es dormir entre 7 y 9 horas cada noche. El descanso adecuado es vital para la salud y el rendimiento.",

    "que es una dieta equilibrada": "Una dieta equilibrada incluye frutas, verduras, proteínas magras, carbohidratos complejos, grasas saludables y suficiente agua.",

    "que es el deficit calorico": "Es consumir menos calorías de las que gastas. Es la base para perder grasa de forma sostenible.",

    "que son las calorias vacias": "Son calorías que vienen de alimentos con poco o ningún valor nutricional, como refrescos, dulces o comida chatarra.",

    "que pasa si no hago ejercicio": "La inactividad física puede aumentar el riesgo de enfermedades cardíacas, obesidad, ansiedad y otros problemas de salud.",

    "me puedes dar consejos para empezar": "Claro. Empieza por moverte más, tomar más agua, dormir bien, y evitar el exceso de azúcar. Ve paso a paso.",

    "que es el metabolismo": "El metabolismo es el conjunto de procesos que usa tu cuerpo para convertir lo que comes en energía.",
}


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto

def main(page: ft.Page):
    page.title = "ChatBoi"
    page.bgcolor = "#121212"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    chat_column = ft.ListView(
        expand=True,
        height=300,
        spacing=10,
        auto_scroll=True
    )

    user_input = ft.TextField(
        label="Escribe tu mensaje...",
        border_radius=15,
        bgcolor="#1e1e1e",
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.LIGHT_BLUE_ACCENT,
        filled=True,
        expand=True,
        on_submit=lambda e: responder(None),
    )

    # Crear burbuja con texto y hora
    def burbuja(texto, de_usuario=True, hora=None):
        hora = hora or datetime.now().strftime("%H:%M")
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    texto,
                    selectable=True,
                    color=ft.Colors.WHITE if de_usuario else ft.Colors.BLACK87,
                    size=16
                ),
                ft.Text(
                    hora,
                    size=10,
                    italic=True,
                    color=ft.Colors.GREY_500 if de_usuario else ft.Colors.GREY_700
                )
            ]),
            alignment=ft.alignment.top_right if de_usuario else ft.alignment.top_left,
            bgcolor="#0d47a1" if de_usuario else "#eeeeee",
            padding=10,
            border_radius=20,
            margin=5,
            width=300,
            shadow=ft.BoxShadow(
                blur_radius=6,
                color=ft.Colors.GREY_900 if de_usuario else ft.Colors.GREY_300
            )
        )

    # Guardar un mensaje al archivo JSON
    def guardar_mensaje(texto, de_usuario):
        historial = []
        if os.path.exists(HISTORIAL_PATH):
            with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
                try:
                    historial = json.load(f)
                except json.JSONDecodeError:
                    historial = []  # Archivo vacío o inválido
        historial.append({
            "texto": texto,
            "de_usuario": de_usuario,
            "hora": datetime.now().strftime("%H:%M")
        })
        with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=2, ensure_ascii=False)

    # Cargar mensajes del archivo JSON al iniciar
    def cargar_historial():
        if os.path.exists(HISTORIAL_PATH):
            with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
                try:
                    mensajes = json.load(f)
                except json.JSONDecodeError:
                    mensajes = []  # Archivo vacío o inválido
                for msg in mensajes:
                    chat_column.controls.append(
                        burbuja(msg["texto"], msg["de_usuario"], msg["hora"])
                    )

    # Al enviar mensaje
    def responder(e):
        mensaje = user_input.value.strip()
        if mensaje == "":
            return

        # Mostrar mensaje usuario y guardar
        chat_column.controls.append(burbuja(mensaje, de_usuario=True))
        guardar_mensaje(mensaje, de_usuario=True)

        # Mostrar "escribiendo..."
        escribiendo = ft.Text("Escribiendo...", color=ft.Colors.GREY_400, italic=True)
        chat_column.controls.append(escribiendo)
        page.update()

        time.sleep(1)

        chat_column.controls.remove(escribiendo)
        respuesta = procesar_mensaje(mensaje)
        chat_column.controls.append(burbuja(respuesta, de_usuario=False))
        guardar_mensaje(respuesta, de_usuario=False)

        user_input.value = ""
        page.update()
    
    # calcular IMC
    def calcular_imc(texto):
        # Buscar números asociados a "peso" y "altura"
        peso_match = re.search(r"peso\s*(de)?\s*(\d+\.?\d*)\s*kg", texto)
        altura_match = re.search(r"(altura|mido)\s*(de)?\s*(\d+\.?\d*)\s*m", texto)

        if peso_match and altura_match:
            peso = float(peso_match.group(2))
            altura = float(altura_match.group(3))
            imc = peso / (altura ** 2)
            categoria = (
                "bajo peso" if imc < 18.5 else
                "peso normal" if imc < 25 else
                "sobrepeso" if imc < 30 else
                "obesidad"
            )
            return f"Tu IMC es {imc:.2f}, lo que indica {categoria}."
        else:
            return "Para calcular el IMC, dime tu peso (en kg) y altura (en metros), por ejemplo: 'peso 70kg y mido 1.75m'."


    # Procesar el mensaje del usuario

    def procesar_mensaje(mensaje):
        mensaje = normalizar(mensaje.strip())  # <- usar la función de limpieza

    # IMC flexible: si contiene palabras clave y números, intenta calcularlo
        if any(p in mensaje for p in ["peso", "altura", "mido"]) and re.search(r"\d", mensaje):
            return calcular_imc(mensaje)

       
       # Coincidencia difusa con difflib
        mejor_pregunta = difflib.get_close_matches(mensaje, BASE_CONOCIMIENTO.keys(), n=1, cutoff=0.5)
        if mejor_pregunta:
            return BASE_CONOCIMIENTO[mejor_pregunta[0]]




        # Intentos simples de intención
        intenciones = {
            "saludo": ["hola", "buenas", "hey","hola, qué tal", "buen día", "buenas tardes", "buenas noches", "qué tal", "cómo estás", "cómo va todo", "qué hay"],
            "despedida": ["adios", "chao", "nos vemos", "hasta luego", "hasta pronto", "cuídate", "hasta la próxima"],
            "agradecimiento": ["gracias", "muchas gracias", "te lo agradezco", "agradecido", "agradecida"],
            "ayuda": ["ayuda", "necesito", "puedes", "cómo", "qué puedes hacer", "qué me recomiendas", "consejos", "ejercicios"]
        }

        for intent, palabras in intenciones.items():
            if any(p in mensaje for p in palabras):
                if intent == "saludo":
                    return "¡Hola! Soy tu asistente de salud. Pregúntame sobre tu peso ideal, IMC, consejos o ejercicios."
                elif intent == "despedida":
                    return "¡Hasta luego! Sigue cuidándote. 💪"
                elif intent == "agradecimiento":
                    return "¡Con gusto! Estoy para ayudarte."
                elif intent == "ayuda":
                    return "Puedo ayudarte a calcular tu IMC, darte consejos fitness y responder dudas sobre salud."

        return "Lo siento, no entendí eso. Pregúntame sobre salud, ejercicio o dime tu peso y altura para calcular tu IMC. 🤖"

    # Cargar historial al iniciar
    cargar_historial()

    # Interfaz
    page.add(
        chat_column,
        ft.Row(
            controls=[
                user_input,
                ft.IconButton(
                    icon=ft.Icons.SEND,
                    on_click=responder,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
                        icon_color=ft.Colors.WHITE
                    ),
                    tooltip="Enviar mensaje"
                )
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=10
        )
    )

ft.app(target=main)
