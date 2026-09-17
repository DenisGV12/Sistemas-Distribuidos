import socket
import sys

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
########## MAIN ##########


print("****** WELCOME TO OUR BRILLIANT SD UA CURSO 2020/2021 SOCKET CLIENT ****")

if  (len(sys.argv) == 5):
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (SERVER, PORT)

    ID_ESTACION = sys.argv[3]
    UBICACION = sys.argv[4]
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print (f"Establecida conexión en [{ADDR}]")

    msg= f"REGISTRO#{ID_ESTACION}#{UBICACION}"
    print("Envio al servidor: ", msg)
    send(msg)
    print("Recibo del Servidor: ", client.recv(2048).decode(FORMAT))
    client.close()
else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos: <ServerIP> <Puerto> <ID_ESTACION> <UBICACION>")
