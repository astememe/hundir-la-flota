import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1112

conexion = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conexion.sendto("CONECTAR".encode(), (SERVER_IP, SERVER_PORT))

msg, _ = conexion.recvfrom(1024)
jugador_info = msg.decode()
print("Conectado como", jugador_info)

# -------------------------------------------------------
# COLOCAR BARCOS
# -------------------------------------------------------
while True:
    msg, _ = conexion.recvfrom(4096)
    if msg.decode() == "TURNO_COLOCAR":
        break

barcos_disponibles = ['portaviones', 'acorazado', 'destructor', 'fragata']

for tipo in barcos_disponibles:
    colocado = False
    while not colocado:
        print(f"\nColocando {tipo.upper()}")
        orient = input("Orientación ('H'orizontal / 'V'ertical): ").upper()
        x = input("Coordenada X inicio: ")
        y = input("Coordenada Y inicio: ")
        conexion.sendto(f"COLOCAR:{tipo}:{orient}:{x}:{y}".encode(), (SERVER_IP, SERVER_PORT))
        resp, _ = conexion.recvfrom(4096)
        resp = resp.decode()
        if resp == "OK":
            print("Barco colocado correctamente")
            colocado = True
        else:
            print(resp)
        # Mostrar mapas
        mapa, _ = conexion.recvfrom(4096)
        print(mapa.decode())

# -------------------------------------------------------
# TURNO DE ATAQUE
# -------------------------------------------------------
while True:
    msg, _ = conexion.recvfrom(4096)
    if msg.decode() == "TU_TURNO":
        print("\n--- TU TURNO ---")
        mapa, _ = conexion.recvfrom(4096)
        print(mapa.decode())
        x = input("Coordenada X a atacar: ")
        y = input("Coordenada Y a atacar: ")
        conexion.sendto(f"ATACAR:{x}:{y}".encode(), (SERVER_IP, SERVER_PORT))
        resp, _ = conexion.recvfrom(1024)
        print("Resultado ataque:", resp.decode())
