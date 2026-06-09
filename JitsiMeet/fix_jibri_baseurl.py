#!/usr/bin/env python3
"""
Script para forzar que Jibri utilice la URL interna https://web en lugar de la
URL pública configurada en PUBLIC_URL.

El objetivo es evitar errores de Selenium relacionados con la carga de la
interfaz web de Jitsi, como el mensaje:

    APP is not defined

Funcionamiento:
1. Detecta el contenedor Jibri en ejecución.
2. Localiza el directorio de configuración montado en /config.
3. Modifica el fichero xmpp.conf para establecer:

       base-url = "https://web"

4. Reinicia el contenedor Jibri.
5. Comprueba en los registros si la URL interna está siendo utilizada.

Requisitos:
- Docker instalado y accesible desde la línea de comandos.
- Permisos para ejecutar comandos Docker.
"""

import json
import os
import re
import subprocess
import sys
import time
from typing import List


def sh(cmd: str, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check
    )


def die(msg: str, cp: subprocess.CompletedProcess = None):
    if cp is not None:
        sys.stderr.write(cp.stdout)
        sys.stderr.write(cp.stderr)

    print("ERROR:", msg)
    sys.exit(1)


def find_jibri_containers() -> List[str]:
    cp = sh(
        "docker ps --filter 'ancestor=jitsi/jibri' --format '{{.Names}}'",
        check=False
    )

    names = [ln.strip() for ln in cp.stdout.splitlines() if ln.strip()]

    if names:
        return names

    cp2 = sh(
        "docker ps --format '{{.Names}}' | grep -i jibri",
        check=False
    )

    return [ln.strip() for ln in cp2.stdout.splitlines() if ln.strip()]


def get_config_mount(container: str) -> str:
    cp = sh(f"docker inspect {container} -f '{{{{json .Mounts}}}}'")

    mounts = json.loads(cp.stdout.strip() or "[]")

    for mount in mounts:
        if mount.get("Destination") == "/config":
            return mount.get("Source")

    die(f"No se encontró un volumen montado en /config para {container}")


def patch_xmpp_conf(xmpp_path: str) -> bool:
    if not os.path.exists(xmpp_path):
        print(f"El fichero {xmpp_path} no existe.")
        return False

    with open(xmpp_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content, changes = re.subn(
        r'base-url\s*=\s*"[^"]+"',
        'base-url = "https://web"',
        content
    )

    if changes > 0:
        with open(xmpp_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print("base-url actualizado a https://web")
        return True

    print("No se encontró ninguna línea base-url para modificar.")
    return False


def show_container_env(container: str):
    cp = sh(
        f"docker inspect -f "
        f"'{{{{range .Config.Env}}}}{{{{println .}}}}{{{{end}}}}' "
        f"{container}"
    )

    public_url = [
        line for line in cp.stdout.splitlines()
        if line.startswith("PUBLIC_URL=")
    ]

    if public_url:
        print(public_url[0])


def restart_container(container: str):
    print(f"Reiniciando contenedor {container}...")
    sh(f"docker restart {container}")
    time.sleep(4)


def tail_for_baseurl(container: str, timeout_sec: int = 30) -> bool:
    start = time.time()

    while time.time() - start < timeout_sec:
        cp = sh(f"docker logs {container}", check=False)

        for line in cp.stdout.splitlines():
            if "baseUrl=" in line or "Visiting url" in line:
                print(line)

                if (
                    "baseUrl=https://web" in line
                    or "baseUrl='https://web'" in line
                ):
                    return True

        time.sleep(2)

    return False


def main():
    print("Jibri base-url fixer")

    containers = find_jibri_containers()

    if not containers:
        die("No se encontró ningún contenedor Jibri en ejecución")

    container = containers[0]

    print(f"Contenedor detectado: {container}")

    show_container_env(container)

    config_dir = get_config_mount(container)

    print(f"Directorio de configuración: {config_dir}")

    os.makedirs(config_dir, exist_ok=True)

    xmpp_path = os.path.join(config_dir, "xmpp.conf")

    modified = patch_xmpp_conf(xmpp_path)

    if not os.path.exists(xmpp_path):
        restart_container(container)

        if os.path.exists(xmpp_path):
            modified = patch_xmpp_conf(xmpp_path) or modified

    if modified:
        restart_container(container)

    if tail_for_baseurl(container):
        print("Verificación correcta: Jibri está utilizando https://web")
        sys.exit(0)

    print("No se pudo verificar el uso de https://web en los registros.")
    sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        die("Error ejecutando un comando del sistema", e)
