import sys
from functions.MSSclient import *
from utils.MSSutils import *
from utils.CLParser import *
import socket
from random import randint
from functions.MSScam import *
import numpy as np
from math import *
import time

class DrawDisplay:
    def __init__(self):
        self.vecMat = []
        self.windowHeight = 960
        self.nRows = 1

    def makeCanvas(self,vecImg, windowHeight, nRows):
        self.vecMat = vecImg
        self.windowHeight = windowHeight
        self.nRows = nRows

        N = len(self.vecMat)
        self.nRows = min(N, self.nRows)
        edgeThickness = 10
        imagesPerRow = int(ceil(float(N) / self.nRows))
        resizeHeight = floor(2.0 * ((floor(float(self.windowHeight - edgeThickness) / self.nRows)) / 2.0)) - edgeThickness
        resizeWidth = []
        for i in range(0, N):
            resizeWidth.append(float(resizeHeight) / self.vecMat[i].shape[0] * self.vecMat[i].shape[1])
            maxresizeWidth = int(max(resizeWidth))
            windowWidth = imagesPerRow * (maxresizeWidth + edgeThickness) + edgeThickness
            canvasImage = np.zeros((int(self.windowHeight), int(windowWidth), 3), np.uint8)
        for k in range(0, N):
            currentImage_pil = Image.fromarray(np.uint8(self.vecMat[k]))
            currentImage_pil = currentImage_pil.resize((int(resizeWidth[k]), int(resizeHeight)))
            currentImage = np.array(currentImage_pil)
            i = k // imagesPerRow
            j = k % imagesPerRow
            currentHeight = i * (resizeHeight + edgeThickness) + edgeThickness
            currentWidth = j * (maxresizeWidth + edgeThickness) + edgeThickness
            canvasImage[int(currentHeight):int(currentHeight + resizeHeight),
            int(currentWidth):int(currentWidth + resizeWidth[k])] = currentImage
        return canvasImage

