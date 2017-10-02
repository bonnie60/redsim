from Components.Base import *


class Block(Base):
    isPoweringStrong = False
    compType = Component.BLOCK

    def powers(self, comp):
        if comp.compType is Component.BLOCK:
            return False
        if (abs(self.x - comp.x) + abs(self.y - comp.y) + abs(self.z - comp.z)) > 1:
            return False
        if self.isPoweringStrong:
            if comp.compType is Component.DUST and self.isAdjacent(comp):
                return True
        if self.isPowering:
            if comp.compType is Component.TORCH:
                return comp.attachedX is self.x and comp.attachedY is self.y and comp.attachedZ is self.z
        return False

    def update(self):
        if self.isPowered and not self.poweredByAdjacent():
            self.isPowered = False
            self.isPoweringStrong = False
            self.isPowering = False
            self.updateAdjacent()
        if not self.isPowered and self.poweredByAdjacent():
            self.isPowered = True
            self.checkPower()
            self.updateAdjacent()

    def checkPower(self):
        if self.bottomComp().compType is Component.TORCH and self.bottomComp().powers(self):
            self.isPoweringStrong = True
        self.isPowering = True

    def scheduleUpdate(self):
        self.cont.scheduleUpdate(self, 0)
