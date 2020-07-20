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
print("RACameraDemo 4: Leer Camaras y Eliminar del Simulador\n")
print(" (1) Conexion como cliente en el simulador")
print(" (2) Registrar objeto 'cam' en el simulador para tener acceso a las funciones")
print(" (3) Identificar numero de camaras en el simulador")
print(" (4) Seleccionar ID de camara para visualizar video")
print(" (5) Escoger ID de camara para remover del simulador")
print(" (6) ESC para finalizar ejecucion")


# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

numcam = MSScam()
numCam= numcam.readTosimulator(cli.sock, ipAddress, port)

name = "Demo4_AccesoRemotoRemover_"+ str(randint(0, 99))
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
            cam.preview(10)
            # wait 1 sec before closing this demo
            # time.sleep(1)  # time in seconds
            # close window & exit preview loop if ESC pressed
            if cv2.waitKey(5) == KEYESCAPE:
                break

nombresCam = []
i = 0
while i < numCam:
    newName = name + "_" + str(i)
    nombresCam.append(newName)
    i += 1

print(nombresCam)
bandera= True
while bandera:
    i = 0
    while i <= len(nombresCam):
        selecID = input("\nSelccione el ID de la camara para eliminarla [s - para salir] : ")
        if selecID == "s":
            bandera = False
            break
        else:
            newName = name + "_" + selecID
            nombresCam.remove(newName)
            cam.setNameRACamera(newName)
            cam.removeCameraSceneSimulator()
            print("\nCamara: "+newName+" Borrada")
            print(nombresCam)
            # wait 1 sec before closing this demo
            # time.sleep(1)  # time in seconds
            # close window & exit preview loop if ESC pressed
            if cv2.waitKey(5) == KEYESCAPE:
                break

#cam.setNameRACamera(name+"_0")
#cam.preview(10)

#cam.setNameRACamera(name+"_1")
#cam.preview(10)

# unregistering camera
# cam.removeFromSimulator()

# resetear transmision de camaras corrienddo en el simulador
cli.resetSimulator(cli.sock)

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)
