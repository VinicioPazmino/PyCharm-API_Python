import sys
from functions.MSSclient import *
from utils.MSSutils import *
from utils.CLParser import *
from utils.DrawDisplay import*
import socket
from random import randint
from functions.MSScam import *
import numpy as np
from math import *
import time

# Inicializar la pantalla de frame
dibujarCanvas=DrawDisplay()

sock = -1

# parse command line arguments (if any)
(ipAddress, port, cfgpath) = CLParser(sys.argv[1:len(sys.argv)])

# display demo information in console
print("FrameOnDemand: Avanzar en el simulador cierto tiempo para capturar siguiente fream\n")
print(" (1) Conexion como cliente en el simulador")

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)
timeWait = 1/25 # tiempo de salto de frame to frame en el simulador (segundos)

name = "demo2_frameOnDemand"+str(randint(0, 99))  # rand in the range 0 to 99;
cam1 = MSScam(name, 640, 480, 10, 0, 10, 0, 10, 123, 0.0)
cam1.addTosimulator(cli.sock, ipAddress, port)

# Crear la misma camara con parametros dienticos
name = "demo2_frameOnDemand"+str(randint(0, 99))  # rand in the range 0 to 99;
cam2 = MSScam(name, 640, 480, 10, 0, 10, 0, 10, 123, 0.0)
cam2.addToSimulatorMapaSemantico(cli.sock, ipAddress, port)
cli.modeFrame(cli.sock, "ONDEMAND") # mode="CONTINUOUS" o "ONDEMAND"


while True:
    vecImgs=[]
    time.sleep(3)  # Simular el tiempo de proceso de iamgenes en algun algoritmo en python
    cli.advancedSimulation(cli.sock,timeWait)
    ## cam 1
    frame1=cam1.operator()
    if isinstance(frame1,np.ndarray):
        width, height = frame1.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame1)

    ## cam 2
    frame2=cam2.operator()
    if isinstance(frame2,np.ndarray):

        width, height = frame2.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame2)

    ## generate video wall image
    videowall = dibujarCanvas.makeCanvas(vecImgs, 960, 2)
    #videowall = makeCanvas(vecImgs, 960, 2)

    ## show image
    if videowall.shape[0]>0 and videowall.shape[1]>0:
        cv2.imshow("Video Wall", videowall) ## display frame

   ## close window & exit preview loop if ESC pressed
    if cv2.waitKey(5) == KEYESCAPE:
        break

# regresar a su estado original la velocidad del Simulador

# time.sleep(1) ## time in seconds

cam1.removeFromSimulator()
cam2.removeFromSimulator()

cli.modeFrame(cli.sock, "CONTINUOUS") # retornar el simulador a su funcionamiento continuo
cli.resetSimulator(cli.sock) # rest el simulador

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)