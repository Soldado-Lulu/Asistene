import sys
import socket
from datetime import datetime

class PortScanner:
    def __init__(self, target):
        self.target = target

    def scan_ports(self):
        print("*" * 50)
        print("Analizando el Objetivo: " + self.target)
        print("Análisis iniciado: " + str(datetime.now()))
        print("*" * 50)

        try:
            for port in range(1, 65536):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    print("El Puerto {} está abierto".format(port))
                s.close()

        except KeyboardInterrupt:
            print("\n Cerrando el Programa !!!")
            sys.exit()

        except socket.gaierror:
            print("\n El Nombre del host no puede ser resuelto!!!")
            sys.exit()

        except socket.error:
            print('\n Host No Responde!!!')
            sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python scanner.py <objetivo>")
    else:
        target = sys.argv[1]
        scanner = PortScanner(target)
        scanner.scan_ports()