# Creation de MSScam
import sys
import socket
import os
import time
import calendar
import numpy as np
import cv2
import base64
import math
from functions.MSScam_control import *
from functions.MSScam_insert import *
from utils.MSSutils import *

# name = "VideoSalida"+str(randint(0, 99))+".avi"
# salida = cv2.VideoWriter(name,cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))

class MSScam:
    def __init__(self, *args):
        #self.name = "None"  # Iniciarlizar el nombre de la ventana
        self.width = -1
        self.height = -1
        self.fps = -1
        self.posX = -1
        self.posY = -1
        self.posZ = -1
        self.rotX = -1
        self.rotY = -1
        self.rotZ = -1
        self.fov = 1
        self.qualityjpg = -1
        self.txFormat = -1
        self.id = -1
        self.numCam=-1

        ##
        #    \brief Default class constructor with default parameters
        ##
        if len(args) == 0:
            print("\nDefault initialization...")
            self.init()
            self.Default()

        ##
        #   \brief Constructor from file
        ##
        elif len(args) == 1:
            filename = args[0]
            print("\nInitiating camera from file " + filename + " ...")
            file = open(filename, "r")
            line = file.readline()
            while line[0] == '/':
                line = file.readline()
            temp = line.replace("\r\n", "")
            values = temp.split('/')
            self.ManualName(*values) # linea incluida para inicializar self.name del .txt leido
            self.initiate_from_camera_descriptor(values)
            file.close()
        else:
            print("\nManual camera initialization...")
            self.init()
            self.Default()
            self.Manual(*args)

    def ManualName(self, *args):
        self.name = args[0]

    def Default(self):
        self.name = "test"
        self.width = -1
        self.height = -1
        self.fps = 10
        self.posX = 0
        self.posY = 0
        self.posZ = 0
        self.rotX = 0
        self.rotY = 0
        self.rotZ = 0
        self.fov = 1
        self.qualityjpg = 75
        self.numCam=0


    def Manual(self, *args):
        self.name = args[0]
        self.width = args[1]
        if len(args) > 2:
            self.height = args[2]
        if len(args) > 3:
            self.fps = args[3]
        if len(args) > 4:
            self.posX = args[4]
        if len(args) > 5:
            self.posY = args[5]
        if len(args) > 6:
            self.posZ = args[6]
        if len(args) > 7:
            self.rotX = args[7]
        if len(args) > 8:
            self.rotY = args[8]
        if len(args) > 9:
            self.rotZ = args[9]
        if len(args) > 10:
            self.fov = args[10]
        if len(args) > 11:
            self.qualityjpg = args[11]

    def init(self):
        self.txFormat = CAM_JPEG  # 0=jpg, 1=png
        self.isFPSrealEnabled = False
        self.fpsReal = -1
        self.fov = 1
        self.qualityjpg = 75

        self.isRegistered = False
        self.sock = -1
        self.port = -1
        self.id = -1

        print("done!")
        return 1

    # \brief Method to initialize camera parameters from a string received from simulator.
    # See more in MSSclient.getAllCamerasFromSimulator.
    #
    # \param values string vector with the information received from the simulator.
    #
    # \return Operation code > 0 if success(-1 if failed)
    ##

    def initFromDescriptorExtended(self, values):
        if len(values) > 0:
            if len(values[0]) > 0:
                self.name = values[0]
        if len(values) > 1:
            if len(values[1]) > 0:
                self.id = int(float(values[1]))
        if len(values) > 2:
            if len(values[2]) > 0:
                self.fps = int(float(values[2]))
        if len(values) > 3:
            if len(values[3]) > 0:
                self.width = int(float(values[3]))
        if len(values) > 4:
            if len(values[4]) > 0:
                self.height = int(float(values[4]))
        if len(values) > 5:
            if len(values[5]) > 0:
                self.txFormat = int(float(values[5]))
        if len(values) > 6:
            if len(values[6]) > 0:
                self.qualityjpg = int(float(values[6]))
        if len(values) > 7:
            if len(values[7]) > 0:
                self.posX = float(values[7])
        if len(values) > 8:
            if len(values[8]) > 0:
                self.posY = float(values[8])
        if len(values) > 9:
            if len(values[9]) > 0:
                self.posZ = float(values[9])
        if len(values) > 10:
            if len(values[10]) > 0:
                self.rotX = float(values[10])
        if len(values) > 11:
            if len(values[11]) > 0:
                self.rotY = float(values[11])
        if len(values) > 12:
            if len(values[12]) > 0:
                self.rotZ = float(values[12])

    # \brief Method to initialize camera parameters from a string received from simulator.
    # See more in MSSclient.getAllCamerasFromSimulator.
    #
    # \param values string vector with the information received from the simulator.
    #
    # \return Operation code > 0 if success(-1 if failed)
    ##

    def initiate_from_camera_descriptor(self, values):
        if len(values) > 1:
            if len(values[1]) > 0:
                self.fps = int(values[1])
        if len(values) > 2:
            if len(values[2]) > 0:
                self.width = int(float(values[2]))
        if len(values) > 3:
            if len(values[3]) > 0:
                self.height = int(float(values[3]))
        if len(values) > 4:
            if len(values[4]) > 0:
                self.txFormat = int(float(values[4]))
        if len(values) > 5:
            if len(values[5]) > 0:
                self.qualityjpg = int(float(values[5]))
        if len(values) > 6:
            if len(values[6]) > 0:
                values[6] = values[6].replace(',', '.')  # Error de could not convert string to float: '-0,5'
                self.posX = float(values[6])
        if len(values) > 7:
            if len(values[7]) > 0:
                values[7]=values[7].replace(',','.')
                self.posY = float(values[7])
        if len(values) > 8:
            if len(values[8]) > 0:
                values[8] = values[8].replace(',', '.')
                self.posZ = float(values[8])
        if len(values) > 9:
            if len(values[9]) > 0:
                values[9] = values[9].replace(',', '.')
                self.rotX = float(values[9])
        if len(values) > 10:
            if len(values[10]) > 0:
                values[10] = values[10].replace(',', '.')
                self.rotY = float(values[10])
        if len(values) > 11:
            if len(values[11]) > 0:
                values[11] = values[11].replace(',', '.')
                self.rotZ = float(values[11].rstrip('\x00'))  # python3.x, .rstrip recirta los caracteres que se indica
                # self.rotZ = float(values[11])  # Python 2.x el
# values es de tipo <class 'list'> y la lista es [...., '10', '0\x00'] donde el value[11] es byte

    # \brief Method to save camera parameters in a configuration file. It currently supports one description per file.
    #
    # \param filename Path to the filename to save the camera descriptor
    #
    # \return Operation code > 0 if success(-1 if failed)
    ##

    def saveTofile(self, filename):
        if os.path.isfile(filename):
            file = open(filename, "w")
            file.write("// each line contains a camera with the following format:\n")
            file.write(
                "// name/fps/width/height/TXRXformat/JPEGquality/positionX/positionY/positionZ/rotationX/rotationY/rotationZ\n")
            file.write("// example: camtest/10/640/480/0/75/9.816450/3.844200/15.368404/0.000000/0.000000/0.000000\n")
            file.write(
                str(self.name) + "/" + str(self.fps) + "/" + str(self.width) + "/" + str(self.height) + "/" + str(
                    self.txFormat) + "/" + str(self.qualityjpg) \
                + "/" + str(self.posX) + "/" + str(self.posY) + "/" + str(self.posZ) + "/" + str(self.rotX) + "/" + str(
                    self.rotY) + "/" + str(self.rotZ))
            print("\nCamera details saved in " + filename)
            file.close()
            return 1
        else:
            print("\nCannot save camera details to %s" % filename)
            return -1

    # \brief Adds the camera to the simulator
    #
    # \param sock Created socket
    # \param ipAddress IP address of the host/machine running the simulator
    # \param port Port number to connect to the host/machine running the simulator
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##
    def setRegister(self, sock, ipAddress, port):

        print("\nRegistered Accese de object camera to simulator...")
        # copy connection settings to the simulator
        self.sock = sock  # this parameter is the only requirement for the connections
        # not needed for TX/RX - copied just for redundancy in the atttributes of the camera object
        self.ipAddress = ipAddress

        self.port = port  # not needed for TX/RX - copied just for redundancy in the atttributes of the camera object

        # create command
        # sprintf(command, "CREACAMARA-%s-%d-%d-%d-%d-%d$", _name, _fps, _width, _height, _txFormat, _qualityjpg);
        command = "REGISTERED-"

        # register camera in simulator
        self.isRegistered = True
        global reply
        reply = " " * CMD_STRLEN_DEF
        if self.send_command(command, reply, True) < 0:
            self.isRegistered = False

        # wait 1sec so the server can initialize data properly
        time.sleep(1)
        return 1

    def setNameRACamera(self, newNameRACamera):
        self.name = newNameRACamera
        return 1

    def configRACamera(self, sock, ipAddress, port):
        print("\nConfigurar a todas las camaras del simulador..")

        # copy connection settings to the simulator
        self.sock = sock  # this parameter is the only requirement for the connections
        # not needed for TX/RX - copied just for redundancy in the atttributes of the camera object
        self.ipAddress = ipAddress
        self.port = port  # not needed for TX/RX - copied just for redundancy in the atttributes of the camera object
        # create command
        # sprintf(command, "CREACAMARA-%s-%d-%d-%d-%d-%d$", _name, _fps, _width, _height, _txFormat, _qualityjpg);

        command = "CONFIGRACAMERA-" + str(self.name) + "/" + str(self.fps) + "/" + str(self.width) + "/" + str(
            self.height) + "/" + str(self.txFormat) + "/" + str(self.qualityjpg)

        # Enviar el comando al servidor para registrar en el simulador
        self.isRegistered = True
        global reply
        reply = " " * CMD_STRLEN_DEF
        if self.send_command(command, reply, True) < 0:
            self.isRegistered = False

        time.sleep(1)
        return 1

    def readTosimulator(self, sock, ipAddress, port):
        print("\nLee el numero de cameras de acceso remoto en el simulator...")

        # copy connection settings to the simulator
        self.sock = sock  # this parameter is the only requirement for the connections
        # not needed for TX/RX - copied just for redundancy in the atttributes of the camera object
        self.ipAddress = ipAddress
        self.port = port  # not needed for TX/RX - copied just for redundancy in the atttributes of the camera object
        # create command
        # sprintf(command, "CREACAMARA-%s-%d-%d-%d-%d-%d$", _name, _fps, _width, _height, _txFormat, _qualityjpg);

        command = "READNUMCAMERA-"+ str(self.name)

        # Enviar el comando al servidor para registrar en el simulador
        self.isRegistered = True
        global reply
        reply = " " * CMD_STRLEN_DEF
        if self.send_command(command, reply, True) < 0:
            self.isRegistered = False

        # get num cameras in to simulator
        if reply != '':
            # reemplazar la instruccion de replace para quitar '\x00' python 3.x en str, si es entre byte se usa b'\x00'
            self.numCam = int(reply.rstrip('\x00'))
            # self.id = int(reply)			# este valor se obitene el entero de la variable reply python 2.x
            reply = reply + "\0"  # add termination to string
            print(reply)
        else:
            self.id = -1

        # wait 1sec so the server can initialize data properly
        time.sleep(1)
        return self.numCam

    def addToSimulatorMapaSemantico(self, sock, ipAddress, port):
        print("Añadir camara de Usuario de Mapa Semantico al simulador ")
        self.sock = sock  # this parameter is the only requirement for the connections
        self.ipAddress = ipAddress
        self.port = port  # not needed for TX/RX - copied just for redundancy in the atttributes of the camera object

        # create new command
        # "ADDCAMUSERCAMSEMANTICO-Demo/fps/width/heigth/txFormat/qualtyjpg/posX/posY/posZ/rotX/rotY/rotZ"
        """
        command = "CREATECAMERAEXTENDED-" + str(self.name) + "/" + str(self.fps) + "/" + str(self.width) + "/" + str(
            self.height) + "/" + str(self.txFormat) + "/" + str(self.qualityjpg) \
                  + "/" + str(self.posX) + "/" + str(self.posY) + "/" + str(self.posZ) + "/" + str(
            self.rotX) + "/" + str(self.rotY) + "/" + str(self.rotZ) + "$" +\
                  "CREATECAMERASEMANTIC-" + str(self.name) + "/" + str(self.fps) + "/" + str(self.width) + "/" + str(
            self.height) + "/" + str(self.txFormat) + "/" + str(self.qualityjpg) + "/" + str(self.posX) + "/" + str(
            self.posY) + "/" + str(self.posZ) + "/" + str(self.rotX) + "/" + str(self.rotY) + "/" + str(self.rotZ)
        """
        command = "CREATECAMERASEMANTIC-" + str(self.name) + "/" + str(self.fps) + "/" + str(self.width) + "/" + str(
            self.height) + "/" + str(self.txFormat) + "/" + str(self.qualityjpg) \
                  + "/" + str(self.posX) + "/" + str(self.posY) + "/" + str(self.posZ) + "/" + str(
            self.rotX) + "/" + str(self.rotY) + "/" + str(self.rotZ)

        # register camera in simulator
        self.isRegistered = True
        global reply
        reply = " " * CMD_STRLEN_DEF
        if self.send_command(command, reply, True) < 0:
            self.isRegistered = False

        # get the camera ID
        if reply != '':
           #variable = reply.split('\x00')
           #print(variable)
           self.id = int(reply.rstrip('\x00'))
           reply = reply + "\0"  # add termination to string
        else:
            self.id = -1
        print(" IDcam=" + str(self.id) + " name=" + self.name)
        time.sleep(1)
        return 1


    def addTosimulator(self, sock, ipAddress, port):

        print("\nAdding camera to simulator...")

        # copy connection settings to the simulator
        self.sock = sock  # this parameter is the only requirement for the connections

        # not needed for TX/RX - copied just for redundancy in the atttributes of the camera object
        self.ipAddress = ipAddress

        self.port = port  # not needed for TX/RX - copied just for redundancy in the atttributes of the camera object

        # create command
        # sprintf(command, "CREACAMARA-%s-%d-%d-%d-%d-%d$", _name, _fps, _width, _height, _txFormat, _qualityjpg);
        command = "CREATECAMERAEXTENDED-" + str(self.name) + "/" + str(self.fps) + "/" + str(self.width) + "/" + str(
            self.height) + "/" + str(self.txFormat) + "/" + str(self.qualityjpg) \
                  + "/" + str(self.posX) + "/" + str(self.posY) + "/" + str(self.posZ) + "/" + str(
            self.rotX) + "/" + str(self.rotY) + "/" + str(self.rotZ)

        # register camera in simulator
        self.isRegistered = True
        global reply
        reply = " " * CMD_STRLEN_DEF
        if self.send_command(command, reply, True) < 0:
            self.isRegistered = False

        # get the camera ID
        if reply != '':
            # reemplazar la instruccion de replace para quitar '\x00' python 3.x en str, si es entre byte se usa b'\x00'
            self.id = int(reply.rstrip('\x00'))
            # self.id = int(reply)			# este valor se obitene el entero de la variable reply python 2.x
            reply = reply + "\0"  # add termination to string
        else:
            self.id = -1
        print(" IDcam=" + str(self.id) + " name=" + self.name)

        # wait 1sec so the server can initialize data properly
        time.sleep(1)
        return 1

    # \brief Removes the camera from the simulator
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##
    def removeCameraSceneSimulator(self):

        print("\nUnregistering " + self.name+ " form Simulator")
        # create command
        command = "DELETECAMARA-" + self.name + "-CAMSCENE"
        # send command
        reply = " " * 50
        if self.send_command(command, reply, True) < 0:
            return -1
        # wait 1sec so the simulator can properly delete the camera
        time.sleep(1)
        return 1


    def removeFromSimulator(self):

        print("\nUnregistering camera id=%d from simulator..." % self.id)

        # create command
        command = "DELETECAMARA-" + self.name

        # send command
        reply = " " * 50
        if self.send_command(command, reply, True) < 0:
            return -1

        self.isRegistered = False

        # wait 1sec so the simulator can properly delete the camera
        time.sleep(1)

        return 1

    # \brief Get current frame from simulator
    #
    # \return image Frame captured from the camera in the simulator
    ##

    def operator(self):
        # create command
        command = "GETFRAME-" + self.name

        # send command to receive one frame (disable "verbose" output)
        if self.send_command_noACK(command, False) < 0:
            return -1

        # receive data & convert to frame
        if self.receiveFrame(False) < 0:  # receive data in chunks & store in the internal buffer "_buf"
            return -1
        image = self.convertBufferToMat()  # convert buffer to Mat

        # received frame is inverted so it is flipped
        image = cv2.flip(image, 0)

        # return succesfull completion
        return image

    # \brief This function reads large amounts of data employing a small buffer of 10KB
    # Data is stored in the global buffer "buf" defined for BUFFER_FRAME_DEF bytes (aprox 10MB)
    # Solution based on http://stackoverflow.com/questions/10011098/how-to-receive-the-large-data-using-recv
    #
    # \param verbose FLAG to show additional information in the command window
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def receiveFrame(self, verbose):

        # huge timeout to wait server to prepare response, 1 s
        timeout = 1
        self.sock.settimeout(timeout)

        iByteCount = 0  # counter for the bytes received

        smallbuf = self.sock.recv(10000, 0)
        if verbose:
            print("\nBytes received at first: %d" % (len(smallbuf)))
        recvBytes = len(smallbuf)
        if recvBytes <= 0:
            return -1

        # message is divided in frame length + frame, so we split

        chars_array = smallbuf.split(b'#')  # dividir entre bytes python 3.x
        # chars_array=smallbuf.split("#")	# hacer split a un byte en python 2.x
        global buf
        if len(chars_array) > 1:
            buf = chars_array[1]
            try:
                bytestorecv = int(chars_array[0])
            except ValueError:
                print("Data not fully received")
                return -1
            if verbose:
                print("Bytes to recv: " + str(bytestorecv))
        else:
            print("Data not fully received")
            return -1
        recvBytes = len(buf)
        iByteCount += recvBytes

        # fast timeout to read socket fast, 1 ms
        timeout = 1
        self.sock.settimeout(timeout)

        nrecep = 1
        while iByteCount < bytestorecv:
            smallbuf = self.sock.recv(10000)
            recvBytes = len(smallbuf)

            if recvBytes > 0:
                # make sure we're not about to go over the end of the buffer
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
                    # do process with received data
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
        return 1

    ## \brief Decodes the internal buffer into a cv::Mat variable. It uses the OpenCV API so standard image formats are supported.
    #
    # \return The decoded image
    ##
    def convertBufferToMat(self):
        global buf
        # buf en un byte
        # length4 es un int
        length4 = int(math.ceil(math.log(len(buf)) * math.log(4)) ** 4)

        buf = buf + b'=' * (length4 - len(buf))  # se hace concatenacion de buf tipo byte con b'=' tipo byte python 3.x
        # buf=buf+"="*(length4-len(buf)) #TypeError: can't concat str to bytes en python2.x buf es byte y "=" es str
        # s=buf.decode('base64')			#sintaxis para python 2.x
        s = base64.b64decode(buf)  # decodificar en base 64 sintaxis para pytho 3.x
        # s = base64.b64decode(buf) ## decode from base64 strings
        # std::vector <uchar> data(s.begin(), s.end()) ## convert to uchar for JPEG/PNG decoding
        data = np.fromstring(s, dtype=np.uint8)
        image = cv2.imdecode(data, 1)
        # cv2.imwrite(self.name+".png",image)

        return image

    ## \brief Display frames continuously until ESC key is pressed or the timeout is triggered.
    #
    # \param timeout Time to perform the camera preview (use "-1" for infinite preview time).
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def preview(self, timeout):
        print("\nCamera preview mode started. Press ESC to cancel...")
        if not self.isRegistered:
            print("Not registered (cannot preview).\n")
            return -1
        winName = self.name + "-preview"
        # initialize timing
        begin = calendar.timegm(time.localtime())
        time_spent = -1
        numframes = 0
        print("Press Escape to break preview loop")
        while True:
            # Capture frame-by-frame
            frame = self.operator()
            if isinstance(frame, np.ndarray):
                width, height = frame.shape[:2]
                if width > 0 and height > 0:
                    numframes += 1
                    cv2.imshow(winName, frame)  # display frame
                    # salida.write(frame) # Aumetnado para grabar imagen
                    if cv2.waitKey(5) == KEYESCAPE:
                        break
            # cv2.waitKey(1000/self.fps)
            # check timeout
            if timeout > 0:
                time_spent = calendar.timegm(time.localtime()) - begin
                print("Preview time: " + str(time_spent) + "s (max " + str(timeout) + "s), " + "frame number: " + str(
                    numframes))
                if time_spent >= timeout:
                    break
        # When everything done, release the capture
        # salida.release() # Aumentado para grabar imagen
        cv2.destroyAllWindows()
        return 1

    ## \brief Set camera status
    #
    # \param connected bool True of False
    ##
    def setStatus(self, connected):
        self.isRegistered = connected

    ## \brief Enable framerate count at the server
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def realFPSenable(self):
        print("\nActivating FPS counter in server...")

        # create command
        command = "SETACTIVEGETREALFPS-%s" % self.name

        # send command & check TX/RX status
        reply = " " * 50
        if self.send_command(command, reply, True) < 0:
            return -1

        self.isFPSrealEnabled = True
        return 1

    ## \brief Disable framerate count at the server
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def realFPSdisable(self):
        print("\nDisabling FPS counter in server...")

        # create command
        command = "SETINACTIVEGETREALFPS-%s" % self.name

        # send command & check TX/RX status
        reply = " " * 50
        if self.send_command(command, reply, True) < 0:
            return -1

        self.isFPSrealEnabled = False
        return 1

    ## \brief Retrieve framerate count from the server
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def updateRealFPS(self):
        print("\nRetrieving FPS counter from server...")

        # create command

        command = "GETCAMERAREALTIMEFPS-%s" % self.name
        global reply
        reply = " " * 50
        # send command & check TX/RX status
        if self.send_command(command, reply, True) < 0:
            return -1
        # get the real FPS returned by simulator
        self.fpsReal = int(reply)
        self.isFPSrealEnabled = False

        return 1

    ## \brief Method to move the camera in the simulator
    #
    # \param option Command to move the camera
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def move(self, option):
        switch_show = {
            0: 'CAM_MOVE_LEFT',
            1: 'CAM_MOVE_RIGHT',
            2: 'CAM_MOVE_UP',
            3: 'CAM_MOVE_DOWN',
            4: 'CAM_MOVE_FORWARD',
            5: 'CAM_MOVE_BACKWARD',
            6: 'CAM_ROTATE_LEFT',
            7: 'CAM_ROTATE_RIGHT',
            8: 'CAM_ROTATE_UP',
            9: 'CAM_ROTATE_DOWN'
        }
        print("\nMoving camera %s..." % (switch_show[option]))

        switch_command = {
            0: "MOVECAMARALEFT-%s" % self.name,
            1: "MOVECAMARARIGHT-%s" % self.name,
            2: "MOVECAMARAUP-%s" % self.name,
            3: "MOVECAMARADOWN-%s" % self.name,
            4: "MOVECAMARAAHEAD-%s" % self.name,
            5: "MOVECAMARABACK-%s" % self.name,
            6: "ROTATECAMARALEFT-%s" % self.name,
            7: "ROTATECAMARARIGHT-%s" % self.name,
            8: "ROTATECAMARAUP-%s" % self.name,
            9: "ROTATECAMARADOWN-%s" % self.name
        }
        command = switch_command[option]

        # send command & check TX/RX status
        reply = " " * CMD_STRLEN_DEF
        return self.send_command(command, reply, True)

    ## \brief Method to set the camera framerate and update it in the MSS server
    #
    # \param newfps New framerate value
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def setFPS(self, newfps):
        print("\nChanging FPS to %d (previous=%d)..." % (newfps, self.fps))

        # create command
        command = "CHANGECAMARAFPS-%s-%d" % (self.name, newfps)

        # send command & check TX/RX
        global reply
        reply = " " * CMD_STRLEN_DEF
        if self.send_command(command, reply, True) < 0:
            return -1

        self.fps = newfps
        return 1

    ## \brief Method to set the TX/RX format for the camera and update it in the MSS server
    #
    # \param newfmt New format value
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def setTXRXformat(self, newfmt):
        switch_fmt = {
            0: 'CAM_JPEG',
            1: 'CAM_PNG'
        }
        print("\nChanging FORMAT to %s (previous=%s)..." % (switch_fmt[newfmt], switch_fmt[self.txFormat]))

        # create command
        command = "CHANGECAMARAFORMAT-%s-%d$" % (self.name, newfmt)

        # send command & check TX/RX status
        reply = " " * CMD_STRLEN_DEF
        if self.send_command(command, reply, True) < 0:
            return -1

        self.txFormat = newfmt
        return 1

    # \brief Method to set the JPEG quality for the camera and update it in the MSS server
    #
    # \param newq New JPEG quality value between 0 and 100
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def setJPEGquality(self, newq):
        print("\nChanging JPEG quality to %d (previous=%d)..." % (newq, self.qualityjpg))

        # create command
        command = "CHANGECAMARACALIDADJPG-%s-%d$" % (self.name, newq)

        # send command & check TX/RX status
        reply = " " * CMD_STRLEN_DEF
        if (self.send_command(command, reply, True) < 0):
            return -1

        self.qualityjpg = newq
        return 1

    ## \brief Method to increase the camera zoom and update it in the MSS server
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def zoomIn(self):
        print("\nZoom in (closing field of view) ...")

        # create command
        command = "CLOSEFIELDOFVIEW-%s$" % (self.name)

        # send command & check TX/RX status
        reply = " " * CMD_STRLEN_DEF
        return self.send_command(command, reply, True)

    ## \brief Method to decrease the camera zoom and update it in the MSS server
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##
    def zoomOut(self):
        print("\nZoom out (opening field of view) ...")

        # create command
        command = "OPENFIELDOFVIEW-%s$" % (self.name)

        # send command & check TX/RX status
        reply = " " * CMD_STRLEN_DEF
        return self.send_command(command, reply, True)

    # \brief Method to set the width of captured frames and update it in the MSS server
    #
    # \param n_width New width value for each frames
    # \return Operation code > 0 if success (-1 if failed)
    #

    def setWidth(self, n_width):

        # create command
        command = "CHANGECAMERAWIDTH-%s-%d$" % (self.name, n_width)

        # send command & check TX/RX status
        reply = " " * CMD_STRLEN_DEF
        return self.send_command(command, reply, True)

    # \brief Method to set the height of captured frames and update it in the MSS server
    #
    # \param n_height New height value for each frames
    # \return Operation code > 0 if success (-1 if failed)
    #
    def setHeight(self, n_height):

        # create command
        command = "CHANGECAMERAHEIGHT-%s-%d$" % (self.name, n_height)

        # send command & check TX/RX status
        reply = " " * CMD_STRLEN_DEF
        return self.send_command(command, reply, True)

    # \brief Method to send a command to the MSS server and receive a reply (most ACKs)
    # \param command String with the command to send
    # \param reply String the reply from the server
    # \param verbose FLAG to get additional information displayed in the command window

    # \return Operation code > 0 if success (-1 if failed)

    def send_command(self, command_in, reply_in, verbose):

        # check if camera is registered in simulator
        global reply
        global command
        global sock
        reply = reply_in
        command = command_in
        if not self.isRegistered:
            if verbose:
                print("Not registered (cannot change).\n")
            return -1

        # send command to server

        if self.sock.send(command.encode('utf-8'), 0) < 0:  # enviarse el command de tipo byte y no str python 3.x
            # if self.sock.send(command, 0) < 0:			# comando para enviar en pyton 2.x
            if verbose:
                print("Send failed\n")
            return -1
        self.sock.settimeout(1)

        # receive ACK from server
        command = self.sock.recv(CMD_STRLEN_DEF, 0)
        command = str(command, 'utf-8')  # se esta convirtiendo en un string python 3.x
        # command=command.replace("\0","")	# se esta reemplazando el b'1\x00' por espacio vacio, hacer conteo python 2.x
        length = len(command)
        if length < 0:
            if verbose:
                print("received failed\n")
            return -1

        # copy returned message in "reply" string
        if reply != "":
            count = min(len(command), len(reply))
            reply = command[0:count]
        if verbose:
            print("done!")

        # ---------- Añadido solo para saber el tipo de camara en el simulador ----
        # para hacer uso de la llamada cam.send_command(command, reply, False)
        # dentro de GUIcontrolRACam()
        if not verbose:
            print("Camara de tipo: " + reply + ". Acciones Limitadas segun su tipo")
        # --------------------------------------------------------------------


        return 1

    ## \brief Method to send a command to the MSS server and not receive a reply (most ACKs)
    #
    # \param command String with the command to send
    # \param verbose FLAG to get additional information displayed in the command window
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def send_command_noACK(self, command_in, verbose):

        # check if camera is registered in simulator
        global command
        command = command_in
        if not self.isRegistered:
            if verbose:
                print("Not registered (cannot change).\n")
            return -1

        # send command to server
        if self.sock.send(command.encode('utf-8'), 0) < 0:  # debe enviarse el command de tipo byte y no str python 3.x
            # if self.sock.send(command, 0) < 0:	# python 2.x  TypeError: a bytes-like object is required, not 'str'
            if verbose:
                print("Send failed\n")
            return -1

        if verbose:
            print("done!")
        return 1

    # brief Method to display camera details in the command window
    def print_details(self):
        if self.isRegistered:
            conn = "connected"
        else:
            conn = "disconnected"
        print("\nID=%d -> name=%s fps=%d W=%d H=%d pX=%.2f pY=%.2f pZ=%.2f rX=%f rY=%f rZ=%f fov=%d q=%d status=%s" \
              % (self.id, self.name, self.fps, self.width, self.height, self.posX, self.posY, self.posZ, self.rotX,
                 self.rotY, self.rotZ, self.fov, self.qualityjpg, conn))

    # \brief Method to start the interactive control of the camera motion through a GUI
    #
    # \return Operation code > 0 if success (-1 if failed)
    ##

    def GUIcontrol(self):
        print("\nCamera control mode started. Press ESC to cancel...")

        # start the interactive controls for camera motion
        self.ctrl = MSScam_control()
        # self.ctrl = MSScam_control.MSScam_control()		# Python 2.x type object 'MSScam_control' has no attribute
        self.ctrl.start(self)

        # update details from server (create & send command)
        global reply
        reply = " " * CMD_STRLEN_DEF
        command = "GETDETAILS-%s$" % self.name
        self.send_command(command, reply, True)
        chars_array = reply.split('/')
        # read new received description and update camera parameters
        self.initiate_from_camera_descriptor(chars_array)
        return 1

    # \brief Method to start the interactive  placement of the camera motion through a GUI
    # \param sock Socket to connect to the MSS server
    # \return Operation code > 0 if success (-1 if failed)

    def GUIinsert(self, sock):
        print("\nStarted interactive GUI for camera positioning...")
        self.sock = sock  # copy the socket info
        self.gui = MSScam_insert()  # python 3.x
        # self.gui=MSScam_insert.MSScam_insert() #type object 'MSScam_insert' has no attribute 'MSScam_insert' python2.x
        self.gui.start(sock, self)

        self.posX = self.gui.posX  # left-right
        self.posY = self.gui.posY  # height
        self.posZ = self.gui.posZ  # forward/backward
        self.rotX = self.gui.rotX
        self.rotY = self.gui.rotY

        if self.isRegistered:
            pass
        # TODO: to implement the update of the camera when it is registered
        return 1


    def GUIcontrolRACam(self):
        print("\nCamera control mode started. Press ESC to cancel...")

        # start the interactive controls for camera motion
        self.ctrl = MSScam_control()
        # self.ctrl = MSScam_control.MSScam_control()		# Python 2.x type object 'MSScam_control' has no attribute
        self.ctrl.start(self)

        # update details from server (create & send command)
        # global reply
        # reply = " " * CMD_STRLEN_DEF
        # command = "GETCAMERATYPE-%s$" % self.name
        # self.send_command(command, reply, True)
        # chars_array = reply.split('/')
        ## read new received description and update camera parameters
        return 1
