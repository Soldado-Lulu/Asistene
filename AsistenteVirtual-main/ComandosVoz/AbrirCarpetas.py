import os
import speech_recognition as sr

import os
import urllib.parse
import shutil


def abrir_carpeta(ruta_carpeta):
    if os.path.exists(ruta_carpeta):
        os.system(f'explorer "{ruta_carpeta}"')
    else:
        print("La carpeta no existe.")


def descargar_archivo(url, carpeta_destino):
    try:
        respuesta = urllib.request.urlopen(url)
        nombre_archivo = os.path.basename(url)
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
        with open(ruta_archivo, 'wb') as archivo_local:
            archivo_local.write(respuesta.read())
        print(f"Archivo descargado: {nombre_archivo}")
        return ruta_archivo
    except Exception as e:
        print("Error al descargar el archivo:", e)
        return None


def organizar_archivos(ruta_archivo, carpeta_destino):
    extension = os.path.splitext(ruta_archivo)[1]
    if not extension:
        extension = "Otros"
    carpeta_extension = os.path.join(carpeta_destino, extension[1:])

    if not os.path.exists(carpeta_extension):
        os.makedirs(carpeta_extension)

    nuevo_ruta_archivo = os.path.join(carpeta_extension, os.path.basename(ruta_archivo))
    shutil.move(ruta_archivo, nuevo_ruta_archivo)
    print(f"Archivo movido a la carpeta: {carpeta_extension}")


if __name__ == "__main__":
    ruta_descargas = os.path.join(os.path.expanduser('~'), 'Descargas')
    abrir_carpeta(ruta_descargas)

    url = input("Introduce la URL del archivo a descargar: ")
    archivo_descargado = descargar_archivo(url, ruta_descargas)

    if archivo_descargado:
        organizar_archivos(archivo_descargado, ruta_descargas)


def escuchar():
    reconocedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Di una carpeta para abrir:")
        audio = reconocedor.listen(source)

    try:
        texto = reconocedor.recognize_google(audio, language="es")
        return texto
    except sr.UnknownValueError:
        print("No pude entender lo que dijiste.")
        return ""