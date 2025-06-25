import socket

SERVIDOR_IP = "192.168.1.50"  # IP de la PC con el sensor
PUERTO = 54001

comando = f"temp {SERVIDOR_IP}"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVIDOR_IP, PUERTO))
    s.sendall(comando.encode())
    respuesta = s.recv(1024).decode()
    print(f"Respuesta del servidor: {respuesta}")
