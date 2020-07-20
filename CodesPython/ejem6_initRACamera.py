import sys
from functions.MSSclient import *
from utils.MSSutils import *
from utils.CLParser import *
import socket
from random import randint

# Ejemplo 6 para acceder a camaras predefinidas en el simulador
# 1.- Ejecutar primero el scrip : ejem6_initRACamera (ejecutar 1 sola vez)
# 2.- Ejecutar despues el script: ejem6_viewRACamera (ejecutar las veces que se desee acceder a las camaras)
sock = -1

# parse command line arguments (if any)
(ipAddress, port, cfgpath) = CLParser(sys.argv[1:len(sys.argv)])

# display demo information in console
print("RACameraDemo 6: Script 1 Inicializar Camaras\n")
print(" (1) Conexion como cliente en el simulador")
print(" (2) Lee numero de Camaras del simulador")
print(" (3) Configura Camaras y Asigna nombres con ID de cda una")
print(" (4) Nombres de acceso para ejecuar en Script 2 (ejem6_viewRACamera)")

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

numcam = MSScam()
numCam= numcam.readTosimulator(cli.sock, ipAddress, port)


name = "Demo6_InitcializarViewCam"
cam = MSScam(name, 640, 480)
cam.configRACamera(cli.sock, ipAddress, port)

print("Numero de camaras Disponibles "+ str(numCam))

if numCam == 0:
    print("No hay camaras moviles en el simulador")
else:
    i = 0
    while i < numCam:
        print("Acceder a las camaras con el nombre: "+ name +"_"+ str(i))
        i += 1

cli.disconnectFromSimulator(cli.sock)