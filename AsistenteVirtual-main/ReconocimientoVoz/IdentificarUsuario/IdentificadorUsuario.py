from scipy.spatial import distance
from python_speech_features import mfcc
import numpy as np
import os
import scipy.io.wavfile as wav

class BiometricVoiceVerification:
    def __init__(self):
        self.users = {}

    def registrar_usuario(self, nombre, grabaciones):
        mfccs = [self.extraer_caracteristicas(grabacion) for grabacion in grabaciones]
        self.users[nombre] = mfccs

    def verificar_usuario(self, entrada_de_voz, umbral=10.0):
        entrada_mfcc = self.extraer_caracteristicas(entrada_de_voz)
        for nombre, mfccs in self.users.items():
            distancias = [distance.euclidean(entrada_mfcc, registro) for registro in mfccs]
            distancia_promedio = np.mean(distancias)
            if distancia_promedio < umbral:
                return nombre
        return "Desconocido"

    def extraer_caracteristicas(self, archivo_audio):
        # Cargar el archivo de audio y extraer las características MFCC
        rate, signal = wav.read(archivo_audio)
        mfccs = mfcc(signal, rate)

        # Retorna las características MFCC como un arreglo
        return mfccs

# Ejemplo de uso:
if __name__ == "__main__":
    biometric_verification = BiometricVoiceVerification()

    # Registro de usuarios (nombre, lista de grabaciones de voz)
    biometric_verification.registrar_usuario("Ema", ["ema1.wav", "ema2.wav"])
    biometric_verification.registrar_usuario("Jose", ["jose1.wav", "jose2.wav"])

    # Verificación de usuario
    entrada_de_voz = "input.wav"
    usuario_verificado = biometric_verification.verificar_usuario(entrada_de_voz, umbral=15.0)

    if usuario_verificado != "Desconocido":
        print(f"Usuario verificado: {usuario_verificado}")
    else:
        print("Usuario desconocido")
