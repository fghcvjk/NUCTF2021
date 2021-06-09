# !/usr/bin/env python3
import socketserver
import os
import sys
import signal
import string
import random
from hashlib import sha256
from random import getrandbits, randrange
from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
import binascii
import traceback


from secret import flag

BANNER = br"""
_________                        __                               .__       .___
\_   ___ \_______ ___.__._______/  |_  ____   __  _  _____________|  |    __| _/
/    \  \/\_  __ <   |  |\____ \   __\/  _ \  \ \/ \/ /  _ \_  __ \  |   / __ | 
\     \____|  | \/\___  ||  |_> >  | (  <_> )  \     (  <_> )  | \/  |__/ /_/ | 
 \______  /|__|   / ____||   __/|__|  \____/    \/\_/ \____/|__|  |____/\____ | 
        \/        \/     |__|                                                \/ 

"""
LOGGER = br"""
WELCOME, YOU HAVE THREE CHOICES BELOW!
1.Get encrypted flag
2.Get encryption
3.Exit
"""


class Task(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kargs):
        self.KEY = b""
        self.IV = b""
        super().__init__(*args, **kargs)

    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def encrypt_cbc(self, data):
        aes = AES.new(self.KEY, AES.MODE_CBC, self.IV)
        return aes.encrypt(data)

    def encrypt_cfb(self, data):
        aes = AES.new(self.KEY, AES.MODE_CFB, self.IV, segment_size=128)
        return aes.encrypt(data)

    def any_cbc(self):
        try:
            hex_input = self.recv()
            if len(hex_input) % 32 != 0:
                self.send(
                    b"[-] the bit length of input data must be a multiple of 128 ")
            text = binascii.unhexlify(hex_input)
            ciphertext = self.encrypt_cbc(text)
            self.send(binascii.hexlify(ciphertext))
        except:
            traceback.print_exc()
            self.send(b"[-] Something Wrong!")
            self.request.close()

    def flag_cfb(self):
        plaintext = self.encrypt_cfb(flag)
        self.send(binascii.hexlify(plaintext))

    def handle(self):
        signal.alarm(1200)
        self.KEY = os.urandom(32)
        self.IV = os.urandom(16)
        self.send(BANNER)
        self.send(LOGGER)
        while True:
            try:
                choice = int(self.recv(prompt=b"[+] What's your choice?\n"))
            except:
                self.send(
                    f'[-] Sorry, you have wrong choice, exit...'.encode())
                exit(0)
            if choice == 1:
                self.send(b"[+] There is a encrypted message for you:")
                self.flag_cfb()
            elif choice == 2:
                self.send(b"[+] Let's make a encryption!")
                self.any_cbc()
            elif choice == 3:
                self.send(b"[!] Bye~")
                exit(0)
            else:
                self.send(b"[-] Wrong!")
                exit(0)


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
