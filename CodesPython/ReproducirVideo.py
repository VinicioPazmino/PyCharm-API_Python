import numpy as np
import cv2

#captura = cv2.VideoCapture('VideoSalida.avi')
captura = cv2.VideoCapture('Semantic.mp4')

while captura.isOpened():
    ret,frame=captura.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Video',frame)
    #cv2.imshow(imagen)
    if cv2.waitKey(9000) & 0xFF == ord('s'):
        break
    else: break
captura.release()
cv2.destroyAllWindows()