import time

log_path = "/var/log/auth.log"

print("--- INICIANDO MONITOR DE SEGURIDAD (SOC) ---")

with open(log_path, "r") as f:
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        
        if "failure" in line.lower() or "failed" in line.lower():
            print(f"\033[91m [ALERTA] Intento fallido detectado: {line.strip()} \033[0m")
        else:
            print(f"[OK] {line.strip()}")
