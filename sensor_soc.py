import os
import time
import shutil
import hashlib
import sys
from datetime import datetime

DIRECTORIO_A_VIGILAR = "."
CARPETA_FORENSE = "evidencia_soc"
LOG_ATAQUES = "soc_incidents.log"
IGNORAR = [CARPETA_FORENSE, ".git", "__pycache__", LOG_ATAQUES]

def calcular_hash(ruta_archivo):
    """Calcula la huella digital SHA-256 del archivo."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(ruta_archivo, "rb") as f:
            for bloque in iter(lambda: f.read(4096), b""):
                hash_sha256.update(bloque)
        return hash_sha256.hexdigest()
    except:
        return None

def registrar_evento(mensaje):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_ATAQUES, "a") as f:
        f.write(f"[{timestamp}] {mensaje}\n")
    print(f"[{timestamp}] {mensaje}")

def alerta_sonora():
    sys.stdout.write('\a')
    sys.stdout.flush()

def obtener_inventario():
    inventario = {}
    for r, _, fs in os.walk(DIRECTORIO_A_VIGILAR):
        if any(ig in r for ig in IGNORAR): continue
        for f in fs:
            if any(ig in f for ig in IGNORAR): continue
            ruta = os.path.join(r, f)
            huella = calcular_hash(ruta)
            if huella: inventario[ruta] = huella
    return inventario

def monitor_soc():
    registrar_evento("[-] SISTEMA: JARVIS SOC v4.0 (SHA-256) Activo. Blindaje Anti-IA iniciado.")
    inventario_anterior = obtener_inventario()

    try:
        while True:
            time.sleep(0.5)
            inventario_actual = obtener_inventario()

            for ruta, huella in inventario_actual.items():
                if ruta not in inventario_anterior:
                    alerta_sonora()
                    registrar_evento(f"[+] NUEVO: Archivo detectado: {ruta}")
                elif huella != inventario_anterior[ruta]:
                    alerta_sonora()
                    registrar_evento(f"[!!!] ALERTA: Cambio de HASH detectado (Manipulación de contenido) en: {ruta}")
                    
                    ts = datetime.now().strftime("%H%M%S")
                    shutil.copy2(ruta, f"{CARPETA_FORENSE}/{ts}_{os.path.basename(ruta)}")

            for ruta in inventario_anterior:
                if ruta not in inventario_actual:
                    alerta_sonora()
                    registrar_evento(f"[CRÍTICO] SABOTAJE: Archivo eliminado: {ruta}")

            inventario_anterior = inventario_actual
    except KeyboardInterrupt:
        registrar_evento("[-] SISTEMA: Sensor desactivado por Analista Salvatierra.")

if __name__ == "__main__":
    monitor_soc()
