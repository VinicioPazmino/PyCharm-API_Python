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
print("RACameraDemo 5: Control de camaras en Ecenario \n")
print(" (1) Este test interactua y controla Posicion y Rotacion de Camaras en escena:")
print(" (2) FIXED CAMERA:   Rotacion Bloqueada  - Movimiento Bloqueada")
print(" (3) MOBILE CAMERA:  Rotacion Habilitada - Movimiento Habilitada")
print(" (4) PTZ CAMERA:     Rotacion Habilitada - Movimiento Bloqueada ")

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

numcam = MSScam()
numCam= numcam.readTosimulator(cli.sock, ipAddress, port)

name = "Demo5_ControlAccesoRemoto_" + str(randint(0, 99))
#cam = MSScam(name, 640, 480, 10, 0)
cam = MSScam(name, 640, 480)
cam.configRACamera(cli.sock, ipAddress, port)

print("Numero de camaras "+ str(numCam))

if numCam == 0:
    print("No hay camaras moviles en el simulador")
else:
    while True:
        i = 0
        while i < numCam:
            print("ID de Camaras: " + str(i))
            i += 1

        selecID = input("Selccione el ID de la camara para acceder [s - para salir] : ")
        if selecID == "s":
            break
        else:
            newName = name + "_" + selecID
            cam.setNameRACamera(newName)
            cam.GUIcontrolRACam()
            cam.print_details()
            # wait 1 sec before closing this demo
            # time.sleep(1)  # time in seconds
            # close window & exit preview loop if ESC pressed
            if cv2.waitKey(5) == KEYESCAPE:
                break



# resetear transmision de camaras corrienddo en el simulador
cli.resetSimulator(cli.sock)

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)