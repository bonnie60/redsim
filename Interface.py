import Controller
from Components import Base
from Components import Block
from Components import Dust
from Components import Torch


class Interface:
    cont = Controller

    def __init__(self, cont):
        self.cont = cont

    def addDust(self, x, y, z):
        comp = Dust(x, y, z, self.cont)
        self.cont.components[x][y][z] = comp
        return comp

    def addAir(self, x, y, z):
        comp = Base(x, y, z, self.cont)
        self.cont.components[x][y][z] = comp
        return comp

    def addBlock(self, x, y, z):
        comp = Block(x, y, z, self.cont)
        self.cont.components[x][y][z] = comp
        return comp

    def addTorch(self, x, y, z, attachedX=None, attachedY=None, attachedZ=None):
        if attachedX is None:
            attachedX = x
            attachedY = y
            attachedZ = z
        comp = Torch(x, y, z, self.cont)
        comp.attachedX = attachedX
        comp.attachedY = attachedY
        comp.attachedZ = attachedZ
        self.cont.components[x][y][z] = comp
        return comp
