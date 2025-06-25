#!/usr/bin/env python3
import socket
import sys

if len(sys.argv) != 2:
    print("Uso: temp <ip>")
    sys.exit(1)

ip = sys.argv[1]
PUERTO = 54001
comando = f"temp {ip}"

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, PUERTO))
        s.sendall(comando.encode())
        respuesta = s.recv(1024).decode()
        print(f"Respuesta del servidor: {respuesta}")
except Exception as e:
    print(f"Error: {e}")
