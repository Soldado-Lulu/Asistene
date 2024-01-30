import openai
import speech_recognition as sr
import pyttsx3
import datetime
from ReconocimientoVoz.ReconocimientoVoz import GrabadorAudio

class AsistenteSentinel:

    def __init__(self, api_key):
        openai.api_key = api_key
        self.engine = pyttsx3.init()
        self.usuarios = {}
        self.voices = self.engine.getProperty('voices')
        self.configurar_voz_asistente()

    def audio_a_texto(self, filename):
        recogizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = recogizer.record(source)
        try:
            return recogizer.recognize_google(audio, language="es")
        except:
            print("No se que paso")

    def capturar_nombre_usuario(self):
        self.configurar_voz_asistente()
        self.hablar_texto("Hola, me llamo senti nel, tu asistente de voz. ¿Cuál es tu nombre?")
        nombre_usuario = None
        while nombre_usuario is None:
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                audio = recognizer.listen(source)
                try:
                    nombre_usuario = recognizer.recognize_google(audio, language="es")
                    nombre_usuario = nombre_usuario.lower()
                    if nombre_usuario not in self.usuarios:
                        self.usuarios[nombre_usuario] = {'nombre': nombre_usuario, 'historial': []}
                    self.hablar_texto(f"¡Hola, {nombre_usuario}! ¿En qué puedo ayudarte?")
                except Exception as e:
                    self.hablar_texto("No pude entender tu nombre. Por favor, inténtalo de nuevo.")
        return nombre_usuario

    def configurar_voz_asistente(self, desired_voice_id=None):
        if desired_voice_id:
            self.engine.setProperty('voice', desired_voice_id)
        else:
            # Configurar la voz predeterminada si no se proporciona una voz específica
            default_voice = self.voices[2]  # Puedes seleccionar la primera voz de la lista
            self.engine.setProperty('voice', default_voice.id)

    def generar_respuesta(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response["choices"][0]["text"]

    def hablar_texto(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def obtener_hora(self):
        # Obtén la hora actual
        hora_actual = datetime.datetime.now().strftime("%H:%M")
        return f"La hora actual es {hora_actual}"

    def obtener_hora_y_fecha(self):
        # Obtén la hora y la fecha actual
        ahora = datetime.datetime.now()
        hora_actual = ahora.strftime("%H:%M")
        fecha_actual = ahora.strftime("%d/%m/%Y")
        return f"La hora actual es {hora_actual} y la fecha es {fecha_actual}"

    def iniciar(self):
        nombre_usuario = None
        while nombre_usuario is None:
            nombre_usuario = self.capturar_nombre_usuario()

        while True:
            print("Di 'Sentinel' para empezar la conversación")
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                audio = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio, language="es")
                    if transcription.lower() == "sentinel":
                        # Verificar si el usuario actual está registrado
                        if nombre_usuario not in self.usuarios:
                            self.hablar_texto(
                                "Lo siento, no estás registrado como usuario. Por favor, regístrate primero.")
                        else:
                            # record audio
                            filename = "input.wav"
                            print("En qué puedo ayudarte")
                            with sr.Microphone() as source:
                                recognizer = sr.Recognizer()
                                source.pause_threshold = 1
                                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                                with open(filename, "wb") as f:
                                    f.write(audio.get_wav_data())
                            # transcript audio to text
                            text = self.audio_a_texto(filename)
                            if text:
                                print(f"Usuario {nombre_usuario}: {text}")

                                # Agregar la conversación al historial del usuario
                                self.usuarios[nombre_usuario]['historial'].append(
                                    {'usuario': nombre_usuario, 'texto': text})

                                # Verificar si la pregunta es sobre la hora o la fecha
                                if "hora" in text.lower() and "fecha" in text.lower():
                                    respuesta = self.obtener_hora_y_fecha()
                                    print(f"Sentinel dice: {respuesta}")
                                    self.hablar_texto(respuesta)
                                elif "hora" in text.lower():
                                    respuesta_hora = self.obtener_hora()
                                    print(f"Sentinel dice: {respuesta_hora}")
                                    self.hablar_texto(respuesta_hora)
                                elif "fecha" in text.lower():
                                    respuesta_fecha = self.obtener_fecha()
                                    print(f"Sentinel dice: {respuesta_fecha}")
                                    self.hablar_texto(respuesta_fecha)
                                else:
                                    # Generar la respuesta
                                    response = self.generar_respuesta(text)
                                    print(f"Sentinel dice: {response}")

                                    # Leer la respuesta usando GPT-3
                                    self.hablar_texto(response)
                except Exception as e:
                    print("Error : {}".format(e))