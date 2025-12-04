import socket
from mapa import Mapa
from barco import Barco

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1112

conexion = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conexion.bind((SERVER_IP, SERVER_PORT))

# Mapas de cada jugador
mapas_real = [Mapa(), Mapa()]       # mapa_real[0] → jugador1, mapa_real[1] → jugador2
mapas_visible = [Mapa(), Mapa()]    # mapa_visible[0] → lo que ve jugador1 del enemigo, mapas_visible[1] → lo que ve jugador2

# Lista de barcos
barcos_disponibles = ['portaviones', 'acorazado', 'destructor', 'fragata']

# Almacenar direcciones de los clientes
jugadores = [None, None]

turno = 0  # 0 → jugador 1, 1 → jugador 2

print("Servidor iniciado. Esperando jugadores...")

# --------------------------
# Conectar jugadores
# --------------------------
while None in jugadores:
    msg, addr = conexion.recvfrom(1024)
    msg = msg.decode()
    if msg.startswith("CONECTAR"):
        if jugadores[0] is None:
            jugadores[0] = addr
            conexion.sendto("JUGADOR:1".encode(), addr)
            print("Jugador 1 conectado:", addr)
        elif jugadores[1] is None:
            jugadores[1] = addr
            conexion.sendto("JUGADOR:2".encode(), addr)
            print("Jugador 2 conectado:", addr)

print("Ambos jugadores conectados. Iniciando juego...")

# --------------------------
# Colocar barcos
# --------------------------
for idx in [0, 1]:
    jugador_actual = idx
    conexion.sendto("TURNO_COLOCAR".encode(), jugadores[jugador_actual])

    for tipo in barcos_disponibles:
        colocado = False
        while not colocado:
            msg, addr = conexion.recvfrom(1024)
            msg = msg.decode()
            partes = msg.split(":")
            if partes[0] == "COLOCAR":
                orient = partes[2].upper()
                x = int(partes[3])
                y = int(partes[4])
                barco = Barco(tipo)
                try:
                    # Colocar barco en el mapa real del jugador
                    mapas_real[jugador_actual].posicionar_barco(barco, orient, x, y)
                    conexion.sendto("OK".encode(), addr)
                    colocado = True
                    print(f"Jugador {jugador_actual+1} colocó un barco")
                    # Avisar al otro jugador que se colocó un barco (sin posiciones)
                    conexion.sendto(f"Jugador {jugador_actual+1} colocó un barco.".encode(),
                                    jugadores[1 - jugador_actual])
                except ValueError as e:
                    conexion.sendto(f"ERROR:{e}".encode(), addr)

            # Enviar mapas al jugador actual
            mapa_info = f"=== MAPA ENEMIGO ===\n{mapas_visible[jugador_actual].get_diseno_string()}\n=== TU MAPA ===\n{mapas_real[jugador_actual].get_diseno_string()}"
            conexion.sendto(mapa_info.encode(), addr)

# --------------------------
# Turnos de ataque
# --------------------------
game_over = False
while not game_over:
    jugador_actual = turno
    jugador_enemigo = 1 - turno

    # Avisar turno
    conexion.sendto("TU_TURNO".encode(), jugadores[jugador_actual])

    # Mostrar mapas al jugador actual
    mapa_info = f"=== MAPA ENEMIGO ===\n{mapas_visible[jugador_actual].get_diseno_string()}\n=== TU MAPA ===\n{mapas_real[jugador_actual].get_diseno_string()}"
    conexion.sendto(mapa_info.encode(), jugadores[jugador_actual])

    # Recibir ataque
    msg, addr = conexion.recvfrom(1024)
    msg = msg.decode()
    partes = msg.split(":")
    if partes[0] == "ATACAR":
        x = int(partes[1])
        y = int(partes[2])
        resultado = mapas_real[jugador_enemigo].golpear(x, y)

        # Actualizar mapa visible del atacante
        if resultado in ["TOCADO", "HUNDIDO"]:
            mapas_visible[jugador_actual].get_mapa_visible()[y-1][x-1] = "x"
        elif resultado == "AGUA":
            mapas_visible[jugador_actual].get_mapa_visible()[y-1][x-1] = "o"

        # Enviar resultado al jugador actual
        conexion.sendto(f"Resultado: {resultado}".encode(), jugadores[jugador_actual])
        print(f"Jugador {jugador_actual+1} atacó ({x},{y}): {resultado}")

        # Avisar al enemigo del ataque (sin mostrar barcos, solo resultado)
        conexion.sendto(f"Jugador {jugador_actual+1} atacó ({x},{y}): {resultado}".encode(),
                        jugadores[jugador_enemigo])

        # Comprobar si todos los barcos del enemigo están hundidos
        todos_hundidos = all(b.get_vida() <= 0 for b in mapas_real[jugador_enemigo]._Mapa__barcos)
        if todos_hundidos:
            print(f"Jugador {jugador_actual+1} ganó!")
            conexion.sendto(f"Jugador {jugador_actual+1} ganó!".encode(), jugadores[0])
            conexion.sendto(f"Jugador {jugador_actual+1} ganó!".encode(), jugadores[1])
            game_over = True

    # Cambiar turno
    turno = 1 - turno
