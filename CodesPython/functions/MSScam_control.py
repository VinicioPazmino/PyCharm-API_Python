import sys
import cv2
from utils.MSSutils import*
from functions.MSScam import *
from functions.MSSclient import *
import socket
from random import randint

class MSScam_control:
	def __init__(self):
		pass

##
#	\brief Method to start the interactive motion of the camera
#
#	\param cam the MSS camera which is going to be moved
##
	def start(self,cam):
		self.cam=cam
		## Create a window for display.
		cv2.namedWindow(cam.name, cv2.WINDOW_AUTOSIZE)

		##create controls
		def_value = 1
		cv2.createTrackbar("Up/Down", cam.name, def_value, 2, self.moveCam_UpDown)
		cv2.createTrackbar("Left/Right", cam.name, def_value, 2, self.moveCam_LeftRight)
		cv2.createTrackbar("Ahead/Back", cam.name, def_value, 2, self.moveCam_AheadBack)
		cv2.createTrackbar("rotate L/R", cam.name, def_value, 2, self.moveCam_rotateLeftRight)
		cv2.createTrackbar("rotate U/D", cam.name, def_value, 2, self.moveCam_rotateUpDown)

		##loop to move the camera until ESC is pressed	

		print ("Press Escape to break preview loop")
		while True:
			frame=cam.operator() ## get frame
			if isinstance(frame,np.ndarray):
				width, height = frame.shape[:2]
				if width>0 and height>0:
					cv2.imshow(cam.name, frame) ## display frame
				else:
					print ("Frame recv failed\n")
			else:
					print ("Frame recv failed\n")
			if cv2.waitKey(5) == KEYESCAPE:
						break
		cv2.destroyWindow(cam.name)

	##
	#	\brief Callback method to move the camera UP & DOWN (Y-axis)
	#
	#	\param value New value of the axis coordinate
	#	\param cam the MSS camera which is going to be movd
	##

	def moveCam_UpDown(self,value):
		if value == 1:
			return

		print ("\nMoving camera UP/DOWN...")
		cam=self.cam

		# ---------------------------------------------------------------
		# Obtener el tipo de camara para saber a que movimientos se accede
		command = "GETCAMERATYPE-%s$" % cam.name
		reply = " " * CMD_STRLEN_DEF
		cam.send_command(command, reply, False)  ##send command
		# ---------------------------------------------------------------
		##create command
		switch={
			0: "MOVECAMARAUP-%s$" % cam.name,
			2: "MOVECAMARADOWN-%s$" % cam.name
		}
		command=switch[value]
		reply=" "*CMD_STRLEN_DEF
		cam.send_command(command, reply, True)	##send command
		cv2.setTrackbarPos("Up/Down", cam.name, 1) ##set to initial state




	##
	#	\brief Callback method to move the camera LEFT & RIGHT (X-axis)
	#
	#	\param value New value of the axis coordinate
	#	\param cam the MSS camera which is going to be moved
	##
	def moveCam_LeftRight(self,value):
		if value == 1:
			return

		print ("\nMoving camera LEFT/RIGHT...")
		cam=self.cam

		# ---------------------------------------------------------------
		# Obtener el tipo de camara para saber a que movimientos se accede
		command = "GETCAMERATYPE-%s$" % cam.name
		reply = " " * CMD_STRLEN_DEF
		cam.send_command(command, reply, False)  ##send command
		# ---------------------------------------------------------------

		##create command
		switch={
			0: "MOVECAMARALEFT-%s$" % cam.name,
			2: "MOVECAMARARIGHT-%s$" % cam.name
		}
		command=switch[value]
		reply=" "*CMD_STRLEN_DEF
		cam.send_command(command, reply, True)	##send command
		cv2.setTrackbarPos("Left/Right", cam.name, 1) ##set to initial state

	##
	#	\brief Callback method to move the camera FORWARD & BACKWARD (Z-axis)
	#
	#	\param value New value of the axis coordinate
	#	\param cam the MSS camera which is going to be moved
	##
	def moveCam_AheadBack(self,value):
		if value == 1:
			return

		print ("\nMoving camera FORWARD/BACKWARD...")
		cam=self.cam

		# ---------------------------------------------------------------
		# Obtener el tipo de camara para saber a que movimientos se accede
		command = "GETCAMERATYPE-%s$" % cam.name
		reply = " " * CMD_STRLEN_DEF
		cam.send_command(command, reply, False)  ##send command
		# ---------------------------------------------------------------

		##create command
		switch={
			0: "MOVECAMARAAHEAD-%s$" % cam.name,
			2: "MOVECAMARABACK-%s$" % cam.name
		}
		command=switch[value]
		reply=" "*CMD_STRLEN_DEF
		cam.send_command(command, reply, True)	##send command
		cv2.setTrackbarPos("Ahead/Back", cam.name, 1) ##set to initial state

	##
	#	\brief Callback method to rotate the camera LEFT & RIGHT (X-axis)
	#
	#	\param value New value of the axis coordinate
	#	\param cam the MSS camera which is going to be moved
	##
	def moveCam_rotateLeftRight(self,value):
		if value == 1:
			return

		print ("\nRotating camera LEFT/RIGHT...")
		cam=self.cam

		# ---------------------------------------------------------------
		# Obtener el tipo de camara para saber a que movimientos se accede
		command = "GETCAMERATYPE-%s$" % cam.name
		reply = " " * CMD_STRLEN_DEF
		cam.send_command(command, reply, False)  ##send command
		# ---------------------------------------------------------------

		##create command
		switch={
			0: "ROTATECAMARALEFT-%s$" % cam.name,
			2: "ROTATECAMARARIGHT-%s$" % cam.name
		}
		command=switch[value]
		reply=" "*CMD_STRLEN_DEF
		cam.send_command(command, reply, True)	##send command
		cv2.setTrackbarPos("rotate L/R", cam.name, 1) ##set to initial state

	##
	#	\brief Callback method to rotate the camera UP & DOWN (Y-axis)
	#
	#	\param value New value of the axis coordinate
	#	\param cam the MSS camera which is going to be moved
	##
	def moveCam_rotateUpDown(self,value):
		if value == 1:
			return

		print ("\nRotating camera UP/DOWN...")
		cam=self.cam

		# ---------------------------------------------------------------
		# Obtener el tipo de camara para saber a que movimientos se accede
		command = "GETCAMERATYPE-%s$" % cam.name
		reply = " " * CMD_STRLEN_DEF
		cam.send_command(command, reply, False)  ##send command
		# ---------------------------------------------------------------

		##create command
		switch={
			0: "ROTATECAMARAUP-%s$" % cam.name,
			2: "ROTATECAMARADOWN-%s$" % cam.name
		}
		command=switch[value]
		reply=" "*CMD_STRLEN_DEF
		cam.send_command(command, reply, True)	##send command
		cv2.setTrackbarPos("rotate U/D", cam.name, 1) ##set to initial state
