#!/usr/bin/env python3


import socket
import threading
import tkinter as tk
from tkinter import messagebox
from servicios.temperatura import tempCPU

# Función para obtener la IP local
def obIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except:
        return "127.0.0.1"

# Función que corre el servidor
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
                                conn.sendall(f"{temperatura} ªC".encode())
                            else:
                                conn.sendall(b"IP no coincide.")
                        except:
                            conn.sendall(b"Comando invalido.")
                    else:
                        conn.sendall(b"Comando desconocido.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el servidor:\n{e}")

# Interfaz gráfica
def main_gui():
    root = tk.Tk()
    root.title("Servidor de Temperatura")
    root.geometry("300x200")
    root.resizable(False, False)

    ip = obIP()

    tk.Label(root, text=f"IP local: {ip}").pack(pady=10)
    tk.Label(root, text="Puerto:").pack()

    puerto_var = tk.StringVar(value="54001")
    puerto_entry = tk.Entry(root, textvariable=puerto_var)
    puerto_entry.pack()

    def iniciar():
        try:
            puerto = int(puerto_var.get())
            threading.Thread(target=iniciar_servidor, args=(puerto,), daemon=True).start()
            messagebox.showinfo("Servidor", f"Servidor activo en {ip}:{puerto}")
        except ValueError:
            messagebox.showerror("Error", "Puerto inválido.")

    tk.Button(root, text="Iniciar servidor", command=iniciar).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
