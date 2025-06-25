#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Por favor, ejecuta este script como administrador (sudo)."
  exit 1
fi

archivo="cliente.py"
noExtension="${archivo%.py}"
destino="/usr/local/bin/$noExtension"

if [ ! -f "$archivo" ]; then
  echo "No se encontró el archivo $archivo en el directorio actual."
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