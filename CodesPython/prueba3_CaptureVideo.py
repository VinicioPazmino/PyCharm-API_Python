import sys
from functions.MSSclient import *
from utils.MSSutils import *
from utils.CLParser import *
import socket
from random import randint
from functions.MSScam import *
import numpy as np
from math import *
import cv2
from utils.DrawDisplay import*

dibujarCanvas=DrawDisplay()
sock = -1

# parse command line arguments (if any)
(ipAddress, port, cfgpath) = CLParser(sys.argv[1:len(sys.argv)])

# display demo information in console
print("Mapa Semantico Demo 1: Doble Pantalla (2 camaras)\n")
print(" (1) Conexion como cliente en el simulador")
print(" (2) Crear 2 objetos Camera con identicas posiciones y ubicaciones ")
print(" (3) Agregar al simulador independientemente, la segunda con el comando(filtro) mapa semantico ")
print(" (4) Llamada a la funcion preview para visualizar las camaras en una VideoWall")
print(" (4) Press ESC para finalziar y desconectar el cliente")

#nameCapute1 = "SecuenciaVideo6_RGB.avi"
nameCapute1 = "Video_RGB"+str(randint(0, 99))+".avi"
salida1 = cv2.VideoWriter(nameCapute1,cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))

#nameCapute2 = "secuenciaVideo6_Semantica.avi"
nameCapute2 = "Video_MapaSemantico"+str(randint(0, 99))+".avi"
salida2 = cv2.VideoWriter(nameCapute2,cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

# create the camera
name = "demo1_MapaSemantico"+str(randint(0, 99))  # rand in the range 0 to 99;
# cam1 = MSScam(name, 640, 480, 10, 0, 10, 0, 10, 123, 0.0) # cam = MSScam("demo2_test", 640, 480, 10, posX, posY, posZ, rotX, rotY, rotZ)
cam1 = MSScam(name, 640, 480, 10, -136, 2, 66, 0, 90, 0.0)
#cam1 = MSScam(name, 640, 480, 10, 26, 2, -13, 0, 270, 0.0)
cam1.addTosimulator(cli.sock, ipAddress, port)

# Crear la misma camara con parametros dienticos
name = "demo1_MapaSemantico"+str(randint(0, 99))  # rand in the range 0 to 99;
# cam2 = MSScam(name, 640, 480, 10, 0, 10, 0, 10, 123, 0.0)
cam2 = MSScam(name, 640, 480, 10, -136, 2, 66, 0, 90, 0.0)
#cam2 = MSScam(name, 640, 480, 10, 26, 2, -13, 0, 270, 0.0)
cam2.addToSimulatorMapaSemantico(cli.sock, ipAddress, port)

while True:
    vecImgs=[]

    ## cam 1
    frame1=cam1.operator()
    salida1.write(frame1)
    if isinstance(frame1,np.ndarray):
        width, height = frame1.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame1)

    ## cam 2
    frame2=cam2.operator()
    salida2.write(frame2)
    if isinstance(frame2,np.ndarray):
        width, height = frame2.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame2)

    ## generate video wall image
    # videowall = makeCanvas(vecImgs, 960, 2)
    videowall = dibujarCanvas.makeCanvas(vecImgs, 960, 2)

    ## show image
    if videowall.shape[0]>0 and videowall.shape[1]>0:
        cv2.imshow("Video Wall", videowall) ## display frame

   ## close window & exit preview loop if ESC pressed
    if cv2.waitKey(5) == KEYESCAPE:
        break
salida1.release()
salida2.release()

time.sleep(1) ## time in seconds


cam1.removeFromSimulator()
cam2.removeFromSimulator()
# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)