import socket
from servicios.temperatura import tempCPU

HOST = "0.0.0.0"  
PUERTO = 54001    

def obIP():
    return socket.gethostbyname(socket.gethostname())

ipLocal = obIP()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
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
