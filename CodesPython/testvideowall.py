##
  # This demo is a client that connect to Unity Simulator and
  # (1) connects the client to the simulator
  # (2) creates 6 cameras
  # (3) registers the cameras in the simulator
  # (4) previews the cameras in a videowall
##
import sys
from functions.MSScam import *
from functions.MSSclient import *
from utils.MSSutils import *
from utils.CLParser import *
import socket
import numpy as np
from math import *
from random import randint

##
# @brief makeCanvas Makes composite image from the given images
# @param vecMat Vector of Images.
# @param windowHeight The height of the new composite image to be formed.
# @param nRows Number of rows of images. (Number of columns will be calculated
#              depending on the value of total number of images).
# @return new composite image.
##
from utils.DrawDisplay import*

dibujarCanvas=DrawDisplay()
sock = -1

## parse command line arguments (if any)
(ipAddress,port,cfgpath)=CLParser(sys.argv[1:len(sys.argv)])

## display demo information in console
print("DEMO: VIDEO WALL\n")
print("This demo test basic functionality:\n")
print(" (1) connects the client to the simulator\n")
print(" (2) creates 6 cameras\n")
print(" (3) registers the cameras in the simulator\n")
print(" (4) previews the cameras in a video wall\n")

##initialize client
cli=MSSclient()
cli.connectTosimulator(ipAddress, port, sock);


##create camera 1
name = "demo1_test"+str(randint(0,999)) ## rand in the range 0 to 999;
#cam1 = MSScam(name, 320, 240, 10, -8.7, -6.13, 5.96, 10.0, 50.0, 0.0) # EPS LITE
cam1 = MSScam(name, 320, 240, 10, 1, 15, 0, 10, 115, 0.0)
cam1.addTosimulator(cli.sock,ipAddress, port)

## create camera 2
name = "demo1_test"+str(randint(0,999)) ## rand in the range 0 to 999;
# cam2 = MSScam(name, 320, 240, 10, -11.38, -5.8, 27.0, 20.0, 90.0, 0.0) # EPS LITE
cam2 = MSScam(name, 320, 240, 10, -100.5, 30.0, -41.5, 15.0, 45.0, 0.0)
cam2.addTosimulator(cli.sock,ipAddress, port)

## create camera 3
name = "demo1_test"+str(randint(0,999)) ## rand in the range 0 to 999;
# cam3 = MSScam(name, 320, 240, 10, 10.70, -6.42, 38.85, 10.0, 180.0, 0.0) # EPS LITE
cam3 = MSScam(name, 320, 240, 10, 27.77, 6.1, -117.35, 0, 1.0, 0.0)
cam3.addTosimulator(cli.sock,ipAddress, port)

## create camera 4
name = "demo1_test"+str(randint(0,999)) ## rand in the range 0 to 999;
# cam4 = MSScam(name, 320, 240, 10, 36.11, -5.25, 43.65, 10.0, 257.0, 0.0) # EPS LITE
cam4 = MSScam(name, 320, 240, 10, 27.7, 14.42, 62.42, 3.5, 180.0, 0.0)
cam4.addTosimulator(cli.sock,ipAddress, port)

## create camera 5
name = "demo1_test"+str(randint(0,999)) ## rand in the range 0 to 999;
#cam5 = MSScam(name, 320, 240, 10, 29.0, -5.95, 26.79, 10.0, -90.0, 0.0) # EPS LITE
cam5 = MSScam(name, 320, 240, 10, -114.5, 13.7, -31.89, 10.0, 60.0, 0.0)
cam5.addTosimulator(cli.sock,ipAddress, port)

## create camera 6
name = "demo1_test"+str(randint(0,999)) ## rand in the range 0 to 999;
#cam6 = MSScam(name, 320, 240, 10, 25.31, -6.6, 9.87, 10.0, -90.0, 0.0) # EPS LITE
cam6 = MSScam(name, 320, 240, 10, -171.9, 5.9, -26.5, 3.5, 45.0, 0.0)
cam6.addTosimulator(cli.sock,ipAddress, port)




## preview cameras
while True:
    vecImgs=[]

    ## cam 1
    frame1=cam1.operator()
    if isinstance(frame1,np.ndarray):
        width, height = frame1.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame1)

    ## cam 2
    frame2=cam2.operator()
    if isinstance(frame2,np.ndarray):
        width, height = frame2.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame2)

    ## cam 3
    frame3=cam3.operator()
    if isinstance(frame3,np.ndarray):
        width, height = frame3.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame3)

    ## cam 4
    frame4=cam4.operator()
    if isinstance(frame4,np.ndarray):
        width, height = frame4.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame4)

    ## cam 5
    frame5=cam5.operator()
    if isinstance(frame5,np.ndarray):
        width, height = frame5.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame5)

    ## cam 6
    frame6=cam6.operator()
    if isinstance(frame6,np.ndarray):
        width, height = frame6.shape[:2]
        if width>0 and height>0:
            vecImgs.append(frame6)

    ## generate video wall image
    #videowall = makeCanvas(vecImgs, 480, 2)
    videowall = dibujarCanvas.makeCanvas(vecImgs, 480, 2)



    ## show image
    if videowall.shape[0]>0 and videowall.shape[1]>0:
        cv2.imshow("Video Wall", videowall) ## display frame

   ## close window & exit preview loop if ESC pressed
    if cv2.waitKey(5) == KEYESCAPE:
        break

## wait 1 sec before closing this demo
time.sleep(1) ## time in seconds

## unregistering cameras
cam1.removeFromSimulator()
cam2.removeFromSimulator()
cam3.removeFromSimulator()
cam4.removeFromSimulator()
cam5.removeFromSimulator()
cam6.removeFromSimulator()

## disconnect from the simulator
cli.disconnectFromSimulator(cli.sock)





