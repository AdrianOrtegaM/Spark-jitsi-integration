#!/usr/bin/env python3
"""
Forces Jibri (docker-jitsi-meet) to open rooms using the container-internal host
`https://web` instead of the PUBLIC_URL/IP, eliminating the Selenium error
"APP is not defined" when the UI fails to initialize.

What this script does:
  1) Detects the running Jibri container name.
  2) Locates the host config dir mounted at /config inside the container.
  3) If an existing xmpp.conf is present in that directory and contains a
     base-url line, rewrites it to base-url = "https://web".
     (This file is included by the default jibri.conf template, so it takes effect.)
  4) Restarts only the Jibri container and tails the log to verify that
     baseUrl='https://web' is being used when you start a recording.

Notes:
  - Run this script on the host where Docker is running.
  - It requires the `docker` CLI to be available in PATH.
  - It DOES NOT change your global .env. Your browser can keep using the IP.
"""
import json
import os
import re
import subprocess
import sys
import time
from typing import List

BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


def sh(cmd: str, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=check)


def die(msg: str, cp: subprocess.CompletedProcess = None):
    if cp is not None:
        sys.stderr.write(cp.stdout)
        sys.stderr.write(cp.stderr)
    print(f"{RED}✖ {msg}{RESET}")
    sys.exit(1)


def find_jibri_containers() -> List[str]:
    # Prefer filtering by image ancestor
    cp = sh("docker ps --filter 'ancestor=jitsi/jibri' --format '{{.Names}}'", check=False)
    names = [ln.strip() for ln in cp.stdout.splitlines() if ln.strip()]
    if names:
        return names
    # Fallback: grep by name
    cp2 = sh("docker ps --format '{{.Names}}' | grep -i jibri", check=False)
    return [ln.strip() for ln in cp2.stdout.splitlines() if ln.strip()]


def get_config_mount(container: str) -> str:
    cp = sh(f"docker inspect {container} -f '{{{{json .Mounts}}}}'")
    mounts = json.loads(cp.stdout.strip() or '[]')
    for m in mounts:
        if m.get('Destination') == '/config':
            return m.get('Source')
    die("No /config mount found for container " + container)


def patch_xmpp_conf(xmpp_path: str) -> bool:
    """Return True if file was modified, False if unchanged/not present."""
    if not os.path.exists(xmpp_path):
        print(f"{YELLOW}• {xmpp_path} no existe aún. No parcheo nada por ahora.{RESET}")
        return False
    with open(xmpp_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace any existing base-url = "..."
    new_content, n = re.subn(r'base-url\s*=\s*"[^"]+"', 'base-url = "https://web"', content)
    if n > 0:
        with open(xmpp_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"{GREEN}✔ Reescrito base-url en {xmpp_path} → https://web{RESET}")
        return True
    else:
        # If base-url is missing but PUBLIC_URL is set in container, the template should generate it.
        print(f"{YELLOW}• No encontré línea base-url en {xmpp_path}. No modifico.{RESET}")
        return False


def show_container_env(container: str):
    cp = sh(f"docker inspect -f '{{{{range .Config.Env}}}}{{{{println .}}}}{{{{end}}}}' {container}")
    public = [ln for ln in cp.stdout.splitlines() if ln.startswith('PUBLIC_URL=')]
    print(f"{DIM}PUBLIC_URL del contenedor {container}: {public[0] if public else 'N/D'}{RESET}")


def restart_container(container: str):
    print(f"{YELLOW}• Reiniciando {container}...{RESET}")
    sh(f"docker restart {container}")
    time.sleep(4)


def tail_for_baseurl(container: str, timeout_sec: int = 30) -> bool:
    print(f"{YELLOW}• Esperando a que aparezca baseUrl en logs (hasta {timeout_sec}s). Inicia una grabación ahora.{RESET}")
    start = time.time()
    found = False
    while time.time() - start < timeout_sec:
        cp = sh(f"docker logs {container}", check=False)
        for ln in cp.stdout.splitlines():
            if 'baseUrl=' in ln or 'Visiting url' in ln:
                print(ln)
                if "baseUrl=https://web" in ln or "baseUrl='https://web'" in ln:
                    found = True
                    break
        if found:
            break
        time.sleep(2)
    return found


def main():
    print(f"{BOLD}Jibri base-url fixer (force https://web){RESET}")
    names = find_jibri_containers()
    if not names:
        die("No se encontró ningún contenedor Jibri en ejecución (imagen jitsi/jibri)")
    if len(names) > 1:
        print(f"{YELLOW}• He encontrado varios contenedores Jibri: {', '.join(names)}{RESET}")
    container = names[0]
    print(f"{GREEN}→ Usando contenedor: {container}{RESET}")

    show_container_env(container)

    cfg = get_config_mount(container)
    print(f"{GREEN}→ Directorio de configuración en host: {cfg}{RESET}")
    os.makedirs(cfg, exist_ok=True)

    xmpp_path = os.path.join(cfg, 'xmpp.conf')
    changed = patch_xmpp_conf(xmpp_path)

    # Si no existía xmpp.conf, fuerza regeneración eliminándolo (si faltara) y reiniciando
    if not os.path.exists(xmpp_path):
        print(f"{YELLOW}• No existe {xmpp_path}. Intento forzar su regeneración reiniciando el contenedor...{RESET}")
        restart_container(container)
        if os.path.exists(xmpp_path):
            print(f"{GREEN}✔ Generado {xmpp_path}{RESET}")
            changed = patch_xmpp_conf(xmpp_path) or changed
        else:
            print(f"{YELLOW}• Aún no existe {xmpp_path} tras reinicio. Puede generarse al primer intento de grabación.{RESET}")

    # Reinicia si hubo cambios
    if changed:
        restart_container(container)

    ok = tail_for_baseurl(container)
    if ok:
        print(f"{GREEN}✔ Detectado baseUrl='https://web' en logs. Debería desaparecer 'APP is not defined'.{RESET}")
        sys.exit(0)
    else:
        print(f"{YELLOW}• No vi baseUrl='https://web' aún. Si acabas de reiniciar, inicia una grabación y vuelve a ejecutar tail en unos segundos.{RESET}")
        print(f"{YELLOW}• Si persiste, revisa el contenido de {xmpp_path} y comparte las líneas con 'base-url'.{RESET}")
        sys.exit(2)


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        die("Fallo ejecutando un comando del sistema", e)
