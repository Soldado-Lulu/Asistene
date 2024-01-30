import tkinter as tk
import speech_recognition as sr
import threading
from Seguridad.IPLocales import IPLocales
# Función para iniciar y detener la grabación
def toggle_recording():
    global listening
    if not listening:
        listening = True
        start_recording()
        boton_inicio.config(text="Detener")
    else:
        listening = False
        stop_recording()
        boton_inicio.config(text="Iniciar")
def ObtenerIps():
    ip_detector = IPLocales()
    ips = ip_detector.get_local_ips()
    print("Direcciones IP locales:")
    for ip in ips:
        print(ip)
# Función para iniciar la grabación
def start_recording():
    global recognizer, microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        while listening:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                cuadro_texto.delete(1.0, tk.END)
                cuadro_texto.insert(tk.END, text)
                if "Obtener IP de la red" in text.lower():
                    ObtenerIps()
            except sr.UnknownValueError:
                cuadro_texto.delete(1.0, tk.END)
                cuadro_texto.insert(tk.END, "No se detectó ninguna entrada de voz.")
            except sr.RequestError as e:
                cuadro_texto.delete(1.0, tk.END)
                cuadro_texto.insert(tk.END, f"Error al realizar la solicitud: {e}")

# Función para detener la grabación
def stop_recording():
    global listening
    listening = False

# Función específica a ejecutar cuando se detecta la palabra clave
def funcion_especifica():
    cuadro_texto.delete(1.0, tk.END)
    cuadro_texto.insert(tk.END, "Palabra clave detectada. Ejecutando función específica.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Reconocimiento de Voz")

# Inicializar objetos de reconocimiento de voz y micrófono
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Bandera para controlar la grabación
listening = False

# Crear un cuadro de texto para mostrar el resultado
cuadro_texto = tk.Text(ventana, height=5, width=40)
cuadro_texto.pack(padx=10, pady=10)

# Botón para iniciar y detener la grabación
boton_inicio = tk.Button(ventana, text="Iniciar", command=toggle_recording)
boton_inicio.pack()

# Iniciar la ventana principal
ventana.mainloop()
