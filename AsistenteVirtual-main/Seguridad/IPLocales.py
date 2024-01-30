import socket

class IPLocales:
    def __init__(self):
        self.local_ips = []

    def get_local_ips(self):
        hostname = socket.gethostname()
        self.local_ips.append(socket.gethostbyname(hostname))

        for interface in socket.if_nameindex():
            if interface[1] != 'lo':
                try:
                    ip = socket.gethostbyname_ex(socket.if_indextoname(interface[0]))[2]
                    self.local_ips.extend(ip)
                except socket.gaierror:
                    pass

        return self.local_ips

    def save_ips_to_file(self, filename):
        with open(filename, 'w') as file:
            for ip in self.local_ips:
                file.write(ip + '\n')




if __name__ == "__main__":
    ip_detector = IPLocales()
    ips = ip_detector.get_local_ips()
    filename = "../../Seguridad/local_ips.txt"
    ip_detector.save_ips_to_file(filename)

    print("Direcciones IP obtenidas:")
    for ip in ips:
        print(ip)
    print(f"Se han guardado las IPs en '{filename}'.")
    print("Proceso de recopilación y guardado completado.")