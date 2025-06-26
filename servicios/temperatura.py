 # servicios/temperatura.py
import psutil

def tempCPU():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return "No se pudo obtener la temperatura."

        resultado = ""
        for nombre, sensores in temps.items():
            resultado += f"{nombre}:\n"
            for sensor in sensores:
                resultado += f"  {sensor.label or 'sin etiqueta'}: {sensor.current} °C\n"

        return resultado
    except Exception as e:
        return f"Error al obtener temperatura: {e}"

