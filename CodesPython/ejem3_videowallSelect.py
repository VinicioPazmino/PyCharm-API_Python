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
print("RACameraDemo 3: Seleccionar camaras para pantalla de displays (8 Display) \n")
print(" (1) Conexion como cliente en el simulador")
print(" (2) Ejecutar script para un Simulador con minimo de X Camaras en Escenario (se pude repetir)")
print(" (3) Escoger que camaras tener acceso para reproducir")
print(" (4) Visualizar las camaras en una pared de pantallas")



# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

numcam = MSScam()
numCam= numcam.readTosimulator(cli.sock, ipAddress, port)


name = "Demo3_SelectVideoWall_"+ str(randint(0, 99))
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

# Agregar al vector los nombres que el suusario selecciona segun el ID se deben agregar 8 camaras, se puede repetirclear
nombres = []
i = 0
while i < 8:
    selecID = input("Selccione el ID para agregar a la visualizacion: ")
    newName = name + "_" + selecID
    nombres.append(newName)
    #print("La lista es: " + newName)
    i += 1


while True:
    vecImgs=[]

    ## cam 1
    cam.setNameRACamera(nombres[0])
    frame1=cam.operator()
    if isinstance(frame1,np.ndarray):
        width, height = frame1.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame1)

    ## cam 2
    cam.setNameRACamera(nombres[1])
    frame2=cam.operator()
    if isinstance(frame2,np.ndarray):
        width, height = frame2.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame2)

    ## cam 3
    cam.setNameRACamera(nombres[2])
    frame3=cam.operator()
    if isinstance(frame3,np.ndarray):
        width, height = frame3.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame3)

    ## cam 4
    cam.setNameRACamera(nombres[3])
    frame4=cam.operator()
    if isinstance(frame4,np.ndarray):
        width, height = frame4.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame4)

    ## cam 5
    cam.setNameRACamera(nombres[4])
    frame5=cam.operator()
    if isinstance(frame5,np.ndarray):
        width, height = frame5.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame5)

    ## cam 6
    cam.setNameRACamera(nombres[5])
    frame6=cam.operator()
    if isinstance(frame6,np.ndarray):
        width, height = frame6.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame6)

    # cam 7
    cam.setNameRACamera(nombres[6])
    frame6 = cam.operator()
    if isinstance(frame6, np.ndarray):
        width, height = frame6.shape[:2]
        if width > 0 and height > 0:
            vecImgs.append(frame6)

    # cam 8
    cam.setNameRACamera(nombres[7])
    frame6 = cam.operator()
    if isinstance(frame6, np.ndarray):
        width, height = frame6.shape[:2]
        if width > 0 and height > 0:
            vecImgs.append(frame6)

    ## generate video wall image
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
