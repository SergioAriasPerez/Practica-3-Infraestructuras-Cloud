#!/usr/bin/env python3
# Despliega N contenedores LXC, cada uno con el servidor web Node.js
# Uso: sudo python3 lxc_web.py [N]
import subprocess, sys, time

REPO = "https://github.com/gisai/SSR-master-server"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1       # nº de contenedores

def sh(cmd):                                           # ejecuta un comando en el anfitrión
    print("$", cmd)
    subprocess.run(cmd, shell=True, check=True)        # si falla, el script se para

for i in range(1, N + 1):
    c = f"web{i}"                                      # nombre del contenedor
    dentro = f"lxc-attach -n {c} --"                   # prefijo: ejecutar dentro del contenedor
    sh(f"lxc-create -t download -n {c} -- --dist ubuntu --release jammy --arch amd64")
    sh(f"lxc-start -n {c}")                            # arranca el contenedor
    time.sleep(10)                                     # espera a que tenga red
    sh(f"{dentro} apt-get update")
    sh(f"{dentro} apt-get install -y nodejs npm git")  # instala Node y git
    sh(f"{dentro} git clone {REPO} /app")              # descarga el servidor
    sh(f"{dentro} npm --prefix /app install")          # instala sus dependencias
    # arranca el servidor en segundo plano (puerto 3000)
    sh(f"{dentro} sh -c 'cd /app && setsid -f node app.js > salida.log 2>&1 < /dev/null'")
    ip = subprocess.check_output(f"lxc-info -n {c} -iH", shell=True, text=True).split()[0]
    print(f"Servidor {c} disponible en http://{ip}:3000")   # accesible desde el anfitrión
