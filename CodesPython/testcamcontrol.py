##
#  This demo is a client that connect to Unity Simulator and
# (1) connects the client to the simulator
# (2) creates a camera you can you can use
# (3) registers the camera in the simulator
# (4) moves the camera (position, rotation,..)
# (5) previews the camera content
##

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
print("DEMO: CAMERA MOTION EXTENDED\n")
print("This demo test basic functionality:\n")
print(" (1) connects the client to the simulator\n")
print(" (2) creates a camera you can you can use\n")
print(" (3) registers the camera in the simulator\n")
print(" (4) activates GUI to move the camera\n")
print(" (5) previews the camera content\n\n")

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

# create the camera
# initialization for a specific parameters (position, rotation, TX/RX)
# cam = MSScam("demo4_test_ext", 640, 480, 20, 10.38, -6.44, 5.0, 20.0, 10.0, 0.0)
#cam = MSScam("demo4_test_ext", 640, 480, 10, 0, 0, 0, 0.0, 0.0, 0.0) # EPS LITE

cam = MSScam("demo4_test_ext", 640, 480, 10, -103.5, 10.7, -147.9, 10.0, 25.0, 0.0)

# add the camera to the simulator
cam.addTosimulator(cli.sock, ipAddress, port)

# start GUI control of the camera
cam.GUIcontrol()

# display the coordinates
cam.print_details()

# wait 1 sec before closing this demo
time.sleep(1)  # time in seconds

# unregistering camera
cam.removeFromSimulator()

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)
