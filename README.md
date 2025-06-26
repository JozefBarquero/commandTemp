# 🖥️ Monitor de Temperatura de Servidor

Este proyecto permite monitorear la temperatura de un servidor de forma remota mediante una interfaz cliente-servidor simple. Cuenta con notificaciones por Telegram, scripts de instalación multiplataforma y una interfaz gráfica para el servidor en Linux.

---

## 🚀 Características

- 📡 Consulta remota de temperatura del servidor.
- 🔔 Notificaciones automáticas por Telegram si se supera un umbral configurable.
- 🖼️ Interfaz gráfica para el servidor (solo en Linux).
- ⚙️ Scripts de instalación para:
  - Linux (`instalador.sh`)
  - Windows (`instalar.ps1`, solo cliente por ahora)

---

## 🛠️ Instalación

### En Linux

**Cliente:**
```bash
sudo bash instalador.sh
```

**Servidor:**
```bash
./dist/server
```

### En Windows

**Cliente:**

Ejecutar `instalar.ps1` como administrador.

**Servidor:**

⚠️ Aún no implementado.

---

## 📦 Requisitos

- Python 3.12 o superior

---

## ▶️ Uso

Desde el cliente, ejecuta:

```bash
temp <IP_del_servidor>
```

---

## ⚠️ Notas

- La versión para servidor en Windows aún no está disponible.
- Las pruebas en Windows son limitadas, puede haber errores.
