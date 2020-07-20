import sys
import cv2
from PIL import Image
import numpy as np
import imutils
from utils.MSSutils import *
from functions.MSScam import *
from functions.MSSclient import *
import socket
from random import randint


class MiniMapInfo:
    def __init__(self):
        # float pointXCamRelative;	///< axis X on image plane (minimap image) -> X-axis on 3D world space
        # float pointYCamRelative;	///< axis Y on image plane (minimap image) -> Z-axis on 3D world space
        # float heightCamRelative;	///< axis X on image plane (minimap image) -> Y-axis on 3D world space
        # cv::Mat *source;			///< minimap image
        # cv::Mat *icon;			///< camera icon which is overlayed in the minimap
        # cv::Mat *dst;				///< composed image with source and icon images
        # int angleCam;				///< rotation angle in image plane (zenital view, minimap image) -> X-axis rotation on 3D world space
        # int heightAngleCam;		///< rotation angle in image plane (lateral view) -> Y-axis rotation on 3D world space
        # bool positionFixed;
        # bool heightFixed;
        # int lengthImage;
        # float xMinAbsolute;		///< minimum value for axis X on 3D world space
        # float xMaxAbsolute;		///< maximum value for axis X on 3D world space
        # float yMinAbsolute;		///< minimum value for axis Y on 3D world space
        # float yMaxAbsolute;		///< maximum value for axis X on 3D world space
        # float floorAbsolute;		///< value for floor location (axis Y on 3D world space)
        # float ceilingAbsolute;	///< value for ceiling location (axis Y on 3D world space)
        self.heightFixed = False
        self.positionFixed = False
        self.heightAngleCam = 0
        self.heightCamRelative = 0
        self.angleCam = 0
        self.pointXCamRelative = -1
        self.pointYCamRelative = -1
        self.createMiniMapInfo()

    ## \brief inizialite MiniMap
    #
    # \define MiniMap Info fields
    #

    def createMiniMapInfo(self):
        pass


##
#	\brief Callback method to detect CLICK events on the displayed map of the scene (zenital view). It gets the X-Z location of the camera in the MSS simulation.
#
#	\param event Type of the event
#	\param x X-coordinate of the CLICK event
#	\param y Y-coordinate of the CLICK event
#	\param flags Additional information of the event (not used)
#	\param data the MiniMapInfo structure
# /
def OnClickMap(event, x, y, flags, data):
    global imagesMap
    imagesMap = data

    if not imagesMap.positionFixed:
        imagesMap.pointXCamRelative = float(x)
        imagesMap.pointYCamRelative = float(y)

    if event == cv2.EVENT_LBUTTONDOWN:
        imagesMap.positionFixed = True



##
#	\brief Callback method to detect CLICK events on the displayed map of the scene (lateral view). It gets the height (Y-axis) of the camera in the MSS simulation.
#
#	\param event Type of the event
#	\param x X-coordinate of the CLICK event
#	\param y Y-coordinate of the CLICK event
#	\param flags Additional information of the event (not used)
#	\param data Pointer to the MiniMapInfo structure
# /

def OnClickHeightMap(event, x, y, flags, data):
    global imagesMap
    imagesMap = data

    if not imagesMap.heightFixed:
        if y > 650:
            y = 650
        elif y < 95:
            y = 95
        imagesMap.heightCamRelative = float(y)

    if event == cv2.EVENT_LBUTTONDOWN:
        imagesMap.heightFixed = True


##
#	\brief Default class constructor with default parameters
# /
class MSScam_insert:
    def __init__(self):
        self.posX = -1
        self.posY = -1
        self.posZ = -1
        self.rotX = -1
        self.rotY = -1
        self.rotZ = -1

    ##
    #	\brief Method to start the interactive insertion of the camera
    #
    #	\param socket Connection socket to determine the TCP/IP connection to the server
    #	\param cam the MSS camera which is going to be inserted
    #
    #	\return Operation code > 0 if success (-1 if failed)
    # /
    def start(self, socket, cam_in):
        global cam
        global imagesMap
        cam = cam_in
        cam.sock = socket

        ## initialization
        imagesMap = MiniMapInfo()  ## create structure
        if self.getMiniMapInfoServer(cam.sock) == -1:
            return -1  ## ask server for details

        ##receive the minimap from server
        minimap = self.receiveMap(cam.name, False)
        if not (minimap.shape[0] > 0 and minimap.shape[1] > 0):
            return -1
        # Data Conversion for further treatment with transparent background
        pil_im_rgb = Image.fromarray(cv2.cvtColor(minimap, cv2.COLOR_BGR2RGB))
        np_im_rgb = np.asarray(pil_im_rgb)
        np_im_rgba = 255 * np.ones((np_im_rgb.shape[0], np_im_rgb.shape[1], np_im_rgb.shape[2] + 1))
        np_im_rgba[:, :, :-1] = np_im_rgb
        imagesMap.source = Image.fromarray(np.uint8(np_im_rgba))

        ## step 1 - ground-plane positioning
        if (self.showMiniMap()) == -1:
            return -1

        ## step 2 - camera height
        if (self.showCameraScheme()) == -1:
            return -1

        ##coordinates conversion & update
        self.posX = self.coordinateConversion(imagesMap.xMinAbsolute, imagesMap.xMaxAbsolute,
                                              1 - imagesMap.pointXCamRelative)  ## left/right
        self.posY = self.coordinateConversion(imagesMap.floorAbsolute, imagesMap.ceilingAbsolute,
                                              imagesMap.heightCamRelative)  ## height
        self.posZ = self.coordinateConversion(imagesMap.yMinAbsolute, imagesMap.yMaxAbsolute,
                                              imagesMap.pointYCamRelative)  ## forward/backward
        self.rotX = float(imagesMap.heightAngleCam)
        self.rotY = float(-imagesMap.angleCam)

        return 1

    ##
    #	\brief Method to read an image provided by the MSS server describing the scenario (zenital view)
    #		   Solution based on http://stackoverflow.com/questions/10011098/how-to-receive-the-large-data-using-recv
    #
    #	\param verbose FLAG to get additional information through the command window
    #
    #	\return Operation code > 0 if success (-1 if failed)
    # /
    def receiveMap(self, name, verbose):
        # Timeout for socket
        global cam
        timeout = 1e-2
        cam.sock.settimeout(timeout)

        mapout = np.zeros((0, 0, 3), np.uint8)

        ## ask server for minimap image
        command = "GETMINIMAP-%s$" % name
        if cam.sock.send(command.encode('utf-8'), 0) < 0:  # necesita enviarse el command de tipo byte y no string python 3.x
        # if cam.sock.send(command, 0) < 0:                # python 2.x TypeError: a bytes-like object is required, not 'str'
            return mapout

        ## huge timeout to wait server to prepare response, 1 s
        timeout = 1
        cam.sock.settimeout(timeout)

        iByteCount = 0  ## counter for the bytes received
        smallbuf = cam.sock.recv(10000, 0)
        if verbose:
            print("\nBytes received at first: %d" % (len(smallbuf)))
        recvBytes = len(smallbuf)
        if recvBytes <= 0:
            return mapout

        ## message is divide in frame length + frame, so we split
        chars_array = smallbuf.split(b'#')  # dividir entre bytes python 3.x
        # chars_array = smallbuf.split("#")   # hacer split a un byte en python 2.x
        if len(chars_array) > 1:
            buf = chars_array[1]
            bytestorecv = int(chars_array[0])
            if verbose:
                print("Bytes to recv: " + str(bytestorecv))
        else:
            print("Data not fully received")
            return -1
        recvBytes = len(buf)
        iByteCount += recvBytes

        ## fast timeout to read socket fast, 1 ms
        timeout = 1
        cam.sock.settimeout(timeout)

        nrecep = 1
        while iByteCount < bytestorecv:
            smallbuf = cam.sock.recv(10000)
            recvBytes = len(smallbuf)

            if recvBytes > 0:
                ##make sure we're not about to go over the end of the buffer
                if iByteCount + recvBytes > BUFFER_FRAME_DEF:
                    break

                buf += smallbuf
                iByteCount += recvBytes

                if verbose:
                    print("Num of receptions: " + str(nrecep))
                    print("Bytes received: %d\n" % recvBytes)
                    print("Total bytes received: %d\n" % (len(buf)))

                nrecep += 1

            elif recvBytes == 0:
                if iByteCount + recvBytes != BUFFER_FRAME_DEF:
                    ##do process with received data
                    if verbose:
                        print("received frame")
                else:
                    if verbose:
                        print("receive failed")
                        break

            else:
                if verbose:
                    print("recv failed: possibly all data has been received ")
                break
        if verbose:
            print("Total bytes received: %d\n" % (len(buf)))

        length4 = int(math.ceil(math.log(len(buf)) * math.log(4)) ** 4)
        buf = buf + b'=' * (length4 - len(buf))  # se hace concatenacion de buf tipo byte con b'=' tipo byte python 3.x
        # buf = buf + "=" * (length4 - len(buf))  # TypeError: can't concat str to bytes en python 2.x buf es tipo byte y "=" es tipo string
        s = base64.b64decode(buf)  # decodificar en base 64 sintaxis para pytho 3.x
        #s = buf.decode('base64')   # sintaxis para python 2.x

        data = np.fromstring(s, dtype=np.uint8)
        mapout = cv2.imdecode(data, 1)

        return mapout

    ## \brief Method to convert between a point selected on local coordinates (width,height) and point on world Unity coordinates (XYZ)
    #
    # \param min minimum world Unity coordinate
    # \param max minimum world Unity coordinate
    # \param pointRelative point selected on local coordinates
    #
    # \return The converted coordinate
    #
    # /
    def coordinateConversion(self, mini, maxi, pointRelative):
        vector = abs(maxi - mini)
        desp = vector * (1 - pointRelative)
        return float(mini + desp)

    ## \brief This function receives from MSSserver info that will be used for
    #          visual insertion cameras.
    #
    # \param sock socket with connection to VMCS
    # \param info pointer to MiniMapInfo struct
    # \return Operation code > 0 if success(-1 if failed)
    #
    # /
    def getMiniMapInfoServer(self, sock):
        i = 0
        global imagesMap
        message = "GETMINIMAPINFO-$"
        if sock.send(message.encode('utf-8'), 0) < 0:  # necesita enviarse el command de tipo byte y no string python 3.x
            # if (sock.send(message, 0) < 0):				#TypeError: a bytes-like object is required, not 'str' python 2.x
            print("Send failed")
            return -1
        sock.settimeout(1)
        ## Receive data from the server
        message = sock.recv(100, 0)
        message = message.rstrip(b'\0')  # reemplazar la instruccion de replace para quitar el '\x00' para python 3.x
        # message=message.replace("\0","")		# instruccion de python 2.x
        length = len(message)
        if length < 0:
            print("recv failed\n")
            return -1

        ##process each element of the reply
        message = message.decode('utf-8')   # Se convierte de byte a string
        #chars_array = message.split(b'/')  # se indica que haga split entre bytes en python 3.x
        chars_array = message.split("/")	# TypeError: a bytes-like object is required, not 'str' python 2.x se puede hacer entre byte y string

        while i < len(chars_array):

            chars_array[i] = chars_array[i].replace(',','.') # Error por escritura de float --> could not convert string to float: b'-49,98297' debe ser '-49.98297'

            if i == 0:  ##header
                #if not (chars_array[i] == b'MINIMAPINFO'):  # en python 3.x hay q comparar byte
                if not (chars_array[i] == "MINIMAPINFO"):
                    return -1
            ## rest of elements
            elif i == 1:
                imagesMap.lengthImage = int(float(chars_array[i]))  ## length image
            elif i == 2:
                imagesMap.xMinAbsolute = float(chars_array[i])
            elif i == 3:
                imagesMap.xMaxAbsolute = float(chars_array[i])
            elif i == 4:
                imagesMap.yMinAbsolute = float(chars_array[i])
            elif i == 5:
                imagesMap.yMaxAbsolute = float(chars_array[i])
            elif i == 6:
                imagesMap.floorAbsolute = float(chars_array[i])
            elif i == 7:
                imagesMap.ceilingAbsolute = float(chars_array[i])

            i += 1
        return 0

    ## \brief Method to show the minimap (zenital scene view) and overlays a camera icon to visualize the placement of the camera.
    #
    # \param imagesMap Structure with the information of the minimap
    #
    # \return Operation code > 0 if success(-1 if failed)
    #
    # /
    def showMiniMap(self):
        global imagesMap
        ## copy source minimap
        imagesMap.dst = imagesMap.source

        ## load icon
        imagesMap.icon = Image.open("./resources/cameraIcon.png")

        ##create a window for display & set the callback function for mouse event
        ##cv2.namedWindow("Mapa", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Scene map", cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback("Scene map", OnClickMap, imagesMap)

        ## rotate icon by pressing LEFT or RIGHT keys
        key = cv2.waitKey(WAITMSTOREFRESH)
        while key != 13: # KEYENTER: # el valor de 13 es el numero en ascci de ENTER
            ## -90, -100 to center image on cursor
            imagesMap.dst = overlayImage(imagesMap.source, imagesMap.icon, (
            int(imagesMap.pointXCamRelative - 96), int(imagesMap.pointYCamRelative - 105)))
            cv2.imshow("Scene map", cv2.cvtColor(np.array(imagesMap.dst), cv2.COLOR_RGB2BGR))
            #cv2.imshow("Scene map", cv2.cvtColor(np.array(imagesMap.dst), cv2.COLOR_RGB2BGR))
            # cv2.displayStatusBar("Mapa", "Instrucciones:\n - Teclas de direccion <- y -> para rotar  - Enter para confirmar  - Esc para cancelar", 0);
            key = cv2.waitKey(WAITMSTOREFRESH)
            if key == KEYLEFT:
                imagesMap.angleCam = imagesMap.angleCam + 1  ## increase the rotation angle
                original = Image.open("./resources/cameraIcon.png")  ## reload icon
                imagesMap.icon = original.rotate(imagesMap.angleCam)  ## rotate icon
            elif key == KEYRIGHT:
                imagesMap.angleCam = imagesMap.angleCam - 1  ## decrease the rotation angle
                original = Image.open("./resources/cameraIcon.png")  ## reload icon
                imagesMap.icon = original.rotate(imagesMap.angleCam)  ## rotate icon
            elif key == KEYESCAPE:
                return -1
        cv2.destroyWindow("Scene map")

        ## coordinates recalculation
        imagesMap.pointXCamRelative = float(imagesMap.pointXCamRelative) / float(imagesMap.source.width)
        imagesMap.pointYCamRelative = float(imagesMap.pointYCamRelative) / float(imagesMap.source.height)
        imagesMap.angleCam = imagesMap.angleCam - 1

        return 1

    ## \brief This function shows the lateralmap (lateral scene view) and overlays a camera icon to visualize the placement of the camera (height).
    #
    # \param imagesMap Structure with the information of the minimap
    #
    # \return Operation code > 0 if success(-1 if failed)
    #
    # /
    def showCameraScheme(self):
        ##load resources
        background = Image.open("./resources/backgroundCamera.jpg")
        bg_rgb = np.array(background)
        bg_rgba = 255 * np.ones((bg_rgb.shape[0], bg_rgb.shape[1], bg_rgb.shape[2] + 1))
        bg_rgba[:, :, :-1] = bg_rgb
        background = Image.fromarray(np.uint8(bg_rgba))
        cameraIcon2 = Image.open("./resources/cameraIcon2.png")
        global imagesMap
        imagesMap.source = background
        imagesMap.dst = background
        imagesMap.icon = cameraIcon2

        ## Create a window for display & set the callback function for mouse event
        cv2.namedWindow("Height", cv2.WINDOW_AUTOSIZE)
        ##cv::namedWindow("Height", 0);
        cv2.setMouseCallback("Height", OnClickHeightMap, imagesMap)

        ##rotate icon by pressing UP or DOWN keys
        key = -1
        while key != 13: #KEYENTER: # el valor de 13 es el numero en ascci de ENTER
            imagesMap.dst = overlayImage(imagesMap.source, imagesMap.icon,
                                         (int(-100), int(imagesMap.heightCamRelative - 280)))
            cv2.imshow("Height", cv2.cvtColor(np.array(imagesMap.dst), cv2.COLOR_RGB2BGR))
            # cv2.displayStatusBar("Mapa", "Instrucciones:\n - Teclas de direccion <flecha UP> y <flecha DOWN> para rotar  - Enter para confirmar  - Esc para cancelar", 0);
            key = cv2.waitKey(WAITMSTOREFRESH)
            if key == KEYUP:
                imagesMap.heightAngleCam = imagesMap.heightAngleCam + 1  ## increase the rotation angle
                original = Image.open("./resources/cameraIcon2.png")  ## reload icon
                imagesMap.icon = original.rotate(imagesMap.heightAngleCam)  ##rotate icon
            elif key == KEYDOWN:
                imagesMap.heightAngleCam = imagesMap.heightAngleCam - 1  ## decrease the rotation angle
                original = Image.open("./resources/cameraIcon2.png")  ## reload icon
                imagesMap.icon = original.rotate(imagesMap.heightAngleCam)  ##rotate icon
            elif key == KEYESCAPE:
                return -1
        cv2.destroyWindow("Height")

        ##coordinates recalculation
        imagesMap.heightCamRelative = float((imagesMap.heightCamRelative - SECOND_IMG_OFFSET)) / float(SECOND_IMG_WIDTH)
        imagesMap.heightAngleCam = -1 * imagesMap.heightAngleCam

        return 1
