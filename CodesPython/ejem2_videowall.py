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


# Inicializar la pantalla de frame
dibujarCanvas=DrawDisplay()

sock = -1

# parse command line arguments (if any)
(ipAddress, port, cfgpath) = CLParser(sys.argv[1:len(sys.argv)])

# display demo information in console
print("RACameraDemo 2: VIDEO WALL (6 camaras)\n")
print(" (1) Conexion como cliente en el simulador")
print(" (2) Ejecutar script para un Simulador con minimo de 6 Camaras en Escenario")
print(" (3) Al objeto creado y registrado 'cam' acceder a la funcion 'setNameRACamera()' para visualzar las camaras  ")
print(" (4) Visualizar las camaras en una pared de pantallas")

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

numcam = MSScam()
numCam= numcam.readTosimulator(cli.sock, ipAddress, port)


name = "Demo2_VideoWall_" + str(randint(0, 99))
cam = MSScam(name, 640, 480)
cam.configRACamera(cli.sock, ipAddress, port)

print("Numero de camaras Disponibles "+ str(numCam))

if numCam == 0:
    print("No hay camaras moviles en el simulador")
else:
    i = 0
    while i < numCam:
        print("Acceder a las camaras con el nombre: "+ name+"_" + str(i))
        i += 1

while True:
    vecImgs=[]

    ## cam 1
    cam.setNameRACamera(name +"_0")
    frame1=cam.operator()
    if isinstance(frame1,np.ndarray):
        width, height = frame1.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame1)

    ## cam 2
    cam.setNameRACamera(name +"_1")
    frame2=cam.operator()
    if isinstance(frame2,np.ndarray):
        width, height = frame2.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame2)

    ## cam 3
    cam.setNameRACamera(name +"_2")
    frame3=cam.operator()
    if isinstance(frame3,np.ndarray):
        width, height = frame3.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame3)

    ## cam 4
    cam.setNameRACamera(name +"_3")
    frame4=cam.operator()
    if isinstance(frame4,np.ndarray):
        width, height = frame4.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame4)

    ## cam 5
    cam.setNameRACamera(name +"_4")
    frame5=cam.operator()
    if isinstance(frame5,np.ndarray):
        width, height = frame5.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame5)

    ## cam 6
    cam.setNameRACamera(name +"_5")
    frame6=cam.operator()
    if isinstance(frame6,np.ndarray):
        width, height = frame6.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame6)

    ## generate video wall image
    # videowall = makeCanvas(vecImgs, 480, 2)
    videowall = dibujarCanvas.makeCanvas(vecImgs, 480, 2)

    ## show image
    if videowall.shape[0]>0 and videowall.shape[1]>0:
        cv2.imshow("Video Wall Remote Acces Camera", videowall) ## display frame

   ## close window & exit preview loop if ESC pressed
    if cv2.waitKey(5) == KEYESCAPE:
        break

## wait 1 sec before closing this demo
time.sleep(1) ## time in seconds

cli.resetSimulator(cli.sock)
# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)
