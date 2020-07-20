import sys
from functions.MSSclient import *
from utils.MSSutils import *
from utils.CLParser import *
import socket
from random import randint
import numpy

# Ejemplo 6 para acceder a camaras predefinidas en el simulador
# 1.- Ejecutar primero el scrip : ejem6_initRACamera (ejecutar 1 sola vez)
# 2.- Ejecutar despues el script: ejem6_viewRACamera (ejecutar las veces que se desee acceder a las camaras)
sock = -1

# parse command line arguments (if any)
(ipAddress, port, cfgpath) = CLParser(sys.argv[1:len(sys.argv)])

# display demo information in console
print("RACameraDemo 6: Script 2 View Camaras\n")
print("Este script pretender ejecutarse varias veces siendo asi cada ejecucion un registro de un nuevo cliente")
print(" (1) Conexion como nuevo cliente en el simulador")
print(" (2) Variable 'Name' de ser igual que en el scriipt 1 (ejem6_initRACamera)")
print(" (3) Indicar solo el ID de la camara a la que se deseea acceder")
print(" (4) Visualizar y finalizar el registro del cliente")

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

name = "Demo6_InitcializarViewCam"
numcamera = input("Ingrese ID al nombre: "+name+"_")
name = name+"_"+numcamera
print(name)

cam = MSScam(name, 640, 480)
cam.setRegister(cli.sock, ipAddress, port)

cam.preview(100)

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)