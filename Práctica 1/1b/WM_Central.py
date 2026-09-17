import socket 
import threading


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
MAX_CONEXIONES = 5

def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")

    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        respuesta = registrar(msg)
        print(f" He recibido de la estacion [{addr}] el mensaje: {msg}")
        conn.send(respuesta.encode(FORMAT))
    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()
    
def registrar(msg):
    sesion = msg.split("#")

    if len(sesion) != 3:
        return "STATUS#ERROR#Formato incorrecto. Debe ser: REGISTRO#<ID_ESTACION>#<UBICACION>"

    registro, id_estacion, ubicacion = sesion
    if registro != "REGISTRO":
        return "STATUS#ERROR#Comando desconocido"
    if not id_estacion or not ubicacion:
        return "STATUS#ERROR#El ID o la ubicacion no pueden estar vacios"
 
    print(f"[ESTACION REGISTRADA] ID: {id_estacion} - Ubicacion: {ubicacion}")
    return "STATUS#OK#Estacion registrada correctamente"

def start():
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = threading.active_count()-1
    print(CONEX_ACTIVAS)
    while True:
        conn, addr = server.accept()
        CONEX_ACTIVAS = threading.active_count()
        if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
            print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
        else:
            print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
            conn.send("STATUS#ERROR#Demasiadas conexiones. Tendras que esperar a que alguien se vaya".encode(FORMAT))
            conn.close()
            CONEX_ACTUALES = threading.active_count()-1
        

######################### MAIN ##########################


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] Servidor inicializándose...")

start()

