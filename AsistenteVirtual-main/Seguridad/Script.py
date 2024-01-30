import socket
class PortScanner:
    def __init__(self, ip_list, portlist):
        self.ip_list = ip_list
        self.portlist = portlist

    def scan_ports(self):
        for ip in self.ip_list:
            for port in self.portlist:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((ip, port))
                print(f"IP: {ip}, Port: {port}, Result: {result}")
                sock.close()

if __name__ == "__main__":
    try:
        with open('local_ips.txt', 'r') as file:
            ips = file.read().splitlines()
    except FileNotFoundError:
        print("El archivo 'ips.txt' no se encuentra.")

    portlist = [21, 40, 23, 80, 355]

    if ips:
        scanner = PortScanner(ips, portlist)
        scanner.scan_ports()
