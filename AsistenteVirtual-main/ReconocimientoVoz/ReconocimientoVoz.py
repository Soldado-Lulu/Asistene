import pyaudio
import numpy as np
import wave
import matplotlib.pyplot as plt
import time

class GrabadorAudio:
    def __init__(self, fs=22050, duration=4):
        self.fs = fs
        self.duration = duration
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def iniciar_grabacion(self):
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.fs,
                                      input=True,
                                      frames_per_buffer=1024)
        print("Comienza a hablar...")

    def detener_grabacion(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def guardar_audio(self, output_filename):
        frames = []
        for _ in range(0, int(self.fs * self.duration / 1024)):
            data = self.stream.read(1024)
            frames.append(data)

        self.detener_grabacion()

        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(frames))
        print(f"Archivo {output_filename} guardado exitosamente.")

    def cargar_audio(self, filename):
        with wave.open(filename, 'rb') as wf:
            self.fs = wf.getframerate()
            s = np.frombuffer(wf.readframes(-1), dtype=np.int16)

        self.d = np.max(np.abs(s))
        self.s = s.astype(float) / self.d

    def procesar_audio(self):
        lon = len(self.s)
        prom = np.sum(self.s * self.s) / lon
        umbral = 0.02
        y = np.array([0], dtype=float)

        for i in range(0, lon - 400, 400):
            seg = self.s[i:i + 400]
            e = np.sum(seg * seg) / 400
            if e > umbral * prom:
                y = np.concatenate((y, seg))

        with wave.open("senal_procesada.wav", 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes((y * self.d).astype(np.int16))

    def graficar_audio(self):
        plt.figure(figsize=(10, 6))
        plt.plot(np.arange(len(self.s)) / self.fs, self.s)
        plt.title("Señal de Voz")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.grid(True)
        plt.show()
        time.sleep(3)  # Esperar 5 segundos antes de cerrar la ventana de la gráfica
        plt.close()

if __name__ == "__main__":
    num_audios = 3  # Cantidad de audios que deseas grabar y procesar
    for i in range(num_audios):
        grabador = GrabadorAudio()
        grabador.iniciar_grabacion()
        print(f"Grabando audio {i + 1}...")
        time.sleep(grabador.duration)  # Grabar durante la duración especificada
        output_filename = f"Usuario_{i + 1}.wav"
        grabador.guardar_audio(output_filename)
        grabador.cargar_audio(output_filename)
        grabador.procesar_audio()
        grabador.graficar_audio()
