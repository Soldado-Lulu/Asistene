from Sentinel import AsistenteSentinel
from ReconocimientoVoz.ReconocimientoVoz import GrabadorAudio
def main():
    api_key = "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"
    asistente = AsistenteSentinel(api_key)
    asistente.iniciar()

if __name__ == "__main__":
    main()
