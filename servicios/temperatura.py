 # servicios/temperatura.py
import psutil

def tempCPU():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return "No se pudo obtener la temperatura."
        
        for nombre, sensores in temps.items():
            for sensor in sensores:
                if sensor.label == 'Package id 0' or sensor.label == '':
                    return f"{sensor.current}"
        
        sensor = list(temps.values())[0][0]
        return sensor.current
        
    except Exception as e:
        return f"Error al obtener temperatura: {e}"
