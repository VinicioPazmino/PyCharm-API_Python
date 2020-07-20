##
#  This demo is a client that connect to Unity Simulator and
#  (1) creates a camera you can you can use.
#  (2) registers the camera in the simulator and previews it
#  (3) saves the camera in a TXT file
#  (4) loads a new camera from this TXT file
#  (5) registers and previews the new camera
##
import sys
from functions.MSScam import *
from functions.MSSclient import *
from utils.MSSutils import*
from utils.PropertyFileReader import *
from utils.CLParser import *
import socket
from random import randint


sock = -1

# parse command line arguments (if any)
(ipAddress, port, cfgpath) = CLParser(sys.argv[1:len(sys.argv)])

# display demo information in console
print ("DEMO: SAVE & LOAD A CAMERA\n")
print ("This demo test basic functionality:\n")
print (" (1) creates a camera you can you can use\n")
print (" (2) registers the camera in the simulator and previews it\n")
print (" (3) saves the camera in a TXT file\n")
print (" (4) loads a new camera from this TXT file\n")
print (" (5) registers and previews the new camera\n\n")

# read application settings
print("\nReading sever configuration (IP & port) from config file %s" % cfgpath)
filereader=PropertyFileReader(cfgpath, False)
(found, value) = filereader.getProperty("SIMULATOR_IP")
if found:
	ipAddress = str(value)
(found, value) = filereader.getProperty("SIMULATOR_PORT")
if found:
	port = int(value)

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

# create the camera
#cam = MSScam("demo2_test", 640, 480, 10, posX, posY, posZ, rotX, rotY, rotZ)

cam = MSScam("demo2_test1", 640, 480, 10, 69.7, 10.8, -80.1, 5, 8.5, 0.0)
#cam = MSScam("demo2_test2", 640, 480, 10, 63, 10, -80, 0.0, 0.0, 0.0)


# add the camera to the simulator
cam.addTosimulator(cli.sock, ipAddress, port)

# preview the camera for 10 secs
cam.preview(10)  # time in seconds

# wait 1 sec before closing this demo
time.sleep(1)  # time in seconds

# unregistering camera
cam.removeFromSimulator()

# save camera details
cam.saveTofile("./resources/camera1new.txt")
	
# load camera from file and preview
cam1 = MSScam("./resources/camera1new.txt")
cam1.addTosimulator(cli.sock, ipAddress, port)
cam1.preview(10)  # time in microseconds

# wait 1 sec before closing this demo
time.sleep(1)  # time in seconds

cam1.removeFromSimulator()

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)
