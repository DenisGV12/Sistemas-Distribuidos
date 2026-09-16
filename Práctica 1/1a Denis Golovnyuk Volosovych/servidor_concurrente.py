import math
import socket 
import threading


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
FIN = "FIN"
MAX_CONEXIONES = 2

def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == FIN:
                connected = False

            resultado = calcular(msg)
            print(f" He recibido del cliente [{addr}] el mensaje: {resultado}")
            conn.send(f"HOLA CLIENTE: El resultado es: {resultado} ".encode(FORMAT))
    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()
    
def calcular(msg):
    partes = msg.split()
    if len(partes) != 3:
        return "Error: Formato incorrecto. Debe ser: <num1> <operador> <num2>"

    n1, op, n2 = partes
    if not n1.isdigit() or not n2.isdigit():
        return "Error: Los operandos deben ser números."

    n1, n2 = int(n1), int(n2)
    match op:
        case '+': return n1 + n2
        case '-': return n1 - n2
        case '*': return n1 * n2
        case '/': return n1 / n2 if n2 != 0 else "Error: División por 0."
        case _:   return "Error: Operador no válido."

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
            conn.send("OOppsss... DEMASIADAS CONEXIONES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
            conn.close()
            CONEX_ACTUALES = threading.active_count()-1
        

######################### MAIN ##########################


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] Servidor inicializándose...")

start()

