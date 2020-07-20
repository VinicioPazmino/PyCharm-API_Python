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
print("DEMO 1: CAMERA CONNECTIVITY\n")
print("This demo test basic functionality:\n")
print(" (1) connects the client to the simulator\n")
print(" (2) creates a camera you can you can use\n")
print(" (3) registers the camera in the simulator\n")
print(" (4) previews the camera content\n\n")


# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)


# if we want to ask for the existing cameras in the simulator

# std::vector<MSScam*> cams;
# cams.begin();
# cli.getAllCamerasFromSimulator(sock, cams);
# for (auto &cam : cams) // access by reference to avoid copying
# {
#   cam->print_details();
# }
# usleep(10000000); //time in microseconds
#

# create the camera
name = "demo1_test"+str(randint(0, 99))  # rand in the range 0 to 99;

# MSScam cam(name, 640, 480, 10); //initialization with default position/rotation

# cam = MSScam(name, 640, 480, 10, 10.38, -6.44, 5.0, 20.0, 10.0, 0.0)
cam = MSScam(name, 640, 480, 10, 0, 10, 0, 10, 123, 0.0)

cam.print_details()

# add the camera to the simulator
cam.addTosimulator(cli.sock, ipAddress, port)
cam.print_details()

# preview the camera for 10 secs
cam.preview(10)
cam.print_details()

# wait 1 sec before closing this demo
time.sleep(1)  # time in seconds

# unregistering camera
cam.removeFromSimulator()

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)

"""
input("\nPress any key to exit")
"""
# python testbasic.py -ip 150.244.57.171
