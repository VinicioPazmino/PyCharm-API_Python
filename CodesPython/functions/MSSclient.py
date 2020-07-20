import sys
import socket
import platform
from utils.MSSutils import *
from functions.MSScam import *
import ctypes
import time



#brief Default client initialization
class MSSclient:
	def __init__(self):
		self.sock = -1
		self.port = -1
		self.isConnected = False
		self.isInitialized = False
		self.id=-1
		self.ipAddress="255.255.255.255"
		##initialize network settings
		self.initialize_network()

	## brief Initialization of network settings for UNIX
	   # return Integer > 0 if OK (-1 if failed)

	def initialize_network(self):
		if platform.system()=='Windows':

			print ("This program only works in Linux")
			return -1

		elif platform.system()=='Linux':
			# Do linux stuff 

			self.isInitialized = True

			return 1
	

	##brief This function must be the first used. It creates the socket.
	  # param ipAddress IP address of the host/machine running the simulator
	  # param port Port number to connect to the host/machine running the simulator
	  # param sock Created socket
	
	  # return The ID of the client logged in the simulator (-1 if failed)
	
	def connectTosimulator(self, ipAddress, port, sock):
		if not self.isInitialized:
			print ("\n Network must be initialized first. Please use 'initialize_network()'\n")
			return -1

		print ("\nConnecting client to simulator with IP %s (port %d)..." % (ipAddress, port))

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

		if sock == -1:
			return -1


		##Connect to remote server
		sock.connect((ipAddress,port))

		buf = sock.recv(STRLEN_SHORT_DEF, 0)
		#buf=buf.replace("\0","")			# buf es de typo byte por lo que en python 3 no se puede usar el .replace si no son string		
		#buf=str(buf[0:1],'ascii')			# con replace se quedaba con el numero entero del ID, en este caso se toma los elementos
								# iniciales [0:2] del buf = b'36\x00' es decir 36 para convertirlo en string de formato ascii
		
		buf = buf.rstrip(b'\x00')			# reemplazar la instruccion de replace para quitar el '\x00' para python 3.x
		length=len(buf)
		if length < 0:
			print ("Error! (recv ACK failed).\n")
			return -1

		self.isConnected = True
		print ("done! IDclient="+str(int(buf)))
		self.id = int(buf)

		self.ipAddress=ipAddress 		##not needed for TX/RX - copied just for redundancy in the atttributes of the camera object
		self.port = port
		self.sock = sock

		##specify socket timeouts
		##setsockopt(_sock, SOL_SOCKET, SO_RCVTIMEO, reinterpret_cast<char*>(&tv1), sizeof(timeval));
		##setsockopt(_sock, SOL_SOCKET, SO_SNDTIMEO, reinterpret_cast<char*>(&tv1), sizeof(timeval));
		self.sock.settimeout(1e-4)

		return int(buf)

	## \brief This function must be used to disconnect from the simulator.
	#		   Otherwise a 'dead' client remains in the simulator.
	#
	#  \param sock Created socket after running "connect2simulator"
	#
	#  \return 1 if success or -1 if failure

	def disconnectFromSimulator(self,sock):

		if not self.isInitialized:  # if self.isInitialized == False:  # Usada para python 2.x
			print ("\nNetwork must be initialized first. Please use 'initialize_network()'")
			return -1

		if not self.isConnected:  # if self.isConnected == False: 	# Usada para python 2.x
			print ("\nClient must be connected first. Please use 'connectTosimulator()'")
			return -1

		print ("\nDisconnecting client from simulator...")

		##create command
		command="DELETECLIENT$"

		##send command to server
		if sock.send(command.encode('utf-8'), 0) < 0:		# necesita enviarse el command de tipo byte y no string python 3.x
		#if sock.send(command,0) < 0:				# comando para enviar en pyton 2.x
			print ("Send failed\n")
			return -1

		## receive ACK from server
		command = sock.recv(STRLEN_SHORT_DEF, 0)
		length=len(command)
		if length < 0:
			print ("recv failed\n")
			return -1

		print ("done!")

		self.isConnected = False
		return 1

	def resetSimulator(self,sock):

		if not self.isInitialized:  # if self.isInitialized == False:  # Usada para python 2.x
			print ("\nNetwork must be initialized first. Please use 'initialize_network()'")
			return -1

		if not self.isConnected:  # if self.isConnected == False: 	# Usada para python 2.x
			print ("\nClient must be connected first. Please use 'connectTosimulator()'")
			return -1

		print ("\nReset simulator: deleting all cameras...")

		##create command
		command="RESET$"

		##send command to server
		if sock.send(command.encode('utf-8'), 0) < 0:
			print ("Send failed\n")
			return -1

		## receive ACK from server
		command = sock.recv(STRLEN_SHORT_DEF, 0)
		length=len(command)
		if length < 0:
			print ("recv failed\n")
			return -1

		print ("done!")

		return 1

	def getAllCamerasFromSimulator(self,sock):
		if not self.isInitialized:  # usada para python 3.X
		# if self.isInitialized == False:  # Usada para python 2.x
			print ("\nNetwork must be initialized first. Please use 'initialize_network()'")
			return -1

		if not self.isConnected:  # usada para python 3.X
		# if self.isConnected == False: 	# Usada para python 2.x
			print ("\nClient must be connected first. Please use 'connectTosimulator()'")
			return -1

		print ("\nGet existing cameras from simulator...")

		##create command
		command="GETDETAILSALLCAMERAS$"

		##send command to server
		if sock.send(command,0) < 0:
			print ("Send failed\n")
			return -1

		## receive ACK from server
		command = sock.recv(1028, 0)
		length=len(command)
		if length < 0:
			print ("recv failed\n")
			return -1

		chars_array=command.split("#")
		global out
		out=[]
		for i in range(0,len(chars_array)):
			cam=MSScam("", 0, 0, 0, 0, 0, 0, 0, 0, 0)
			stringaux=chars_array[i]
			stringaux=stringaux.split("/")
			cam.initFromDescriptorExtended(stringaux)
			cam.setStatus(True)
			out.append(cam)

		print ("done!")
		return 1

	def modeFrame(self,sock,mode):

		if not self.isInitialized:  # if self.isInitialized == False:  # Usada para python 2.x
			print ("\nNetwork must be initialized first. Please use 'initialize_network()'")
			return -1

		if not self.isConnected:  # if self.isConnected == False: 	# Usada para python 2.x
			print ("\nClient must be connected first. Please use 'connectTosimulator()'")
			return -1

		if mode == "CONTINUOUS":
			print ("\nMode: Frame Continuous...")
			command = "MODEFRAME" + "-" + str(mode) + "$"
		elif mode == "ONDEMAND":
			print ("\nMode: Frame On Demand...")
			command = "MODEFRAME" + "-" + str(mode) + "$"
		else:
			print("\nMode Default: Continuos...")
			command = "MODEFRAME" + "-" + str(mode) + "$"


		##send command to server
		if sock.send(command.encode('utf-8'), 0) < 0:
			print ("Send failed\n")
			return -1

		## receive ACK from server
		command = sock.recv(STRLEN_SHORT_DEF, 0)
		length=len(command)
		if length < 0:
			print ("recv failed\n")
			return -1

		print ("done!")

		return 1

	def advancedSimulation(self,sock,timeWait):

		if not self.isInitialized:  # if self.isInitialized == False:  # Usada para python 2.x
			print ("\nNetwork must be initialized first. Please use 'initialize_network()'")
			return -1

		if not self.isConnected:  # if self.isConnected == False: 	# Usada para python 2.x
			print ("\nClient must be connected first. Please use 'connectTosimulator()'")
			return -1

		print ("\nAdvanced Simulation: Frame on Demanda...")

		##create command
		#command = "ADVANCESIMULATION$"
		command="ADVANCESIMULATION"+"-"+str(timeWait)+"$"

		##send command to server
		if sock.send(command.encode('utf-8'), 0) < 0:
			print ("Send failed\n")
			return -1

		## receive ACK from server
		command = sock.recv(STRLEN_SHORT_DEF, 0)
		length=len(command)
		if length < 0:
			print ("recv failed\n")
			return -1

		#time.sleep(timeWait)
		print("done!")

		return 1