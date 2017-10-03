from Components.Base import *
from enum import Enum


class DustDirection(Enum):
    NONE = 0    # Points everywhere
    NS = 1      # North-South
    NE = 2      # North-East
    NW = 3      # North-West
    SE = 4      # South-East
    SW = 5      # South-West
    EW = 6      # East-West
    NSW = 7     # North-South-West
    NSE = 8     # North-South-East
    NEW = 9     # North-East-West
    SEW = 10    # SouthEast-West

    def isNorth(self):
        val = self.value
        return val is 0 or val is 1 or val is 2 or val is 3 or val is 7 or val is 8 or val is 9

    def isSouth(self):
        val = self.value
        return val is 0 or val is 1 or val is 4 or val is 5 or val is 7 or val is 8 or val is 10

    def isEast(self):
        val = self.value
        return val is 0 or val is 2 or val is 4 or val is 6 or val is 8 or val is 9 or val is 10

    def isWest(self):
        val = self.value
        return val is 0 or val is 3 or val is 5 or val is 6 or val is 7 or val is 9 or val is 10


class Dust(Base):
    compType = Component.DUST
    direction = DustDirection.NONE
    powerSources = []

    @staticmethod
    def shouldConnect(compType):
        if compType is Component.DUST:
            return True
        elif compType is Component.TORCH:
            return True
        elif compType is Component.BLOCK:
            return False
        elif compType is Component.AIR:
            return False

    def checkDirection(self):
        N = self.shouldConnect(self.northComp().compType)
        E = self.shouldConnect(self.eastComp().compType)
        S = self.shouldConnect(self.southComp().compType)
        W = self.shouldConnect(self.westComp().compType)
        if N and E and S and W:
            self.direction = DustDirection.NONE
            return
        if N:
            if S:
                if E:
                    self.direction = DustDirection.NSE
                    return
                if W:
                    self.direction = DustDirection.NSW
                    return
                self.direction = DustDirection.NS
                return
            if E:
                if W:
                    self.direction = DustDirection.NEW
                    return
                self.direction = DustDirection.NE
                return
            if W:
                self.direction = DustDirection.NW
                return
            self.direction = DustDirection.NS
            return
        if S:
            if E:
                if W:
                    self.direction = DustDirection.SEW
                    return
                self.direction = DustDirection.SE
                return
            if W:
                self.direction = DustDirection.SW
                return
            self.direction = DustDirection.NS
            return
        if E:
            self.direction = DustDirection.EW
            return
        if W:
            self.direction = DustDirection.EW
            return

    def pointsTo(self, comp) -> bool:
        dx = self.x - comp.x
        dy = self.y - comp.y
        dz = self.z - comp.z
        if dy is not 0:
            return False
        if dx > 1 or dx < -1 or dz > 1 or dz < -1:
            return False
        if dx is -1 and dz is 0:
            return self.direction.isNorth()
        if dx is 1 and dz is 0:
            return self.direction.isSouth()
        if dx is 0 and dz is -1:
            return self.direction.isEast()
        if dx is 0 and dz is 1:
            return self.direction.isWest()
        return False

    def powers(self, comp) -> bool:
        if not self.isPowering:
            return False
        if (abs(self.x - comp.x) + abs(self.y - comp.y) + abs(self.z - comp.z)) > 1:
            return False
        if self.y - comp.y is 1 and comp.compType is Component.BLOCK:
            return True
        if self.pointsTo(comp) and (comp.compType is Component.BLOCK or comp.compType is Component.DUST):
            return True
        return False

    def update(self):
        self.checkDirection()
        self.powerSources = []
        if self.poweredByBottomComp():
            self.powerSources.append(self.bottomComp())
        if self.poweredByNorthComp():
            self.powerSources.append(self.northComp())
        if self.poweredByEastComp():
            self.powerSources.append(self.eastComp())
        if self.poweredBySouthComp():
            self.powerSources.append(self.southComp())
        if self.poweredByWestComp():
            self.powerSources.append(self.westComp())
        if self.poweredByTopComp():
            self.powerSources.append(self.topComp())
        if self.isPowered and not self.poweredByAdjacent():
            self.isPowered = False
            self.isPowering = False
            self.updateAdjacent()
        if not self.isPowered and self.poweredByAdjacent():
            self.isPowered = True
            self.isPowering = True
            self.scheduleUpdate()
            self.northComp().scheduleUpdate()
            self.eastComp().scheduleUpdate()
            self.southComp().scheduleUpdate()
            self.eastComp().scheduleUpdate()
        if self.isPowered and self.poweredByAdjacent():
            if self.powers(self.northComp()) and not self.northComp().isPowered:
                self.northComp().scheduleUpdate()
            if self.powers(self.southComp()) and not self.southComp().isPowered:
                self.southComp().scheduleUpdate()
            if self.powers(self.eastComp()) and not self.eastComp().isPowered:
                self.eastComp().scheduleUpdate()
            if self.powers(self.westComp()) and not self.westComp().isPowered:
                self.westComp().scheduleUpdate()
            if self.powers(self.bottomComp()) and not self.bottomComp().isPowered:
                self.bottomComp().scheduleUpdate()
            if self.poweredOnlyByDust():
                self.isPowered = False
                self.isPowering = False
                self.updateAdjacent()

    def scheduleUpdate(self):
        self.cont.scheduleUpdate(self, 0)

    def poweredOnlyByDust(self):
        localCopy = self.powerSources.copy()
        for i in range(16):
            for e in localCopy:
                if e.compType is Component.DUST:
                    localCopy = localCopy + e.powerSources
                else:
                    return False
        return True