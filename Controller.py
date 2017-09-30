from Components.Base import Base


class Controller:
    toUpdate = {}
    components = []
    worldSize = int

    def scheduleUpdate(self, comp):
        if comp in self.toUpdate:
            return
        self.toUpdate[comp] = 1

    def __init__(self, size):
        self.worldSize = size
        self.components = self.components = [[[Base(i, j, k, self) for k in range(self.worldSize)] for j in range(self.worldSize)] for i in range(self.worldSize)]

    def tick(self):
        toDel = []
        updateCpy = self.toUpdate.copy()
        for k in updateCpy.keys():
            if updateCpy[k] is 0:
                k.update()
                toDel.append(k)
            if 0 not in updateCpy.values():
                updateCpy[k] -= 1
        print(updateCpy)
        for d in toDel:
            del updateCpy[d]
            del self.toUpdate[d]
        print(updateCpy)
        self.toUpdate.update(updateCpy)
        if 0 in self.toUpdate.values():
            self.tick()

    def getComponent(self, x, y, z):
        try:
            return self.components[x][y][z]
        except:
            return Base(0, 0, 0, self)

    def getComp(self, x, y, z):
        try:
            return self.components[x][y][z]
        except:
            return Base(0, 0, 0, self)
