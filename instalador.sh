#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Este script requiere privilegios de administrador. Pidiendo contraseña..."
  exec sudo bash "$0" "$@"
fi

archivo="cliente.py"
archivo2="server.py"
destino="/usr/local/bin/temp"

if [ ! -f "$archivo" ] || [ ! -f "$archivo2" ]; then
  echo "No se encontró el archivo $archivo o $archivo2 en el directorio actual."
  echo "Debes correr este .sh en el mismo directorio de $archivo y $archivo2"
  exit 1
fi


cp "$archivo" "$destino"
chmod +x "$destino"

echo "Archivo instalado correctamente en $destino"

if command -v ufw >/dev/null 2>&1; then
  echo "Habilitando puerto 54001 en ufw..."
  ufw allow 54001/tcp
  echo "Puerto 54001 habilitado en ufw."
else
  echo "ufw no está instalado, no se pudo habilitar el puerto 54001."
fi

echo "Instalacion completa."
