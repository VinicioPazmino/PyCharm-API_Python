##
#  This demo is a client that connect to Unity Simulator and
#  (1) creates a camera you can you can use.
#  (2) registers the camera in the simulator and previews it
#  (3) changes the FPS and previews
#  (4) changes the JPEG quality and previews  
#  (5) deletes the camera and disconnects from simulator
##
import sys
from functions.MSScam import *
from functions.MSSclient import *
from utils.MSSutils import*
from utils.PropertyFileReader import *
import socket
from random import randint

port = 8889
# port=-1
sock = -1
ipAddress = "150.244.57.171"
cfgpath="./config.ini"

# parse command line arguments (if any)
if len(sys.argv) > 2:
	port = sys.argv[1]
	ipAddress = sys.argv[2]
	cfgpath = sys.argv[3]

# display demo information in console
print("DEMO3: SAVE & LOAD A CAMERA\n")
print("This demo test basic functionality:\n")
print("(1) creates a camera you can you can use\n")
print("(2) registers the camera in the simulator and previews it\n")
print("(3) changes the FPS and previews\n")
print("(4) changes the JPEG quality and previews\n")
print("(5) deletes the camera and disconnects from simulator\n")

# read application settings
print("\nReading sever configuration (IP & port) from config file %s" % cfgpath)
filereader = PropertyFileReader(cfgpath, False)
(found, value) = filereader.getProperty("SIMULATOR_IP")
if found:
	ipAddress = str(value)
(found, value) = filereader.getProperty("SIMULATOR_PORT")
if found:
	port=int(value)

# initialize client
cli = MSSclient()
cli.connectTosimulator(ipAddress, port, sock)

# create the camera
# cam = MSScam("demo3_test", 640, 480, 10, 15.0, -3.0, 5.0, 20.0, 10.0, 0.0) # EPS LITE
cam = MSScam("demo3_test", 640, 480, 10, -108.5, 20.0, -31.5, 15.0, 45.0, 0.0)

# add the camera to the simulator
cam.addTosimulator(cli.sock, ipAddress, port)

# preview the camera for 10 secs
cam.preview(10)  # time in seconds

# preview the camera for 10 secs
cam.setFPS(1)
cam.preview(10)  # time in seconds

# set PNG images (lossless codec) and preview camera for 10 secs
cam.setTXRXformat(CAM_PNG)  # 0 = jpg, 1 = png,
cam.preview(10)  # time in seconds

# set JPEG quality to low and preview camera for 10 secs
cam.setTXRXformat(CAM_JPEG)  # 0 = jpg, 1 = png,
cam.setJPEGquality(25)
cam.preview(10)  # time in seconds

# set JPEG quality to low and preview camera for 10 secs
cam.setTXRXformat(CAM_JPEG)  # 0 = jpg, 1 = png,
cam.setJPEGquality(95)
cam.preview(10)  # time in seconds

# wait 1 sec before closing this demo
time.sleep(1)  # time in seconds

# unregistering camera
cam.removeFromSimulator()

# disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)