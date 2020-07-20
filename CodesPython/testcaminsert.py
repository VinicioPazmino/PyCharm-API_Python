"""
#  This demo is a client that connect to Unity Simulator and
#    (1) connects the client to the simulator
#	(2) creates a camera you can you can use
#	(3) registers the camera in the simulator
#	(4) moves the camera (position, rotation,..)
#	(5) previews the camera content
"""
import sys
from functions.MSScam import *
from functions.MSSclient import *
from functions.MSScam_control import *
from utils.MSSutils import *
from utils.CLParser import *
from utils.PropertyFileReader import *
import socket
from random import randint

sock = -1
# parse command line arguments (if any)
(ipAddress, port, cfgpath) = CLParser(sys.argv[1:len(sys.argv)])

# display demo information in console

print("DEMO : CAMERA MOTION EXTENDED\n")
print("This demo test basic functionality:\n")
print(" (1) connects the client to the simulator\n")
print(" (2) createS a camera you can you can use\n")
print(" (3) user the GUI to position the camera in the simulator\n")
print(" (4) registers the camera in the simulator\n")
print(" (5) previews\n")
print(" (6) previews the camera content\n\n")


# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

# create the camera	+str(randint(0,100))

cam = MSScam("demo5_test_2", 640, 480, 10)  # initialization for a specific parameters (position, rotation, TX/RX)

# start GUI control of the camera
cam.GUIinsert(cli.sock)

# add the camera to the simulator
cam.addTosimulator(cli.sock, ipAddress, port)
cam.preview(10)

# display the coordinates
# cam.print_details()

# wait 1 sec before closing this demo
time.sleep(1)  # time in seconds

# unregistering camera
cam.removeFromSimulator()

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)

