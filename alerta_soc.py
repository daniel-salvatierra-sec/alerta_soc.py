#!/usr/bin/env python3
"""
Real-time SOC authentication log monitor.

Streams a Linux authentication log (default: /var/log/auth.log) and raises
a visual + audible alert whenever a failed login attempt is detected.
Built as a lightweight SOC Tier 1 monitoring exercise using the `rich`
library for terminal output.

Usage:
    sudo python3 alerta_soc.py [--log-path /var/log/auth.log]
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()

FAILURE_KEYWORDS = ("fail", "incorrect", "invalid", "failure")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Real-time SOC authentication log monitor.")
    parser.add_argument(
        "--log-path",
        default="/var/log/auth.log",
        help="Path to the authentication log to monitor (default: /var/log/auth.log)",
    )
    return parser.parse_args()


def monitor(log_path: str) -> None:
    if not Path(log_path).exists():
        console.print(f"[bold red]Error:[/bold red] log file not found: {log_path}")
        sys.exit(1)

    console.print(
        Panel(
            "[bold green]SECURITY SHIELD ACTIVE[/bold green]\nMonitoring authentication attempts...",
            title="SOC MONITOR",
        )
    )

    cmd = ["sudo", "tail", "-f", log_path]

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] 'sudo' or 'tail' not available on this system.")
        sys.exit(1)

    try:
        for line in process.stdout:
            if any(keyword in line.lower() for keyword in FAILURE_KEYWORDS):
                print("\a")  # audible alert
                timestamp = time.strftime("%H:%M:%S")
                console.print(f"\n[bold white on red] ALERT - {timestamp} [/bold white on red]")
                console.print(Panel(f"[bold yellow]DETAIL:[/bold yellow] {line.strip()}", border_style="red"))
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Stopping monitor...[/bold yellow]")
    except PermissionError:
        console.print("[bold red]Error:[/bold red] insufficient permissions to read the log. Run with sudo.")
    finally:
        process.terminate()


if __name__ == "__main__":
    args = parse_args()
    monitor(args.log_path)
