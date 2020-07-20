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
print("RACameraDemo 1: Leer Camaras en Escenario\n")
print(" (1) Conexion como cliente en el simulador")
print(" (2) Leer el numero de camaras existentes en la escena del simulador")
print(" (3) Asignar nombre y un numero random a las camaras seguido de ID ordenadamente NOMBRE_RAND_ID")
print(" (4) Seleccionar por teclado el ID [0 - numCam] para visualizar contenido de la Camara\n")

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

InitialConstructor = MSScam()
numCam= InitialConstructor.readTosimulator(cli.sock, ipAddress, port) # La funcion .readTosimulator return numero de camaras en Unity


name = "Demo1_AccesoRemoto_" + str(randint(0, 99))
cam = MSScam(name, 1024, 512, 10)
#cam = MSScam(name, 640, 480)
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
            cam.preview(20)
            # wait 1 sec before closing this demo
            # time.sleep(1)  # time in seconds
            # close window & exit preview loop if ESC pressed
            if cv2.waitKey(5) == KEYESCAPE:
                break


#cam.setNameRACamera(name+"_0")
#cam.preview(10)

# unregistering camera
# cam.removeFromSimulator()

# resetear transmision de camaras corrienddo en el simulador
cli.resetSimulator(cli.sock)

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)
