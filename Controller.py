from Components.Base import Base
from Renderer import *
from array2gif import write_gif
from PIL import Image, ImageDraw, ImageFont
import scipy.misc as sp
import numpy as np

class Controller:
    toUpdate = {}
    components = []
    worldSize = int

    def scheduleUpdate(self, comp, time):
        if comp in self.toUpdate:
            return
        self.toUpdate[comp] = time

    def __init__(self, size):
        self.worldSize = size
        self.components = self.components = [[[Base(i, j, k, self) for k in range(self.worldSize)] for j in range(self.worldSize)] for i in range(self.worldSize)]

    def tick(self):
        while 0 in self.toUpdate.values():
            copy = self.toUpdate.copy()
            for k in copy.keys():
                if copy[k] is 0:
                    k.update()
                    self.toUpdate[k] -= 1
        toDelete = []
        for k in self.toUpdate.keys():
            if self.toUpdate[k] < 0:
                toDelete.append(k)
        for k in toDelete:
            del self.toUpdate[k]
        for k in self.toUpdate.keys():
            self.toUpdate[k] -= 1

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

    def simulate(self, ticks, output, fps=24, drawTicks=True):
        rend = Renderer(self)
        runtime = ticks
        frames = []
        emptyCount = 0
        for i in range(runtime):
            self.tick()
            data = rend.render(0)
            data = sp.imrotate(data, 180)
            data = np.fliplr(data)
            im = sp.toimage(data)
            drw = ImageDraw.Draw(im)
            fnt = ImageFont.truetype('DroidSansMono.ttf', 40)
            if drawTicks:
                drw.text((1, 1), str(i), font=fnt, fill=(0, 0, 255, 255))
            data = sp.fromimage(im)
            frames.append(data)
            if not self.toUpdate:
                emptyCount += 1
            else:
                emptyCount = 0
            if emptyCount > 3:
                break
            print("Processing tick " + str(i))

        rend.gif(output, frames, fps=fps)
