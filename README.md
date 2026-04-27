# 🛡️ SOC Automation Lab - Security Monitor

A practical **Security Operations Center (SOC)** laboratory designed to monitor, detect, and alert on intrusion attempts within a Linux (WSL/Ubuntu) environment using Python.

## 🚀 Key Features
- **Active Surveillance:** Real-time streaming of `/var/log/auth.log`.
- **Threat Detection:** Identifies failed login attempts and unauthorized `sudo` usage.
- **Sensory Alerts:** Triggers a physical "Beep" sound and visual cues upon detecting critical events.
- **Professional Dashboard:** Displays security incidents in structured tables using the `Rich` library.

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **OS:** Ubuntu (WSL2)
- **Main Libraries:** - `Rich`: For advanced terminal UI.
  - `Subprocess`: For Linux kernel integration.

## 📁 Project Structure
- `alerta_soc.py`: Main real-time monitoring and alerting script.
- `tabla_seguridad.py`: Security incident report generator.
- `venv_soc/`: Isolated virtual environment for lab integrity.

## 🛡️ Analysis Purpose
This lab simulates the workflow of a Tier 1 SOC Analyst, focusing on **observability** and initial **incident response**.
