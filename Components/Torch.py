from Components.Base import *


class Torch(Base):
    attachedX = int
    attachedY = int
    attachedZ = int
    compType = Component.TORCH

    def __init__(self, x: int, y: int, z: int, cont: Controller):
        super().__init__(x, y, z, cont)
        self.attachedX = x
        self.attachedY = y-1
        self.attachedZ = z
        self.isPowering = True

    def update(self):
        if self.topComp().compType is Component.BLOCK:
            if not self.topComp().isPoweredStrongly:
                self.topComp().update()
        if self.attachedComp().powers(self) and self.isPowering:
            self.isPowered = True
            self.isPowering = False
            self.scheduleUpdate()
        if not self.attachedComp().powers(self) and self.isPowered:
            self.isPowered = False
            self.isPowering = True
            self.scheduleUpdate()
        if self.northComp().poweredByAdjacent() and not self.northComp().isPowered:
            self.northComp().scheduleUpdate()
        if self.eastComp().poweredByAdjacent() and not self.eastComp().isPowered:
            self.eastComp().scheduleUpdate()
        if self.southComp().poweredByAdjacent() and not self.southComp().isPowered:
            self.southComp().scheduleUpdate()
        if self.westComp().poweredByAdjacent() and not self.westComp().isPowered:
            self.westComp().scheduleUpdate()
        if not self.northComp().poweredByAdjacent() and self.northComp().isPowered:
            self.northComp().scheduleUpdate()
        if not self.eastComp().poweredByAdjacent() and self.eastComp().isPowered:
            self.eastComp().scheduleUpdate()
        if not self.southComp().poweredByAdjacent() and self.southComp().isPowered:
            self.southComp().scheduleUpdate()
        if not self.westComp().poweredByAdjacent() and self.westComp().isPowered:
            self.westComp().scheduleUpdate()

    def attachedComp(self):
        return self.getComp(self.attachedX, self.attachedY, self.attachedZ)

    def powers(self, comp) -> bool:
        if comp.compType is Component.BLOCK:
            return (comp.y is self.y+1 and comp.x is self.x and comp.z is self.z) and self.isPowering
        if comp.compType is Component.TORCH:
            return False
        if comp.compType is Component.DUST:
            comp.checkDirection()
            return (comp.pointsTo(self)) and self.isPowering
