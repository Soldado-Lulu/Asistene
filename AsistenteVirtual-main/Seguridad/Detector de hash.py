import time
import hashlib
import os


class HashDetector:
    def __init__(self):
        self.file_name = None
        self.md5_hash = None
        self.sha1_hash = None
        self.sha256_hash = None

    def load_file(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                self.file_name = file_name
                file_content = file.read()
                self.calculate_hashes(file_content)
        except FileNotFoundError:
            print("El archivo '{}' no se encuentra.".format(file_name))

    def calculate_hashes(self, content):
        md5_hash = hashlib.md5(content)
        sha1_hash = hashlib.sha1(content)
        sha256_hash = hashlib.sha256(content)

        self.md5_hash = md5_hash.hexdigest()
        self.sha1_hash = sha1_hash.hexdigest()
        self.sha256_hash = sha256_hash.hexdigest()

    def detect_threat(self):
        if self.md5_hash == "b8e98421d608f4b5858f300974079002":
            print("MasterBootRecord VIRUS DETECTED!")

        if self.md5_hash == "7ed5b2dcccc1e3686f4b4f0da6a78e3e":
            print("RANSOMWARE.ENC.TROYAN DETECTED\n")

    def save_hashes_to_file(self):
        info = "md5 {} \nsha1 {}".format(self.md5_hash, self.sha1_hash)
        with open("hash.txt", 'w') as file:
            file.write(info)


if __name__ == "__main__":
    detector = HashDetector()
    file_name = "archivo.docx"  # Reemplaza con el nombre de tu archivo
    if os.path.exists(file_name):
        detector.load_file(file_name)
        detector.detect_threat()
        detector.save_hashes_to_file()
    else:
        print(f"El archivo '{file_name}' no existe.")

    time.sleep(9999)
