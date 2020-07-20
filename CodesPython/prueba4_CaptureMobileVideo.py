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

# Quitar las dos lineas de comentario y  comentar la funcion --> def makeCanvas
# from utils.DrawDisplay import*
# dibujarCanvas=DrawDisplay()

def makeCanvas(vecMat, windowHeight, nRows):
    N=len(vecMat)
    nRows=min(N,nRows)
    edgeThickness=10
    imagesPerRow=int(ceil(float(N)/nRows))
    resizeHeight=floor(2.0 * ((floor(float(windowHeight - edgeThickness) / nRows)) / 2.0)) - edgeThickness
    resizeWidth=[]
    for i in range(0,N):
        resizeWidth.append(float(resizeHeight)/vecMat[i].shape[0]*vecMat[i].shape[1])
        maxresizeWidth=int(max(resizeWidth))
        windowWidth=imagesPerRow*(maxresizeWidth+edgeThickness)+edgeThickness
        canvasImage=np.zeros((int(windowHeight),int(windowWidth),3),np.uint8)
    for k in range(0,N):
        currentImage_pil=Image.fromarray(np.uint8(vecMat[k]))
        currentImage_pil=currentImage_pil.resize((int(resizeWidth[k]),int(resizeHeight)))
        currentImage=np.array(currentImage_pil)
        i=k//imagesPerRow
        j=k%imagesPerRow
        currentHeight=i*(resizeHeight+edgeThickness)+edgeThickness
        currentWidth=j*(maxresizeWidth+edgeThickness)+edgeThickness
        canvasImage[int(currentHeight):int(currentHeight+resizeHeight),int(currentWidth):int(currentWidth+resizeWidth[k])]=currentImage
    return canvasImage


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

nameCapute1 = "SecuenciaAutoBus_RGB.avi"
#nameCapute1 = "AppTFM_RGB"+str(randint(0, 99))+".avi"
salida1 = cv2.VideoWriter(nameCapute1,cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))

nameCapute2 = "secuenciaAutoBus_Semantica.avi"
#nameCapute2 = "AppTFM_MapaSemantico"+str(randint(0, 99))+".avi"
salida2 = cv2.VideoWriter(nameCapute2,cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))



# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

numcam = MSScam()
numCam= numcam.readTosimulator(cli.sock, ipAddress, port)

name = "Prueba4_SelectVideoWall_CaptureVideo"+ str(randint(0, 99))
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
while i < 2:
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
    salida1.write(frame1)
    if isinstance(frame1,np.ndarray):
        width, height = frame1.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame1)

    ## cam 2
    cam.setNameRACamera(nombres[1])
    frame2=cam.operator()
    salida2.write(frame2)
    if isinstance(frame2,np.ndarray):
        width, height = frame2.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame2)

    ## generate video wall image
    videowall = makeCanvas(vecImgs, 960, 2) # comentar si se usa las dos lienas de arriba
    # videowall = dibujarCanvas.makeCanvas(vecImgs, 960, 2) # usar si se descomenta las dos lineas de de arriba

    ## show image
    if videowall.shape[0]>0 and videowall.shape[1]>0:
        cv2.imshow("Video Wall", videowall) ## display frame

   ## close window & exit preview loop if ESC pressed
    if cv2.waitKey(5) == KEYESCAPE:
        break
salida1.release()
salida2.release()

time.sleep(1) ## time in seconds

cli.resetSimulator(cli.sock)
# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)