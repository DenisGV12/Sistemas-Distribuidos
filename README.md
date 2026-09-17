# Práctica 1 — Sockets

Sistemas Distribuidos, Universidad de Alicante, curso 26/27.

Denis Golovnyuk Volosovych y Daironas Sukis.

Aquí está nuestra práctica de sockets en Python, dividida en dos partes: primero
una calculadora cliente/servidor para coger soltura con los sockets y los hilos
(1a), y luego el registro de estaciones de riego (1b), que reutiliza la misma
estructura y nos sirve de base para la práctica final de Water Management.

Todo va sobre TCP y el servidor atiende a cada cliente en un hilo aparte, así que
se pueden conectar varios a la vez.

## 1a — La calculadora

El servidor recibe operaciones del tipo `3 + 4` y devuelve el resultado. Admite
suma, resta, multiplicación y división con enteros positivos. Si le mandas algo
mal escrito o una división entre cero, responde con un mensaje de error pero no
corta la conexión.

Para lanzarlo:

```bash
python3 servidor_concurrente.py
python3 cliente_concurrente.py <IP_SERVIDOR> 5050 "3 + 4"
```

La operación va entre comillas porque lleva espacios. Después el cliente te va
pidiendo más operaciones por teclado hasta que escribes `FIN`.

En la carpeta están también `servidor_simple.py` y `cliente_simple.py`, que son
el material de clase sin modificar (una sola conexión, puerto 8010). Los dejamos
como referencia.

## 1b — WM_Central y WM_WS_M

Misma idea, pero en vez de calcular, la central registra estaciones de riego. Los
nombres de los ficheros son los que pide el anexo para poder reaprovecharlos
luego en Water Management.

Los mensajes son tramas con los campos separados por `#`. La estación manda:

```
REGISTRO#WS-04#River Park
```

Y la central contesta `STATUS#OK#Estacion registrada correctamente` si todo está
bien, o `STATUS#ERROR#<motivo>` si la trama no tiene tres campos, el primero no
es `REGISTRO`, o el ID o la ubicación vienen vacíos. Cuando registra una estación
la saca por consola.

Para lanzarlo:

```bash
python3 WM_Central.py
python3 WM_WS_M.py <IP_SERVIDOR> 5050 WS-01 Fuentealbilla
```

Si la ubicación tiene espacios, entre comillas:

```bash
python3 WM_WS_M.py 192.168.18.76 5050 WS-04 "River Park"
```

El monitor se conecta, manda su trama, imprime lo que le contesta la central y
cierra. Si quieres ver la concurrencia, abre tres terminales y lánzalos a la vez.
