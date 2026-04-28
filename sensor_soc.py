import os
import time
import shutil
from datetime import datetime


DIRECTORIO_A_VIGILAR = "."
CARPETA_FORENSE = "evidencia_soc"
EXTENSIONES_IGNORADAS = {'.git', '.swp', '.tmp'}

if not os.path.exists(CARPETA_FORENSE):
    os.makedirs(CARPETA_FORENSE)

def obtener_estado_archivos(directorio):
    estado = {}
    for ruta_directorio, _, archivos in os.walk(directorio):
        if CARPETA_FORENSE in ruta_directorio or ".git" in ruta_directorio:
            continue
        for nombre_archivo in archivos:
            ruta_completa = os.path.join(ruta_directorio, nombre_archivo)
            try:
                estado[ruta_completa] = os.path.getmtime(ruta_completa)
            except OSError:
                continue
    return estado

print(f"[-] JARVIS: Sensor v2.0 Activo. Guardando evidencia en '{CARPETA_FORENSE}'...")
estado_anterior = obtener_estado_archivos(DIRECTORIO_A_VIGILAR)

try:
    while True:
        time.sleep(1)
        estado_actual = obtener_estado_archivos(DIRECTORIO_A_VIGILAR)

        
        for archivo, fecha_mod in estado_actual.items():
            if archivo not in estado_anterior or fecha_mod > estado_anterior[archivo]:
                tipo = "Nuevo" if archivo not in estado_anterior else "Modificado"
                print(f"[!] ALERTA: {tipo}: {archivo}")
                
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_backup = f"{timestamp}_{os.path.basename(archivo)}"
                shutil.copy2(archivo, os.path.join(CARPETA_FORENSE, nombre_backup))
                print(f"[+] FORENSE: Evidencia resguardada como {nombre_backup}")

        
        for archivo in estado_anterior:
            if archivo not in estado_actual:
                print(f"[X] CRÍTICO: Archivo ELIMINADO: {archivo}")

        estado_anterior = estado_actual
except KeyboardInterrupt:
    print("\n[-] Sensor desactivado por el analista.")
