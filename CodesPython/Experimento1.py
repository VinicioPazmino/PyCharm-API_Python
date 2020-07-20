import sys
from functions.MSSclient import *
from utils.MSSutils import *
from utils.CLParser import *
import socket
from random import randint

sock = -1
# parse command line arguments (if any)
(ipAddress, port, cfgpath) = CLParser(sys.argv[1:len(sys.argv)])

# display demo information in console
print("Experimento 1 para evaluacion del rendimiento de MSS\n")
print("Crear y conectar una camara de Usuario al simulador\n")
print("Usar el Escenario <Experimento1> donde se varia el parâmetro Densidad de Objetos\n")

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)


# create the camera
name = "Experimento1"+str(randint(0, 99))  # rand in the range 0 to 99;

# cam = MSScam(name, 640, 480, 10, 10.38, -6.44, 5.0, 20.0, 10.0, 0.0)
cam = MSScam(name, 1280, 720, 29, 120, 5, -1, 0, -135, 0)
# cam = MSScam(name, 320, 240, 10, 10.38, -6.44, 5.0, 20.0, 10.0, 0.0)
cam.print_details()

# add the camera to the simulator
cam.addTosimulator(cli.sock, ipAddress, port)
cam.print_details()

# preview the camera for 10 secs
cam.preview(250)
cam.print_details()

# wait 1 sec before closing this demo
time.sleep(1)  # time in seconds

# unregistering camera
cam.removeFromSimulator()

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)