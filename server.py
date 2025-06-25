import socket
from servicios.temperatura import tempCPU

HOST = "0.0.0.0"  
PUERTO = 54001    

import socket

def obIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except:
        return "127.0.0.1"

PUERTO = 54001
ipLocal = obIP()
HOST = "0.0.0.0"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PUERTO))
    s.listen()
    print(f"Servidor activo en {ipLocal}:{PUERTO}")


    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conexión desde {addr}")
            datos = conn.recv(1024).decode().strip()

            if datos.startswith("temp"):
                try:
                    _, ip_destino = datos.split()

                    if ip_destino == ipLocal:
                        temperatura = tempCPU()
                        conn.sendall(f"Temperatura: {temperatura}".encode())
                    else:
                        conn.sendall(b"IP no coincide.")
                except:
                    conn.sendall(b"Comando invalido.")
            else:
                conn.sendall(b"Comando desconocido.")
