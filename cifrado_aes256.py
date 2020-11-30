
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".aes", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'script.py' and fname != 'data.txt.enc'):
                    dirs.append(dirName + "\\" + fname)
        return dirs

key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
aes = Encryptor(key)
clear = lambda: os.system('cls')

if os.path.isfile('data.txt.aes'):
    while True:
        password = str(input("Ingrese contraeña: "))
        aes.decrypt_file("data.txt.aes")
        p = ''
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            aes.encrypt_file("data.txt")
            break

    while True:
        clear()
        choice = int(input(
            "1. Presiona '1' para encriptar el archivo.\n2. Presiona '2' para desencriptar el archivo.  "))
        clear()
        if choice == 1:
            aes.encrypt_file(str(input("Ingrese el nombre del archivo a encriptar: ")))
        elif choice == 2:
            aes.decrypt_file(str(input("INgrese el nombre del archivo a desencriptar: ")))
   
else:
    while True:
        clear()
        password = str(input("Ingrese contraseña para desencriptar: "))
        repassword = str(input("Confirmar contraseña: "))
        if password == repassword:
            break
        else:
            print("contraeña incorrecta!")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    aes.encrypt_file("data.txt")
    print("Reinicia el programa para realizar cambios")
    time.sleep(5)
