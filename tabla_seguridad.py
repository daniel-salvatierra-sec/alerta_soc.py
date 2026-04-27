import re
from rich.console import Console
from rich.table import Table

console = Console()
log_path = "/var/log/auth.log"

def analizar_logs():
    table = Table(title="🚨 REPORTE AUTOMÁTICO DE SEGURIDAD - SOC 🚨")
    table.add_column("Fecha/Hora", style="cyan")
    table.add_column("Usuario", style="magenta")
    table.add_column("Acción/Error", style="yellow")
    table.add_column("Severidad", style="bold red")

    try:
        with open(log_path, "r") as f:
            lineas = f.readlines()
            
        
        for linea in lineas[-50:]:
            if "incorrect password" in linea or "FAILED" in linea:
                
                fecha = linea[:16]
                
                usuario = "daniel" if "daniel" in linea else "desconocido"
                
                table.add_row(fecha, usuario, "Fallo de Autenticación", "CRÍTICA")
        
        console.print(table)
    except PermissionError:
        console.print("[bold red]Error:[/bold red] Necesitas ejecutar con 'sudo'")

if __name__ == "__main__":
    analizar_logs()
