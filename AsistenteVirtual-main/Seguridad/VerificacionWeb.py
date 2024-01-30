import webbrowser
import pyperclip
import pyautogui
import time
from colorama import Fore, Style

class IPAnalysisTool:
    def __init__(self):
        self.documento = open('local_ips.txt', 'r').read().split('\n')

    def analyze_symantec(self):
        for ip in self.documento:
            webbrowser.open_new("https://sitereview.bluecoat.com/#/")
            time.sleep(3)
            pyperclip.copy(ip)
            pyautogui.hotkey('ctrl', 'v', interval=0.15)
            pyautogui.press("enter")

    def analyze_abuseip(self):
        for ip in self.documento:
            webbrowser.open_new("https://www.abuseipdb.com/")
            time.sleep(3)
            for i in range(15):
                pyautogui.press('tab')
            pyperclip.copy(ip)
            pyautogui.hotkey('ctrl', 'v', interval=0.15)
            pyautogui.press("enter")

    def analyze_virustotal(self):
        for ip in self.documento:
            webbrowser.open_new("https://www.virustotal.com/gui/home/search")
            time.sleep(3)
            for i in range(6):
                pyautogui.press('tab')
            pyperclip.copy(ip)
            pyautogui.hotkey('ctrl', 'v', interval=0.15)
            pyautogui.press("enter")

if __name__ == "__main__":
    tool = IPAnalysisTool()
    eleccion = input(Fore.GREEN + "Escribe el número de la herramienta que quieras usar para analizar las direcciones IP" + Fore.YELLOW +
                    """\n1 - Symantec
                    2 - AbuseIP
                    3 - VirusTotal: \n""" + Style.RESET_ALL + "Cuál es tu elección? -->")

    if eleccion == "1":
        tool.analyze_symantec()
    elif eleccion == "2":
        tool.analyze_abuseip()
    elif eleccion == "3":
        tool.analyze_virustotal()
    else:
        print("ERROR: Elige un número del 1 al 3")