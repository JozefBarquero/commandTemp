# servicios/temperatura.py
import psutil

def tempCPU():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return "No se pudo obtener la temperatura del sistema."

        resultado = "\n\n"
        for nombre, sensores in temps.items():
            resultado += f"- Sensor: {nombre}\n"
            for sensor in sensores:
                etiqueta = sensor.label or "General"
                resultado += f"   ├─ {etiqueta}: {sensor.current:.1f} °C\n"
            resultado += "\n"

        return resultado.strip()
    except Exception as e:
        return f"Error al obtener temperatura: {e}"
