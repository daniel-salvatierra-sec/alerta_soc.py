# AGENTS.md

## Cursor Cloud specific instructions

This is a small Python 3 (3.12) "SOC Automation Lab" project. There are no services,
web servers, databases, tests, lint config, or build steps — just three standalone CLI
scripts documented in `README.md`. The only third-party dependency is `rich`.

### Environment
- Dependencies are installed into the `venv_soc/` virtualenv (git-ignored). Run scripts
  with `./venv_soc/bin/python <script>.py`.
- The `python3-venv` system package is required to create the virtualenv; it is provided
  by the VM snapshot (the update script only refreshes the Python deps).
- `sudo` is passwordless in the cloud VM.

### Runtime data caveat (important, non-obvious)
- All three scripts read `/var/log/auth.log`, which does **not** exist by default in the
  cloud VM. Without it, `monitor.py`/`tabla_seguridad.py` raise `FileNotFoundError` and
  `alerta_soc.py`'s `sudo tail -f` prints nothing. To exercise/demonstrate the scripts,
  populate the log with realistic auth entries (e.g. `sudo tee -a /var/log/auth.log`),
  including lines containing `Failed`, `failure`, `invalid`, `incorrect password`, or
  `FAILED` so the detectors fire.

### Running the scripts
- `tabla_seguridad.py` is one-shot: reads the last 50 lines and prints a Rich table of
  detected failures, then exits.
- `monitor.py` and `alerta_soc.py` run forever (tail-follow); stop with Ctrl-C. When
  capturing their output to a file, use `python -u` (unbuffered) or the buffer may not
  flush before the process is stopped.
