import numpy as np
import scipy.misc as sp
import Controller
from Components.Base import Component
import os
from moviepy.editor import ImageSequenceClip
from PIL import Image, ImageDraw, ImageFont


class Renderer:
    cont = Controller

    def __init__(self, cont):
        self.cont = cont

    def render(self, layer):
        blocks = [[self.cont.components[x][layer][z] for x in range(self.cont.worldSize)] for z in range(self.cont.worldSize)]
        data = np.zeros((self.cont.worldSize*8, self.cont.worldSize*8, 3), dtype=np.uint8)
        for x in range(len(blocks)):
            for z in range(len(blocks[0])):
                c = self.cont.getComp(x, layer, z)
                if c.compType is Component.BLOCK:
                    if c.isPowering:
                        for i in range(8):
                            for j in range(8):
                                data[x*8+i][z*8+j] = [50, 0, 0]
                    else:
                        for i in range(8):
                            for j in range(8):
                                data[x*8+i][z*8+j] = [228, 244, 0]
                elif c.compType is Component.TORCH:
                    if c.isPowering:
                        for i in range(8):
                            for j in range(8):
                                data[x*8+i][z*8+j] = [255, 0, 0]
                    else:
                        for i in range(8):
                            for j in range(8):
                                data[x*8+i][z*8+j] = [102, 81, 81]
                elif c.compType is Component.DUST:
                    color = [165, 38, 38] if c.isPowering else [0, 255, 0]
                    for i in range(8):
                        for j in range(8):
                            data[x*8 + i][z*8 + j] = [255, 255, 255]
                    # Middle Block which is there for every piece of dust
                    xoff = 0
                    zoff = 0
                    data[x * 8 + 3 + xoff][z * 8 + 3 + zoff] = color
                    data[x * 8 + 3 + xoff][z * 8 + 4 + zoff] = color
                    data[x * 8 + 3 + xoff][z * 8 + 5 + zoff] = color
                    data[x * 8 + 4 + xoff][z * 8 + 3 + zoff] = color
                    data[x * 8 + 4 + xoff][z * 8 + 4 + zoff] = color
                    data[x * 8 + 4 + xoff][z * 8 + 5 + zoff] = color
                    data[x * 8 + 5 + xoff][z * 8 + 3 + zoff] = color
                    data[x * 8 + 5 + xoff][z * 8 + 4 + zoff] = color
                    data[x * 8 + 5 + xoff][z * 8 + 5 + zoff] = color
                    if c.direction.isNorth():
                        xoff = 2
                        yoff = 0
                        data[x * 8 + 3 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 3 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 3 + xoff][z * 8 + 5 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 5 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 5 + zoff] = color
                    if c.direction.isEast():
                        xoff = 0
                        zoff = 2
                        data[x * 8 + 3 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 3 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 3 + xoff][z * 8 + 5 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 5 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 5 + zoff] = color
                    if c.direction.isSouth():
                        xoff = -2
                        zoff = 0
                        data[x * 8 + 3 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 3 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 3 + xoff][z * 8 + 5 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 5 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 5 + zoff] = color
                    if c.direction.isWest():
                        xoff = 0
                        zoff = -2
                        data[x * 8 + 3 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 3 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 3 + xoff][z * 8 + 5 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 4 + xoff][z * 8 + 5 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 3 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 4 + zoff] = color
                        data[x * 8 + 5 + xoff][z * 8 + 5 + zoff] = color

                else:
                    for i in range(8):
                        for j in range(8):
                            data[x*8 + i][z*8 + j] = [255, 255, 255]
        for x in range(len(data)):
            for y in range(len(data)):
                if data[x][y] is [0, 0, 0]:
                    data[x][y] = [0, 0, 255]
                if x % 8 is 0 or y % 8 is 0:
                    data[x][y] = [0, 0, 0]
        return data

    def gif(self, filename, array, fps=10):
        clip = ImageSequenceClip(array, fps=fps)
        clip.write_gif(filename, fps=fps)
        return clip

    def toImage(self, layer, tickNumber, drawTicks=True):
        data = self.render(layer)
        data = sp.imrotate(data, 180)
        data = np.fliplr(data)
        im = sp.toimage(data)
        drw = ImageDraw.Draw(im)
        fnt = ImageFont.truetype('DroidSansMono.ttf', 40)
        if drawTicks:
            drw.text((1, 1), str(tickNumber), font=fnt, fill=(0, 0, 255, 255))
        return sp.fromimage(im)
