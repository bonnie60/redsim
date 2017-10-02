import Controller
from enum import Enum


class Component(Enum):
    AIR = 0
    BLOCK = 1
    DUST = 2
    TORCH = 3


class Base:
    """
    Common Variables
    Shared between all components
    """
    x = int
    y = int
    z = int
    cont = Controller
    compType = Component.AIR
    isPowering = False
    isPowered = False

    def __init__(self, x: int, y: int, z: int, cont: Controller):
        self.x = x
        self.y = y
        self.z = z
        self.cont = cont

    def poweredByAdjacent(self) -> bool:
        return (self.cont.getComp(self.x + 1, self.y, self.z).powers(self) or
                self.cont.getComp(self.x - 1, self.y, self.z).powers(self) or
                self.cont.getComp(self.x, self.y + 1, self.z).powers(self) or
                self.cont.getComp(self.x, self.y - 1, self.z).powers(self) or
                self.cont.getComp(self.x, self.y, self.z + 1).powers(self) or
                self.cont.getComp(self.x, self.y, self.z - 1).powers(self))

    def updateAdjacent(self):
        self.cont.getComp(self.x + 1, self.y, self.z).scheduleUpdate()
        self.cont.getComp(self.x - 1, self.y, self.z).scheduleUpdate()
        self.cont.getComp(self.x, self.y + 1, self.z).scheduleUpdate()
        self.cont.getComp(self.x, self.y - 1, self.z).scheduleUpdate()
        self.cont.getComp(self.x, self.y, self.z + 1).scheduleUpdate()
        self.cont.getComp(self.x, self.y, self.z - 1).scheduleUpdate()

    def update(self):
        pass

    def northComp(self):
        return self.cont.getComp(self.x + 1, self.y, self.z)

    def southComp(self):
        return self.cont.getComp(self.x - 1, self.y, self.z)

    def eastComp(self):
        return self.cont.getComp(self.x, self.y, self.z + 1)

    def westComp(self):
        return self.cont.getComp(self.x, self.y, self.z - 1)

    def topComp(self):
        return self.cont.getComp(self.x, self.y + 1, self.z)

    def bottomComp(self):
        return self.cont.getComp(self.x, self.y - 1, self.z)

    def scheduleUpdate(self):
        if self.compType is Component.TORCH and self.x is 16:
            print("test")
        self.cont.scheduleUpdate(self, 1)

    def isAdjacent(self, comp):
        return (self.northComp() is comp or
                self.southComp() is comp or
                self.eastComp() is comp or
                self.westComp() is comp or
                self.bottomComp() is comp or
                self.topComp() is comp)

    def getComp(self, x, y, z):
        return self.cont.getComponent(x, y, z)

    def powers(self, comp):
        return False
