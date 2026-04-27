import subprocess
import time
from rich.console import Console
from rich.panel import Panel

console = Console()

def monitor_tiempo_real():
    log_path = "/var/log/auth.log"
  
    cmd = ["sudo", "tail", "-f", log_path]
    
    console.print(Panel("[bold green]🛡️ ESCUDO DE SEGURIDAD ACTIVO[/bold green]\nMonitorizando intentos de intrusión...", title="SOC DANIEL"))

    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        for line in process.stdout:
            
            if any(word in line.lower() for word in ["fail", "incorrect", "invalid", "failure"]):
                
                print("\a") 
                hora = time.strftime('%H:%M:%S')
                console.print(f"\n[bold white on red] 🚨 ALERTA - {hora} 🚨 [/bold white on red]")
                console.print(Panel(f"[bold yellow]DETALLE:[/bold yellow] {line.strip()}", border_style="red"))
                
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Desactivando vigilancia...[/bold yellow]")
        process.terminate()

if __name__ == "__main__":
    monitor_tiempo_real()
