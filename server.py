#!/usr/bin/env python3

import socket
import threading
import tkinter as tk
import requests
import time
from servicios.temperatura import tempCPU


TOKEN = ""
CHAT_ID = "" 
UMBRAL_TEMP = 80.0  


def obIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except:
        return "127.0.0.1"


def enviar_alerta(temp):
    mensaje = f"🚨 ¡Alerta! La temperatura del CPU es {temp}°C"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error al enviar mensaje de Telegram: {e}")


def monitor_temperatura():
    while True:
        try:
            temperatura = tempCPU()
            if temperatura and float(temperatura) > UMBRAL_TEMP:
                enviar_alerta(temperatura)
        except Exception as e:
            print(f"Error al verificar temperatura: {e}")
        time.sleep(10)  # cada 10 segundos

def enviar_mensaje_inicio():
    ip = obIP()
    mensaje = f"✅ Servidor iniciado correctamente en {ip}:54001"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error al enviar mensaje de inicio: {e}")


def iniciar_servidor(puerto):
    HOST = "0.0.0.0"
    ipLocal = obIP()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, puerto))
            s.listen()
            print(f"Servidor activo en {ipLocal}:{puerto}")
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
                                conn.sendall(f"{temperatura}".encode())
                            else:
                                conn.sendall(b"IP no coincide.")
                        except:
                            conn.sendall(b"Comando invalido.")
                    else:
                        conn.sendall(b"Comando desconocido.")
    except Exception as e:
        print(f"No se pudo iniciar el servidor: {e}")


def main_gui():
    root = tk.Tk()
    root.title("Servidor de Temperatura")
    root.geometry("300x110")
    root.resizable(False, False)

    ip = obIP()
    puerto = 54001  

    tk.Label(root, text=f"IP local: {ip}").pack(pady=10)
    tk.Label(root, text="Puerto:").pack()

    puerto_var = tk.StringVar(value=str(puerto))
    puerto_entry = tk.Entry(root, textvariable=puerto_var, state='disabled')
    puerto_entry.pack()
    
    enviar_mensaje_inicio()  # Notifica al iniciar el servidor


    threading.Thread(target=iniciar_servidor, args=(puerto,), daemon=True).start()
    threading.Thread(target=monitor_temperatura, daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main_gui()
